========
Crawling
========

Downloading the checklists from a database is performed using the scrapy
crawl command::

    scrapy crawl ebird -a region=PT-11

The -a option is used to pass arguments to the crawler, in this case checklists
will be downloaded for eBird region PT-11 (Lisbon, Portugal).

All of the environment variables, used to configure the crawlers, may be
overridden on the command line when the crawlers are run using the -s option::

    scrapy crawl ebird -s DOWNLOAD_DIR=/path/to/dir

Note that the "CHECKLISTING_" prefix from the environment variable name is
dropped.

See the docs for each crawler to get a list of the command line arguments.
