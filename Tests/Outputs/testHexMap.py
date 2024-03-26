import ast
import os
import re
import unittest

import networkx as nx
import pytest

from PyRoute.DeltaDebug.DeltaDictionary import DeltaDictionary, SectorDictionary
from PyRoute.DeltaDebug.DeltaGalaxy import DeltaGalaxy
from PyRoute.Outputs.HexMap import HexMap
from PyRoute.Outputs.PDFHexMap import PDFHexMap
from Tests.baseTest import baseTest


class testHexMap(baseTest):
    timestamp_regex = rb'(\d{14,})'
    md5_regex = rb'([0-9a-f]{32,})'
    timeline = re.compile(timestamp_regex)
    md5line = re.compile(md5_regex)

    def test_document_object(self):
        sourcefile = self.unpack_filename('DeltaFiles/no_subsectors_named/Zao Kfeng Ig Grilokh empty.sec')

        args = self._make_args()
        args.interestingline = None
        args.interestingtype = None
        args.maps = True
        args.subsectors = True

        delta = DeltaDictionary()
        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        delta[sector.name] = sector

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output

        secname = 'Zao Kfeng Ig Grilokh'

        hexmap = HexMap(galaxy, 'trade')

        blurb = [
            ("Live map", True, os.path.abspath(args.output + '/Zao Kfeng Ig Grilokh Sector.pdf')),
            ("Regression map", False, "string")
        ]

        for msg, is_live, expected_path in blurb:
            with self.subTest(msg):
                document = hexmap.document(galaxy.sectors[secname], is_live=is_live)
                self.assertEqual(4, document.margins.left, 'Unexpected margins value')
                # check writer properties
                if is_live:
                    self.assertTrue(hexmap.writer.session.compression, 'PDF writer compression not set')
                else:
                    self.assertFalse(hexmap.writer.session.compression, 'PDF writer compression set')
                self.assertEqual('Sector Zao Kfeng Ig Grilokh (-2,4)', hexmap.writer.title)
                self.assertEqual('Trade route map generated by PyRoute for Traveller', hexmap.writer.subject)
                self.assertEqual('PyPDFLite', hexmap.writer.creator)
                self.assertEqual(expected_path, hexmap.writer.filepath)

    def test_document_object_pdf(self):
        sourcefile = self.unpack_filename('DeltaFiles/no_subsectors_named/Zao Kfeng Ig Grilokh empty.sec')

        args = self._make_args()
        args.interestingline = None
        args.interestingtype = None
        args.maps = True
        args.subsectors = True

        delta = DeltaDictionary()
        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        delta[sector.name] = sector

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output

        secname = 'Zao Kfeng Ig Grilokh'

        hexmap = PDFHexMap(galaxy, 'trade')

        blurb = [
            ("Live map", True, os.path.abspath(args.output + '/Zao Kfeng Ig Grilokh Sector.pdf')),
            ("Regression map", False, "string")
        ]

        for msg, is_live, expected_path in blurb:
            with self.subTest(msg):
                document = hexmap.document(galaxy.sectors[secname], is_live=is_live)
                self.assertEqual(4, document.margins.left, 'Unexpected margins value')
                # check writer properties
                if is_live:
                    self.assertTrue(hexmap.writer.session.compression, 'PDF writer compression not set')
                else:
                    self.assertFalse(hexmap.writer.session.compression, 'PDF writer compression set')
                self.assertEqual('Sector Zao Kfeng Ig Grilokh (-2,4)', hexmap.writer.title)
                self.assertEqual('Trade route map generated by PyRoute for Traveller', hexmap.writer.subject)
                self.assertEqual('PyPDFLite', hexmap.writer.creator)
                self.assertEqual(expected_path, hexmap.writer.filepath)

    def test_verify_empty_sector_write(self):
        sourcefile = self.unpack_filename('DeltaFiles/no_subsectors_named/Zao Kfeng Ig Grilokh empty.sec')

        outfile = self.unpack_filename('OutputFiles/verify_empty_sector_write/Zao Kfeng Ig Grilokh empty.txt')

        args = self._make_args()
        args.interestingline = None
        args.interestingtype = None
        args.maps = True
        args.subsectors = True

        delta = DeltaDictionary()
        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        delta[sector.name] = sector

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)

        galaxy.output_path = args.output

        secname = 'Zao Kfeng Ig Grilokh'

        hexmap = HexMap(galaxy, 'trade')

        oldtime = b'20230911163653'
        oldmd5 = b'8419949643701e6b438d6f3f93239cf7'

        with open(outfile, 'rb') as file:
            expected_result = file.read()

        result = hexmap.write_sector_pdf_map(galaxy.sectors[secname], is_live=False)
        self.assertIsNotNone(result)
        # rather than try to mock datetime.now(), patch the output result.
        # this also lets us check that there's only a single match
        matches = self.timeline.search(result)
        self.assertEqual(1, len(matches.groups()), 'Should be exactly one create-date match')
        result = self.timeline.sub(oldtime, result)
        # likewise patch md5 outout
        matches = self.md5line.findall(result)
        self.assertEqual(2, len(matches), 'Should be exactly two MD5 matches')
        result = self.md5line.sub(oldmd5, result)
        self.assertEqual(expected_result, result)

    def test_verify_empty_sector_write_pdf(self):
        sourcefile = self.unpack_filename('DeltaFiles/no_subsectors_named/Zao Kfeng Ig Grilokh empty.sec')

        outfile = self.unpack_filename('OutputFiles/verify_empty_sector_write/Zao Kfeng Ig Grilokh empty.txt')

        args = self._make_args()
        args.interestingline = None
        args.interestingtype = None
        args.maps = True
        args.subsectors = True

        delta = DeltaDictionary()
        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        delta[sector.name] = sector

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)

        galaxy.output_path = args.output

        secname = 'Zao Kfeng Ig Grilokh'

        hexmap = PDFHexMap(galaxy, 'trade')

        oldtime = b'20230911163653'
        oldmd5 = b'8419949643701e6b438d6f3f93239cf7'

        with open(outfile, 'rb') as file:
            expected_result = file.read()

        result = hexmap.write_sector_pdf_map(galaxy.sectors[secname], is_live=False)
        self.assertIsNotNone(result)
        # rather than try to mock datetime.now(), patch the output result.
        # this also lets us check that there's only a single match
        matches = self.timeline.search(result)
        self.assertEqual(1, len(matches.groups()), 'Should be exactly one create-date match')
        result = self.timeline.sub(oldtime, result)
        # likewise patch md5 outout
        matches = self.md5line.findall(result)
        self.assertEqual(2, len(matches), 'Should be exactly two MD5 matches')
        result = self.md5line.sub(oldmd5, result)
        self.assertEqual(expected_result, result)

    @pytest.mark.xfail(reason='Flaky on ubuntu')
    def test_verify_subsector_trade_write(self):
        sourcefile = self.unpack_filename('DeltaFiles/no_subsectors_named/Zao Kfeng Ig Grilokh - subsector P.sec')
        outfile = self.unpack_filename('OutputFiles/verify_subsector_trade_write/Zao Kfeng Ig Grilokh - subsector P - trade.txt')

        starsfile = self.unpack_filename('OutputFiles/verify_subsector_trade_write/trade stars.txt')
        rangesfile = self.unpack_filename('OutputFiles/verify_subsector_trade_write/trade ranges.txt')

        args = self._make_args()
        args.interestingline = None
        args.interestingtype = None
        args.maps = True
        args.subsectors = True
        args.routes = 'trade'

        delta = DeltaDictionary()
        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        delta[sector.name] = sector

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output

        galaxy.generate_routes()

        with open(starsfile, 'rb') as file:
            galaxy.stars = nx.read_edgelist(file, nodetype=int)
        self.assertEqual(26, len(galaxy.stars.nodes()), "Unexpected number of stars nodes")
        self.assertEqual(53, len(galaxy.stars.edges), "Unexpected number of stars edges")
        for item in galaxy.stars.edges(data=True):
            self.assertIn('trade', item[2], 'Trade value not set during edgelist read')

        self._load_ranges(galaxy, rangesfile)
        self.assertEqual(27, len(galaxy.ranges.nodes()), "Unexpected number of ranges nodes")
        self.assertEqual(44, len(galaxy.ranges.edges), "Unexpected number of ranges edges")

        secname = 'Zao Kfeng Ig Grilokh'

        hexmap = HexMap(galaxy, 'trade')

        oldtime = b'20230912001440'
        oldmd5 = b'b1f97f6ac37340ab332a9a0568711ec0'

        with open(outfile, 'rb') as file:
            expected_result = file.read()

        result = hexmap.write_sector_pdf_map(galaxy.sectors[secname], is_live=False)
        self.assertIsNotNone(result)
        # rather than try to mock datetime.now(), patch the output result.
        # this also lets us check that there's only a single match
        matches = self.timeline.search(result)
        self.assertEqual(1, len(matches.groups()), 'Should be exactly one create-date match')
        result = self.timeline.sub(oldtime, result)
        # likewise patch md5 output
        matches = self.md5line.findall(result)
        self.assertEqual(2, len(matches), 'Should be exactly two MD5 matches')
        result = self.md5line.sub(oldmd5, result)
        self.assertEqual(expected_result, result)

    def test_verify_subsector_trade_write_pdf(self):
        sourcefile = self.unpack_filename('DeltaFiles/no_subsectors_named/Zao Kfeng Ig Grilokh - subsector P.sec')
        outfile = self.unpack_filename('OutputFiles/verify_subsector_trade_write/Zao Kfeng Ig Grilokh - subsector P - trade.txt')

        starsfile = self.unpack_filename('OutputFiles/verify_subsector_trade_write/trade stars.txt')
        rangesfile = self.unpack_filename('OutputFiles/verify_subsector_trade_write/trade ranges.txt')

        args = self._make_args()
        args.interestingline = None
        args.interestingtype = None
        args.maps = True
        args.subsectors = True
        args.routes = 'trade'

        delta = DeltaDictionary()
        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        delta[sector.name] = sector

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output

        galaxy.generate_routes()

        with open(starsfile, 'rb') as file:
            galaxy.stars = nx.read_edgelist(file, nodetype=int)
        self.assertEqual(26, len(galaxy.stars.nodes()), "Unexpected number of stars nodes")
        self.assertEqual(53, len(galaxy.stars.edges), "Unexpected number of stars edges")
        for item in galaxy.stars.edges(data=True):
            self.assertIn('trade', item[2], 'Trade value not set during edgelist read')

        self._load_ranges(galaxy, rangesfile)
        self.assertEqual(27, len(galaxy.ranges.nodes()), "Unexpected number of ranges nodes")
        self.assertEqual(44, len(galaxy.ranges.edges), "Unexpected number of ranges edges")

        secname = 'Zao Kfeng Ig Grilokh'

        hexmap = PDFHexMap(galaxy, 'trade')

        oldtime = b'20230912001440'
        oldmd5 = b'b1f97f6ac37340ab332a9a0568711ec0'

        with open(outfile, 'rb') as file:
            expected_result = file.read()

        result = hexmap.write_sector_pdf_map(galaxy.sectors[secname], is_live=False)
        self.assertIsNotNone(result)
        # rather than try to mock datetime.now(), patch the output result.
        # this also lets us check that there's only a single match
        matches = self.timeline.search(result)
        self.assertEqual(1, len(matches.groups()), 'Should be exactly one create-date match')
        result = self.timeline.sub(oldtime, result)
        # likewise patch md5 output
        matches = self.md5line.findall(result)
        self.assertEqual(2, len(matches), 'Should be exactly two MD5 matches')
        result = self.md5line.sub(oldmd5, result)
        self.assertEqual(expected_result, result)

    def test_verify_subsector_comm_write(self):
        sourcefile = self.unpack_filename('DeltaFiles/no_subsectors_named/Zao Kfeng Ig Grilokh - subsector P.sec')
        outfile = self.unpack_filename('OutputFiles/verify_subsector_comm_write/Zao Kfeng Ig Grilokh - subsector P - comm.txt')

        starsfile = self.unpack_filename('OutputFiles/verify_subsector_comm_write/comm stars.txt')

        rangesfile = self.unpack_filename('OutputFiles/verify_subsector_comm_write/comm ranges.txt')

        args = self._make_args()
        args.interestingline = None
        args.interestingtype = None
        args.maps = True
        args.routes = 'comm'
        args.subsectors = True

        delta = DeltaDictionary()
        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        delta[sector.name] = sector

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output

        galaxy.generate_routes()

        with open(starsfile, 'rb') as file:
            galaxy.stars = nx.read_edgelist(file, nodetype=int)
        self.assertEqual(5, len(galaxy.stars.nodes()), "Unexpected number of stars nodes")
        self.assertEqual(4, len(galaxy.stars.edges), "Unexpected number of stars edges")
        for item in galaxy.stars.edges(data=True):
            self.assertIn('trade', item[2], 'Trade value not set during edgelist read')

        self._load_ranges(galaxy, rangesfile)
        self.assertEqual(27, len(galaxy.ranges.nodes()), "Unexpected number of ranges nodes")
        self.assertEqual(28, len(galaxy.ranges.edges), "Unexpected number of ranges edges")

        secname = 'Zao Kfeng Ig Grilokh'

        hexmap = HexMap(galaxy, 'trade')

        oldtime = b'20230912013953'
        oldmd5 = b'ff091edb9d8ca0abacea39e5791a9843'

        with open(outfile, 'rb') as file:
            expected_result = file.read()

        result = hexmap.write_sector_pdf_map(galaxy.sectors[secname], is_live=False)
        self.assertIsNotNone(result)
        # rather than try to mock datetime.now(), patch the output result.
        # this also lets us check that there's only a single match
        matches = self.timeline.search(result)
        self.assertEqual(1, len(matches.groups()), 'Should be exactly one create-date match')
        result = self.timeline.sub(oldtime, result)
        # likewise patch md5 output
        matches = self.md5line.findall(result)
        self.assertEqual(2, len(matches), 'Should be exactly two MD5 matches')
        result = self.md5line.sub(oldmd5, result)
        self.assertEqual(expected_result, result)

    def test_verify_subsector_comm_write_pdf(self):
        sourcefile = self.unpack_filename('DeltaFiles/no_subsectors_named/Zao Kfeng Ig Grilokh - subsector P.sec')
        outfile = self.unpack_filename('OutputFiles/verify_subsector_comm_write/Zao Kfeng Ig Grilokh - subsector P - comm.txt')

        starsfile = self.unpack_filename('OutputFiles/verify_subsector_comm_write/comm stars.txt')

        rangesfile = self.unpack_filename('OutputFiles/verify_subsector_comm_write/comm ranges.txt')

        args = self._make_args()
        args.interestingline = None
        args.interestingtype = None
        args.maps = True
        args.routes = 'comm'
        args.subsectors = True

        delta = DeltaDictionary()
        sector = SectorDictionary.load_traveller_map_file(sourcefile)
        delta[sector.name] = sector

        galaxy = DeltaGalaxy(args.btn, args.max_jump)
        galaxy.read_sectors(delta, args.pop_code, args.ru_calc,
                            args.route_reuse, args.routes, args.route_btn, args.mp_threads, args.debug_flag)
        galaxy.output_path = args.output

        galaxy.generate_routes()

        with open(starsfile, 'rb') as file:
            galaxy.stars = nx.read_edgelist(file, nodetype=int)
        self.assertEqual(5, len(galaxy.stars.nodes()), "Unexpected number of stars nodes")
        self.assertEqual(4, len(galaxy.stars.edges), "Unexpected number of stars edges")
        for item in galaxy.stars.edges(data=True):
            self.assertIn('trade', item[2], 'Trade value not set during edgelist read')

        self._load_ranges(galaxy, rangesfile)
        self.assertEqual(27, len(galaxy.ranges.nodes()), "Unexpected number of ranges nodes")
        self.assertEqual(28, len(galaxy.ranges.edges), "Unexpected number of ranges edges")

        secname = 'Zao Kfeng Ig Grilokh'

        hexmap = PDFHexMap(galaxy, 'trade')

        oldtime = b'20230912013953'
        oldmd5 = b'ff091edb9d8ca0abacea39e5791a9843'

        with open(outfile, 'rb') as file:
            expected_result = file.read()

        result = hexmap.write_sector_pdf_map(galaxy.sectors[secname], is_live=False)
        self.assertIsNotNone(result)
        # rather than try to mock datetime.now(), patch the output result.
        # this also lets us check that there's only a single match
        matches = self.timeline.search(result)
        self.assertEqual(1, len(matches.groups()), 'Should be exactly one create-date match')
        result = self.timeline.sub(oldtime, result)
        # likewise patch md5 output
        matches = self.md5line.findall(result)
        self.assertEqual(2, len(matches), 'Should be exactly two MD5 matches')
        result = self.md5line.sub(oldmd5, result)
        self.assertEqual(expected_result, result)

    def _load_ranges(self, galaxy, sourcefile):
        with open(sourcefile, "rb") as f:
            lines = f.readlines()
            for rawline in lines:
                line = rawline.strip()
                bitz = line.split(b') ')
                source = str(bitz[0]).replace('\'', '').lstrip('b')
                target = str(bitz[1]).replace('\'', '').lstrip('b')
                srcbitz = source.split('(')
                targbitz = target.split('(')
                hex1 = srcbitz[1][-4:]
                sec1 = srcbitz[1][0:-5]
                hex2 = targbitz[1][-4:]
                sec2 = targbitz[1][0:-5]

                world1 = galaxy.sectors[sec1].find_world_by_pos(hex1)
                world2 = galaxy.sectors[sec2].find_world_by_pos(hex2)
                rawdata = str(bitz[2]).lstrip('b')
                data = ast.literal_eval(ast.literal_eval(rawdata))

                galaxy.ranges.add_edge(world1, world2)
                for item in data:
                    galaxy.ranges[world1][world2][item] = data[item]


if __name__ == '__main__':
    unittest.main()
