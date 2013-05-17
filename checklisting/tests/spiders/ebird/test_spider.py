"""Tests for initializing and starting the EBirdSpider."""

from unittest import TestCase

from checklisting.spiders import ebird_spider


class InitializeSpiderTestCase(TestCase):
    """Tests to verify the spider initialization."""

    def test_region(self):
        """Verify the ebird region is set."""
        spider = ebird_spider.EBirdSpider('REG', 10, '.')
        self.assertEqual('REG', spider.region)

    def test_duration(self):
        """Verify the number of days to fetch observations for is set."""
        spider = ebird_spider.EBirdSpider('REG', 10, '.')
        self.assertEqual(10, spider.duration)

    def test_directory(self):
        """Verify the directory where checklists are saved is set."""
        spider = ebird_spider.EBirdSpider('REG', 10, "/tmp")
        self.assertEqual("/tmp", spider.directory)


class StartRequestsTestCase(TestCase):
    """Verify the initial request for the recent observations of a region."""

    def setUp(self):
        """Initialize the test."""
        self.spider = ebird_spider.EBirdSpider(
            region='REG', duration=10, directory='.')
        self.requests = list(self.spider.start_requests())

    def test_request_count(self):
        """Verify a single request is generated for the region."""
        self.assertEqual(1, len(self.requests))

    def test_request_url(self):
        """Verify the URL contains the region identifier and duration."""
        expected = self.spider.region_url % ('REG', 10)
        self.assertTrue(self.requests[0].url, expected)

    def test_request_callback(self):
        """Verify the request contains the callback for parsing the region."""
        expected = self.spider.parse_region
        self.assertTrue(self.requests[0].callback, expected)
