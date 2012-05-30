from django.core.urlresolvers import reverse
from django.test import TestCase

class LotViewsTestCase(TestCase):
    fixtures = [
        'lots_test.json',
    ]

    def test_base_query(self):
        """
        Tests base lots query
        """
        base_query = '?boroughs=Brooklyn&lot_type=vacant,organizing,accessed,private_accessed'
        resp = self.client.get(reverse('lots.views.lot_geojson') + base_query)
        self.assertEqual(resp.status_code, 200)
