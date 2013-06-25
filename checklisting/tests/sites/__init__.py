"""Checklist validation tests.

Verify that the format of the downloaded checklists matches the checklist file
format and so can consistently be loaded into a target database with a
minimum in variation.

The goal of these tests are both checking of the files that the crawlers
generate and notifying any breaking changes to the sites being crawled. The
checks could have been added to the crawlers but the unittest framework
provides a good infrastructure that would have to be duplicated otherwise.
Using tests also provide more flexibility in what to test - it's a lot
easier to add crawler specific tests for example.

Downloading checklists is extremely expensive (relatively) since we don't
want to be hitting servers unnecessarily. Adding module level setup and tear
down functions here ensures that the function are called before and after,
respectively, another test in this module or submodule.
"""
import json
import shutil
import tempfile

from unittest import TestCase

from scrapy.settings import CrawlerSettings

from checklisting import settings
from checklisting.spiders import ebird_spider, worldbirds_spider
from checklisting.tests.utils import RunCrawler
from checklisting.utils import list_files


checklists = []


def setUpModule():
    """Setup the fixtures for all the validation tests."""
    global checklists

    settings.CHECKLISTING_DOWNLOAD_DIR = tempfile.mkdtemp()
    settings.SPIDER_STATUS_REPORT_RECIPIENTS = []

    spiders = {
        'ebird': ebird_spider.EBirdSpider,
        'worldbirds': worldbirds_spider.WorldBirdsSpider,
    }

    for values in settings.CHECKLISTING_SITES_TEST:
        spider = spiders[values[0]](**values[1])
        RunCrawler(CrawlerSettings(settings)).crawl(spider)

    for path in list_files(settings.CHECKLISTING_DOWNLOAD_DIR, 'json'):
        with open(path, 'rb') as fp:
            checklists.append(json.load(fp))


def tearDownModule():
    """Remove the files downloaded by the crawlers."""
    shutil.rmtree(settings.CHECKLISTING_DOWNLOAD_DIR)


class ValidationTestCase(TestCase):
    """A class that provides extra assert methods for validating data."""

    def assertStripped(self, obj, msg=None):
        """Assert that a string does not have leading or trailing whitespace.

        Args:
            obj: The string to check.
            msg: Optional message to use on failure instead.
        """
        self.assertIsInstance(obj, basestring, 'Argument is not a string')

        if len(obj) != len(obj.strip()):
            standardMsg = '%s contains leading or trailing whitespace'
            self.fail(self._formatMessage(msg, standardMsg))

