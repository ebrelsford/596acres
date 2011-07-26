import sys
import os
import csv

BASE_DIR = os.path.sep.join((os.path.abspath(os.path.curdir), '..'))
PROJECT_DIR = os.path.sep.join((BASE_DIR, 'fiveninesix'))

sys.path.append(BASE_DIR)
sys.path.append(PROJECT_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'fiveninesix.settings'

from fiveninesix.lots.models import Lot

def fix_area_for_lots(file):
    for lot in csv.DictReader(file):
        bbl = lot['BBL']
        area = lot['LotArea']

        try:
            existing_lot = Lot.objects.filter(bbl=bbl)[0]
            existing_lot.area = area
            existing_lot.save()
        except:
            continue

if __name__ == '__main__':
    fix_area_for_lots(open(sys.argv[1], 'r'))

