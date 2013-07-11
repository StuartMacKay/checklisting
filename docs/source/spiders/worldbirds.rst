==========
WorldBirds
==========

The crawler for WorldBirds scrapes the web application pages so you need an
account to extract the data. The data is generally available for download but
scraping pages makes it easier to obtain the most recently added checklists.

The crawler is run using the crawl command-line tool::

    scrapy crawl worldbirds -a username=<username> -a password=<password> -a country=<iso code>

The -a option is used by scrapy to pass key-value pairs to the crawler. Three
options are used to run the crawler:

+----------+-------------------------------------------------------------------+
| username | is the username for your WorldBirds account.                      |
+----------+-------------------------------------------------------------------+
| password | is the password for your WorldBirds account.                      |
+----------+-------------------------------------------------------------------+
| country  | is a two-letter country code (ISO 3166) that is used to identify  |
|          | the database to access.                                           |
+----------+-------------------------------------------------------------------+

You will need separate accounts for each geographical region or country you
want to extract data from.

Most of the WorldBirds databases are accessed with a URL that takes the
general form www.worldbirds.org/v3/<country>.php. Exceptions are the databases
for Africa where countries are grouped into regions, e.g. East Africa and those
for Iberia which are hosted at birdlaa5.memset.net/. The country code makes it
easier to specify which database to use.


Settings
========

The following setting also control the behaviour of the crawler:

    CHECKLISTING_DOWNLOAD_DIR: the directory where the downloaded checklists
    will by written in JSON format. The value defined in the settings uses the
    temporary used by python but it can be set to any path. Filenames use the
    name of the source and the checklist identifier so running the crawler
    multiple times will overwrite any existing files but will not destroy any
    data. This also allows the same directory to be used for all crawlers.

    WORLDBIRDS_DURATION: the number of days to fetch checklists for.

Settings can be changed by either editing checklisting/settings.py or changing
the settings when the crawler is run. For example::

    scrapy crawl worldbirds ... -s CHECKLISTING_DOWNLOAD_DIR=.


Supported Databases
===================

The network of databases hosted by WorldBirds covers some 28 geographical
areas and countries. All the databases use the same version of the web
application for access so the crawler should be able to download checklists
from any of them. Databases it has been specifically tested with include:

========   ====  ===
Country    Code  URL
========   ====  ===
Portugal   pt    `<http://birdlaa5.memset.net/worldbirds/portugal.php>`_
========   ====  ===



