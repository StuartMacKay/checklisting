"""Scrapy settings."""

import os
import tempfile


BOT_NAME = 'checklisting'

SPIDER_MODULES = ['checklisting.spiders']
NEWSPIDER_MODULE = 'checklisting.spiders'

LOG_LEVEL = 'INFO'
LOG_STDOUT = True
LOG_FILE = 'eBird.log'

# eBird redirects requests for the checklist web page to do some security
# checks so the redirect middleware needs to be enabled.
REDIRECT_ENABLED = True

COOKIES_ENABLED = True

# The maximum number of simultaneous requests that will be performed by the
# Scrapy downloader.
#
# IMPORTANT: Do not change this value, otherwise the Requests and Responses
# when parsing the eBird checklist web pages get mixed up. Since each eBird
# spider processes the checklists for one region and the number of checklists
# to be downloaded is low (typically a few dozen) then this restriction does
# not adversely affect performance.
CONCURRENT_REQUESTS = 1

#
# Settings for the eBird spider.
#

# Set the directory where the downloaded checklists will be written. Here
# checklists are written to python's tmp directory, but any path can be used.
# It will be created if it does not exist.
EBIRD_DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), 'ebird')

# Get the observations from the eBird API from the last <n> days. A value of
# 7 (one week) offers a reasonable trade-off between only fetching recent data
# while still catching checklists that are added late.
EBIRD_DURATION = 7

# Whether the checklist web page is also parsed to extract data (True) or
# only the data from the API is used (False).
EBIRD_INCLUDE_HTML = True
