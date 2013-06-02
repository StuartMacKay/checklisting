"""Integration test verifying spiders download real data."""

from unittest import TestCase

from scrapy.settings import CrawlerSettings
from scrapy.crawler import CrawlerProcess

from multiprocessing import Process

from checklisting import settings
from checklisting.spiders import ebird_spider, worldbirds_spider


class RunCrawler():
    """RunCrawler runs a crawler in a separate process.

    Useful sources:
    https://groups.google.com/forum/?fromgroups#!topic/scrapy-users/8zL8W3SdQBo
    http://stackoverflow.com/questions/13437402/how-to-run-scrapy-from-within-a-python-script
    """
    def __init__(self, settings):
        self.crawler = CrawlerProcess(settings)
        self.crawler.configure()

    def _crawl(self, spider):
        self.crawler.crawl(spider)
        self.crawler.start()
        self.crawler.stop()

    def crawl(self, spider):
        p = Process(target=self._crawl, args=(spider,))
        p.start()
        p.join()


class DownloadsTestCase(TestCase):
    """Verify the spiders work with actual sites.

    The spiders to run are defined in the setting CHECKLISTING_DOWNLOADS_TEST
    which contains a tuple with the name of the spider and a dictionary
    with the arguments used to initialize it.

    The test simply runs the spiders. Any exception raised by the crawler or
    spider will not be caught so the test provides a quick sanity check
    whether everything is working.
    """

    def setUp(self):
        """Initialize the test."""
        # make sure status report emails are not sent
        settings.SPIDER_STATUS_REPORT_RECIPIENTS = []
        self.spiders = {
            'ebird': ebird_spider.EBirdSpider,
            'worldbirds': worldbirds_spider.WorldBirdsSpider,
        }

    def test_downloads(self):
        """Verify the spiders work with actual sites."""
        for values in settings.CHECKLISTING_DOWNLOADS_TEST:
            spider = self.spiders[values[0]](**values[1])
            RunCrawler(CrawlerSettings(settings)).crawl(spider)
