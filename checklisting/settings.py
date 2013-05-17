"""Scrapy settings."""

BOT_NAME = 'checklisting'

SPIDER_MODULES = ['checklisting.spiders']
NEWSPIDER_MODULE = 'checklisting.spiders'

LOG_LEVEL = 'DEBUG'
LOG_STDOUT = True

REDIRECT_ENABLED = True
COOKIES_ENABLED = True

DOWNLOAD_DELAY = 1
