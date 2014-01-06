"""
validate_ebird_crawler.py

This script is used to validate the crawler used to download checklists from
the eBird API and checklist web pages. Once the crawler has finished the suite
of tests in the module checklisting.tests.sites is executed to verify that all
the information is extracted correctly.

To run the tests on the checklists downloaded by the WorldBirds crawler run
the script as follows:

    python validate_ebird_crawler.py <region>

where,

    <region> is eBird region code for a given area, e.g. PT-11

"""

import json
import nose
import shutil
import sys
import tempfile

from scrapy.settings import CrawlerSettings

from checklisting import settings
from checklisting.spiders.ebird_spider import EBirdSpider
from checklisting.tests.utils import RunCrawler
from checklisting.utils import list_files

from checklisting.tests.validation import checklists


settings.DOWNLOAD_DIR = tempfile.mkdtemp()
settings.REPORT_RECIPIENTS = ''

region = sys.argv[1]

spider = EBirdSpider(region=region)
RunCrawler(CrawlerSettings(settings)).crawl(spider)

for path in list_files(settings.DOWNLOAD_DIR, 'json'):
    with open(path, 'rb') as fp:
        checklists.append(json.load(fp))

nose.run(argv=['checklisting.tests.validation'])

shutil.rmtree(settings.DOWNLOAD_DIR)
