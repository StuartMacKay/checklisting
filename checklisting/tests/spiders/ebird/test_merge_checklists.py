"""Tests for merging the checklists parsed from JSON and HTML together."""

from unittest import TestCase

from checklisting.spiders import ebird_spider


class MergeChecklistsTestCase(TestCase):
    """Verify merging the JSON and HTML checklists together."""

    def setUp(self):
        """Initialize the test."""
        self.spider = ebird_spider.EBirdSpider('REG')
        self.lista = {
            'identifier': 'S0000001',
            'date': '2013-03-27',
            'time': '09:00',
            'submitted_by': 'Name Surname',
            'observers': ['Name Surname'],
            'observer_count': 1,
            'source': 'eBird',
            'location': {
                'identifier': 'L0000001',
                'name': 'Location 1',
                'county': 'County',
                'region': 'Region',
                'country': 'Country',
                'lat': 45.000000,
                'lon': -45.000000,
            },
            'entries': [
                {
                    'identifier': 'OBS0000001',
                    'species': {
                        'standard_name': 'Common Name',
                        'common_name_en': 'Common Name',
                        'scientific_name': 'Scientific Name',
                    },
                    'count': 23
                }
            ]
        }
        self.listb = {
            'observers': [],
            'observer_count': 1,
            'protocol': {
                'type': 'TRV',
                'duration_hours': 2,
                'duration_minutes': 35,
                'distance': 2000,
                'area': 0,
            },
            'entries': [
                {
                    'species': {
                        'standard_name': 'Common Name',
                        'common_name_en': 'Common Name',
                        'scientific_name': 'Scientific Name',
                    },
                    'count': 23,
                    'details': [
                        {'age': 'AD', 'sex': 'M', 'count': 9},
                        {'age': 'AD', 'sex': 'F', 'count': 6},
                        {'age': 'JUV', 'sex': 'X', 'count': 8}
                    ]
                }
            ]
        }

        self.fixture = self.spider.merge_checklists(self.lista, self.listb)

    def test_observer_count(self):
        """Verify the number of observers is set."""
        self.fixture = self.spider.merge_checklists(self.lista, self.listb)
        self.assertEqual(1, self.fixture['observer_count'])

    def test_protocol(self):
        """Verify the protocol is set."""
        self.fixture = self.spider.merge_checklists(self.lista, self.listb)
        expected = {
            'type': 'TRV',
            'duration_hours': 2,
            'duration_minutes': 35,
            'distance': 2000,
            'area': 0,
        }
        self.assertEqual(expected, self.fixture['protocol'])

    def test_details(self):
        """Verify the entry details are set."""
        self.fixture = self.spider.merge_checklists(self.lista, self.listb)
        expected = [
            {'age': 'AD', 'sex': 'M', 'count': 9},
            {'age': 'AD', 'sex': 'F', 'count': 6},
            {'age': 'JUV', 'sex': 'X', 'count': 8},
        ]
        self.assertEqual(expected, self.fixture['entries'][0]['details'])

    def test_entry_added(self):
        """Verify new entries in the second list are added."""
        self.listb['entries'].append({
            'species': {
                'standard_name': 'New Name',
                'common_name_en': 'New Name',
                'scientific_name': 'New Scientific Name',
            },
            'count': 10,
            'details': []
        })
        self.fixture = self.spider.merge_checklists(self.lista, self.listb)
        self.assertEqual(2, len(self.fixture['entries']))

    def test_entry_overwritten(self):
        """Verify entries in the second list overwrite those from the first."""
        self.listb['entries'].append({
            'species': {
                'standard_name': 'Common Name',
                'common_name_en': 'Common Name',
                'scientific_name': 'Scientific Name',
            },
            'count': 10,
            'details': []
        })
        self.fixture = self.spider.merge_checklists(self.lista, self.listb)
        self.assertEqual(10, self.fixture['entries'][0]['count'])
