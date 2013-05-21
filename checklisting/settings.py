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

# The delay between requests in seconds. Keep this number relatively long
# in order to avoid overloading the server or getting banned.
DOWNLOAD_DELAY = 1

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
