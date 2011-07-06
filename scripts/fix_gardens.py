#!/usr/bin/python

#
# Given a file of gardens and their BBLs, mark their lots as not vacant
#

import sys
import os
import csv

BASE_DIR = os.path.sep.join((os.path.abspath(os.path.curdir), '..'))
PROJECT_DIR = os.path.sep.join((BASE_DIR, 'fiveninesix'))

sys.path.append(BASE_DIR)
sys.path.append(PROJECT_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'fiveninesix.settings'

from fiveninesix.lots.models import Lot

def mark_as_garden(lot, garden_name, garden_id):
    lot.is_vacant = False
    lot.actual_use = "Garden|%s|%s" % (garden_name, garden_id)
    lot.save()

if __name__ == '__main__':
    gardens = csv.DictReader(open(sys.argv[1], 'r'))
    for garden in gardens:
        lots = Lot.objects.filter(bbl=garden['BBL'])
        try:
            lot = lots[0]
            print 'found lot for garden "%s", marking as non-vacant' % garden['GardenName']
            mark_as_garden(lot, garden['GardenName'], garden['GARDENID'])
        except:
            continue
