"""Tests for initializing and starting the EBirdSpider."""

from unittest import TestCase

from checklisting.spiders import ebird_spider


class StartRequestsTestCase(TestCase):
    """Verify the initial request for the recent observations of a region."""

    def setUp(self):
        """Initialize the test."""
        self.spider = ebird_spider.EBirdSpider('REG')
        self.requests = self.spider.start_requests()

    def test_request_count(self):
        """Verify a single request is generated for the region."""
        self.assertEqual(1, len(self.requests))

    def test_request_url(self):
        """Verify the URL contains the region identifier and duration."""
        expected = self.spider.region_url % ('REG', 7)
        self.assertTrue(self.requests[0].url, expected)

    def test_request_callback(self):
        """Verify the request contains the callback for parsing the region."""
        expected = self.spider.parse_region
        self.assertTrue(self.requests[0].callback, expected)

    def test_duration(self):
        """Verify the number of days to fetch observations for is set."""
        self.assertEqual(7, self.spider.duration)

    def test_directory(self):
        """Verify the directory where checklists are saved is set."""
        self.assertIsNone(self.spider.directory)

    def test_include_html(self):
        """Verify the include_html flag is set."""
        self.assertTrue(self.spider.include_html)
