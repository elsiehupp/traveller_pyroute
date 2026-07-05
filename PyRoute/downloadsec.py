"""
Created on Jun 3, 2014

@author: tjoneslo
"""
import argparse
import codecs
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import requests
from requests import Response, Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def get_url(url: str, sector: str, suffix: str, output_dir: str, params: dict[str, str], s: Session) -> bool:
    try:
        f: Response = s.get(url, timeout=3, params=params)
        f.raise_for_status()
    except urllib.error.HTTPError as ex:
        print("get URL failed: {} -> {}".format(url, ex))
        return False
    except urllib.error.URLError as ex:
        print("get URL failed: {} -> {}".format(url, ex))
        return False

    # requests lib handles decoding automagically
    content = f.text.replace('\r\n', '\n')
    path = os.path.join(output_dir, '%s.%s' % (sector, suffix))

    with codecs.open(path, 'wb', 'utf-8') as out:
        out.write(content)
    f.close()
    return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Download sector/metadata from TravellerMap')
    parser.add_argument('--routes', dest='routes', default=False, action='store_true',
                        help='Include route information in the sector downloads')
    parser.add_argument('sector_list', help='List of sectors to download')
    parser.add_argument('output_dir', help='output directory for sector data and xml metadata')
    parser.add_argument('--milieu', default="M1105", help="Milieu of data to download")
    args = parser.parse_args()

    with codecs.open(args.sector_list, 'r', encoding="utf-8") as f:
        sectorsList = [line for line in f]

    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    s: Session = requests.Session()
    s.mount('http://', adapter)
    s.mount('https://', adapter)

    for raw_sector in sectorsList:
        sector = raw_sector.rstrip()
        print('Downloading %s' % sector)
        params = {'sector': sector, 'type': 'SecondSurvey', "milieu": args.milieu}
        if args.routes:
            params['routes'] = '1'
        url = 'http://www.travellermap.com/api/sec'

        success = get_url(url, sector, 'sec', args.output_dir, params, s)
        if not success:
            print("Retrying " + sector)
            get_url(url, sector, 'sec', args.output_dir, params, s)

        params = {'sector': sector, 'accept': 'text/xml'}
        url = 'http://travellermap.com/api/metadata'
        success = get_url(url, sector, 'xml', args.output_dir, params, s)
        if not success:
            print("Retrying XML for " + sector)
            get_url(url, sector, 'sec', args.output_dir, params, s)

        time.sleep(5)
