"""Scrapy settings."""

import os
import tempfile


BOT_NAME = 'checklisting'

SPIDER_MODULES = ['checklisting.spiders']
NEWSPIDER_MODULE = 'checklisting.spiders'

LOG_LEVEL = 'INFO'
LOG_STDOUT = True
LOG_FILE = 'checklisting.log'

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

EXTENSIONS = {
    'checklisting.extensions.SpiderStatusReport': 600,
    'checklisting.extensions.ErrorLogger': 600,
}

# Define a shared directory for crawler downloads. The crawlers use the name
# of the source in file names so checklists from different sources will not
# overwrite each other. Here checklists are written to python's tmp directory,
# but any path can be used. It will be created if it does not exist.
CHECKLISTING_DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), 'checklisting')

# The list of email addresses where status reports are sent. Be sure to also
# set the values for the SMTP server used to send the email message.
CHECKLISTING_STATUS_REPORT_RECIPIENTS = []


#
# Settings for the eBird spider.
#

# Get the observations from the eBird API from the last <n> days. A value of
# 7 (one week) offers a reasonable trade-off between only fetching recent data
# while still catching checklists that are added late.
EBIRD_DURATION = 7

# Whether the checklist web page is also parsed to extract data (True) or
# only the data from the API is used (False).
EBIRD_INCLUDE_HTML = True

#
# Settings for the WorldBirds spider.
#

# Get the checklists for the last <n> days, including today. A value of 7
# (one week) offers a reasonable trade-off between only fetching recent data
# while still catching checklists that are added late.
WORLDBIRDS_DURATION = 7

#
# Settings for tests
#

# A list of the spiders and arguments used to initialize them that are used
# in the sites tests to verify the crawlers are working and the data are being
# parsed correctly to create the checklists. See the file, local_settings.py
# in the root project directory for more details.
CHECKLISTING_SITES_TEST = []

#
# Override settings with local values
#

try:
    from checklisting.local_settings import *
except ImportError:
    pass
