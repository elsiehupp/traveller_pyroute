'''
Created on Mar 5, 2014

@author: tjoneslo
'''

import logging
import bisect
import random
import math
from AllyGen import AllyGen

class Star (object):
    def __init__ (self, line, starline, sector, pop_code):
        self.sector = sector
        logging.getLogger('PyRoute.Star').debug(line)
        data = starline.match(line).groups()
        self.position = data[0].strip()
        self.set_location(sector.dx, sector.dy)
        self.name = data[1].strip()
            
        self.uwp = data[2].strip()
        self.port = self.uwp[0]
        self.size = self.uwp[1]
        self.atmo = self.uwp[2]
        self.hydro = self.uwp[3]
        self.pop   = self.uwp[4]
        self.gov   = self.uwp[5]
        self.law   = self.uwp[6]
        self.tl = int(self.uwp[8],36)
        try:
            self.popCode = int(self.pop,12)
        except ValueError:
            self.popCode = 12
            
        self.tradeCode = data[3].strip().split()
            
        if (data[6]):
            self.economics = data[6].strip()
        else:
            self.economics = None
            
        self.baseCode = data[12].strip()
        self.zone = data[13].strip()
        self.ggCount = int(data[14][2],16)
        self.popM = int(data[14][0])
        
        self.alg = data[16].strip()
        
        self.uwpCodes = {'Starport': self.port,
                           'Size': self.size,
                           'Atmosphere': self.atmo,
                           'Hydrographics': self.hydro,
                           'Population': self.pop,
                           'Government': self.gov,
                           'Law Level': self.law,
                           'Tech Level': self.uwp[8],
                           'Pop Code': str(self.popM)}
        
        self.rich = 'Ri' in self.tradeCode 
        self.industrial = 'In' in self.tradeCode 
        self.agricultural = 'Ag' in self.tradeCode 
        self.poor = 'Po' in self.tradeCode 
        self.nonIndustrial = 'Ni' in self.tradeCode 
        self.extreme = 'As' in self.tradeCode or 'Ba' in self.tradeCode or \
                'Fl' in self.tradeCode or 'Ic' in self.tradeCode or 'De' in self.tradeCode or \
                'Na' in self.tradeCode or 'Va' in self.tradeCode or 'Wa' in self.tradeCode or \
                'He' in self.tradeCode
        self.nonAgricultural = 'Na' in self.tradeCode

        if (data[5]):
            imp = int(data[5][1:-1].strip())
            self.calculate_importance()
            if imp != self.importance:
                logging.getLogger('PyRoute.Star').error(u'{}-{} Calculated importance {} does not match generated importance {}'.format(self, self.baseCode, self.importance, imp))
        else:
            self.calculate_importance()

        self.calculate_wtn()
        self.calculate_gwp(pop_code)
        self.calculate_ru()
        self.calculate_TCS()
        self.owned_by()
        self.calculate_army()
        
        self.tradeIn  = 0
        self.tradeOver = 0
        self.tradeCount = 0
        self.passIn = 0
        self.passOver = 0
        self.starportSize = 0
        self.starportBudget = 0
        self.starportPop = 0
        
    def __unicode__(self):
        return u"{} ({} {})".format(self.name, self.sector.name, self.position)
        
    def __str__(self):
        name = u"%s (%s %s)" % (self.name,self.sector.name, self.position)
	#return name
        return name.encode('utf-8')

    def __repr__(self):
        return u"{} ({} {})".format(self.name, self.sector.name, self.position)
    
    def __key(self):
        return (self.position, self.name, self.uwp, self.sector.name)

    def __eq__(self, y):
        if isinstance(y, Star):
            return self.__key() == y.__key()
        else:
            return False

    def __hash__(self):
        return hash(self.__key())

    def wiki_name(self):
        name = u" ".join(w.capitalize() for w in self.name.lower().split())
        name = u'{{WorldS|' + name + u'|' + self.sector.sector_name() + u'|' + self.position + u'}}'
        return name

    def set_location (self, dx, dy):
        # convert odd-q offset to cube
        q = int (self.position[0:2]) + dx -1
        r = int (self.position[2:4]) + dy -1
        self.x = q
        self.z = r - (q - (q & 1)) / 2
        self.y = -self.x - self.z
        
        # convert cube to axial
        self.q = self.x
        self.r = self.z

        self.col = q - dx + 1
        self.row = r - dy + 1
        
    def hex_distance(self, star):
        return max(abs(self.x - star.x), abs(self.y - star.y), abs(self.z -star.z))
        
    @staticmethod    
    def heuristicDistance(star1, star2):
        return max(abs(star1.x - star2.x), abs(star1.y - star2.y), abs(star1.z - star2.z))
    
    @staticmethod
    def axial_distance(Hex1, Hex2):
        return (abs(Hex1[0] - Hex2[0]) + abs(Hex1[1] - Hex2[1])
            + abs(Hex1[0] + Hex1[1] - Hex2[0] - Hex2[1])) / 2

    def distance (self, star):
        y1 = self.y * 2
        if not self.x % 2:
            y1 += 1
        y2 = star.y * 2
        if not star.y % 2:
            y2 += 1
        dy = y2 - y1
        if dy < 1:
            dy = -dy;
        dx = star.x - self.x
        if dx < 1:
            dx = -dx
        if dx > dy:
            return dx
        return dx + dy / 2
    
    def subsector(self):
        subsector = ["ABCD","EFGH","IJKL","MNOP"]
        indexy = (self.col - 1) / 8
        indexx = (self.row - 1) / 10
        
        return subsector[indexx][indexy]
        pass
    
    def calculate_gwp(self, pop_code):
        calcGWP = [220, 350, 560, 560, 560, 895, 895, 1430, 2289, 3660, 3660, 3660, 5860, 5860, 9375, 15000, 24400, 24400, 39000, 39000]
        popCodeM = [0, 10, 13, 17, 22, 28, 36, 47, 60, 78]

        if pop_code == 'scaled':
            self.population =int (pow (10, self.popCode) * popCodeM[self.popM] / 1e7) 
            self.uwpCodes['Pop Code'] = str(popCodeM[self.popM]/10)
            
        elif pop_code == 'fixed':
            self.population = int (pow (10, self.popCode) * self.popM / 1e6)
            
        elif pop_code == 'benford':
            popCodeRange=[0.243529203, 0.442507049, 0.610740422, 0.756470797, 0.885014099, 1]

            if self.popM >= 1 and self.popM <= 6:
                popM = popCodeM[self.popM]
            else:            
                popM = (bisect.bisect(popCodeRange, random.random()) + 4) * 10
            self.population = int (pow (10, self.popCode) * popM / 1e7)
            self.uwpCodes['Pop Code'] = str(popM/10)


        self.gwp = int (self.population * calcGWP[min(self.tl,19)] / 1000)    
        #self.gwp = int (pow(10,self.popCode) * popCodeM[self.popM] * calcGWP[self.tl] / 1e10 )
        if self.rich:
            self.gwp = self.gwp * 16 / 10
        if self.industrial:
            self.gwp = self.gwp * 14 / 10
        if self.agricultural:
            self.gwp = self.gwp * 12 / 10
        if self.poor:
            self.gwp = self.gwp * 8 / 10
        if self.nonIndustrial:
            self.gwp = self.gwp * 8 / 10
        if self.extreme:
            self.gwp = self.gwp * 8 / 10    
        
    def calculate_wtn(self):
        self.wtn = self.popCode
        self.wtn -= 1 if self.tl == 0 else 0
        self.wtn += 1 if self.tl >= 5 else 0
        self.wtn += 1 if self.tl >= 9 else 0
        self.wtn += 1 if self.tl >= 15 else 0
        
        port = self.port
             
        if port == 'A':
            self.wtn = (self.wtn * 3 + 13) / 4
        if port == 'B':
            self.wtn = (self.wtn * 3 + 11) / 4
        if port == 'C':
            if (self.wtn > 9):
                self.wtn = (self.wtn + 9) / 2
            else:
                self.wtn = (self.wtn * 3 + 9) / 4
        if port == 'D':
            if (self.wtn > 7):
                self.wtn = (self.wtn + 7) / 2
            else:
                self.wtn = (self.wtn * 3 + 7) / 4
        if port == 'E':
            if (self.wtn > 5):
                self.wtn = (self.wtn + 5) / 2
            else:
                self.wtn = (self.wtn * 3 + 5) / 4
        if port == 'X':
            self.wtn = (self.wtn - 5) / 2
            
        self.wtn = math.trunc(max(0, self.wtn))

    def calculate_ru(self):
        if not self.economics: 
            self.ru = 0
            return
        
        resources = int(self.economics[1],30)
        labor = int(self.economics[2], 20)
        if self.economics[3] == '-' :
            infrastructure = int(self.economics[3:5])
            efficency = int(self.economics[5:7])
        else:
            infrastructure = int(self.economics[3], 30)
            efficency = int(self.economics[4:6])
        
        resources = resources if resources != 0 else 1
        # No I in eHex, so J,K,L all -1
        resources -= 0 if resources < 18 else 1
        
        labor = labor if labor != 0 else 1
        labor = labor if self.popCode != 0 else 0
        
        infrastructure = infrastructure if infrastructure != 0 else 1
        infrastructure += 0 if infrastructure < 18 else -1
        
        efficency = efficency if efficency != 0 else 1
        if efficency < 0: 
            efficency = 1 + (efficency * 0.1)
            self.ru = int(round(resources * labor * infrastructure * efficency))
        else:
            self.ru = resources * labor * infrastructure * efficency
        
    def calculate_TCS(self):
        tax_rate = {'0': 0.50, '1': 0.8, '2': 1.0, '3': 0.9, '4': 0.85, 
                 '5': 0.95, '6': 1.0, '7': 1.0, '8': 1.1, '9': 1.15, 
                 'A': 1.20, 'B': 1.1, 'C': 1.2, 'D': 0.75,'E': 0.75,
                 'F': 0.75,
                 # Aslan Government codes
                 'G': 1.0, 'H': 1.0, 'J': 1.2, 'K': 1.1, 'L': 1.0,
                 'M': 1.1, 'N': 1.2,
                 # Unknown Gov Codes
                 'I': 1.0, 'P': 1.0, 'Q': 1.0, 'R': 1.0, 'S': 1.0,'T': 1.0, 
                 'U': 1.0, 'V': 1.0, 'W': 1.0, 'X': 1.0
                 }
        self.ship_capacity = long (self.population * tax_rate[self.uwpCodes['Government']] * 1000)
        gwp_base = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 28, 32]
        if self.tl >= 5:
            self.tcs_gwp = self.population * gwp_base[min(self.tl - 5, 13)] * 1000
        else:
            self.tcs_gwp = 0
            
        if self.rich:
            self.tcs_gwp = self.tcs_gwp * 16 / 10
        if self.industrial:
            self.tcs_gwp = self.tcs_gwp * 14 / 10
        if self.agricultural:
            self.tcs_gwp = self.tcs_gwp * 12 / 10
        if self.poor:
            self.tcs_gwp = self.tcs_gwp * 8 / 10
        if self.nonIndustrial:
            self.tcs_gwp = self.tcs_gwp * 8 / 10
        if self.nonAgricultural:
            self.tcs_gwp = self.tcs_gwp * 8 / 10
            
        budget = long (self.tcs_gwp * 0.03 * tax_rate[self.uwpCodes['Government']])
        
        #if AllyGen.sameAligned('Im', self.alg):
        #    budget = budget * 0.3
        
        transfer_rate = {'A': 1.0, 'B': 0.95, 'C': 0.9, 'D': 0.85, 'E': 0.8}
        
        if self.uwpCodes['Starport'] in 'ABCDE':
            access = transfer_rate[self.uwpCodes['Starport']]
            access -= (15-self.tl)*0.05
            if self.tl <= 4:
                access -= 0.05
            if self.tl <= 3:
                access -= 0.05
        else:
            access = 0
            
        if access <= 0:
            access = 0
        
        self.budget = long(budget * access)

    def calculate_importance(self):
        imp = 0
        imp += 1 if self.port in 'AB' else 0
        imp -= 1 if self.port in 'DEX' else 0
        imp += 1 if self.tl >= 10 else 0
        imp -= 1 if self.tl <= 8 else 0
        imp -= 1 if self.popCode <= 6 else 0
        imp += 1 if self.popCode >= 9 else 0
        imp += 1 if self.agricultural else 0
        imp += 1 if self.rich else 0
        imp += 1 if self.industrial else 0
        imp += 1 if self.baseCode in [u'NS', u'NW', u'W', u'D', u'X', u'RT', u'CK', u'KM'] else 0 
        self.importance = imp
        
    def owned_by(self):
        self.ownedBy = self
        for code in self.tradeCode:
            if code.startswith(u'O:'):
                self.ownedBy = code[2:]

    def calculate_army(self):
        #       3, 4, 5, 6, 7, 8, 9, A
        
        BE = [ [0, 0, 0, 0, 1, 10, 100, 1000], # TL 0
               [0, 0, 0, 1, 5, 50, 500, 5000], # TL 1
               [0, 0, 1, 5, 50, 500, 5000, 50000], # TL 2
               [0, 1, 10, 100, 1000, 10000, 50000, 100000], # TL 3
               [0, 1, 10, 100, 1000, 2000, 20000, 200000], # TL 4
               [1, 2, 3, 30, 300, 3000, 30000, 300000], # TL 5
               [1, 2, 3, 30, 300, 3000, 30000, 300000], # TL 6
               [0, 1, 2, 20, 200, 2000, 20000, 200000], # TL 7
               [0, 1, 2, 20, 200, 2000, 20000, 200000], # TL 8
               [0, 0, 1, 15, 150, 1500, 15000, 150000], # TL 9
               [0, 0, 1, 15, 150, 1500, 15000, 150000], # TL A
               [0, 0, 1, 12, 120, 1200, 12000, 120000], # TL B
               [0, 0, 1, 12, 120, 1200, 12000, 120000], # TL C
               [0, 0, 1, 10, 100, 1000, 10000, 100000], # TL D
               [0, 0, 0,  7,  70,  700,  7000,  70000], # TL E
               [0, 0, 0,  5,  50,  500,  5000,  50000], # TL F
               [0, 0, 0,  5,  50,  500,  5000,  50000], # TL G
            ]
        
        pop_code = min(self.popCode - 3, 7)
        if self.uwpCodes['Atmosphere'] not in ['568']:
            pop_code -= 1
        if pop_code >= 0:
            self.raw_be = BE[min(self.tl, 16)][pop_code]
        else: 
            self.raw_be = 0
 
        self.col_be = self.raw_be * 0.1 if self.tl >= 9 else 0
            
        if AllyGen.are_allies(u'Im', self.alg):
            self.im_be = self.raw_be * 0.05
            if self.tl < 13:
                mul = 1-((13 - self.tl)/10.0)
                self.im_be = self.im_be * mul
        else:
            self.im_be = 0
            
        
