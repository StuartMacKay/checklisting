WorldBirds
----------
The crawler for WorldBirds scrapes the web application pages so you need an
account to extract the data. The data is generally available for download but
scraping pages makes it easier to obtain the most recently added checklists.

The crawler is run using the crawl command-line tool:

    scrapy crawl worldbirds -a username=<username> -a password=<password> -a country=<iso code>

where,

    username  is the username for your WorldBirds acccount - you will need
              separate accounts for each country you want to extract data from.

    password  is the password for your WorldBirds account.

    country   is a two-letter country code (ISO 3166) that is used to identify
              the URL of the database to access.

Worldbirds uses different URLs for the countries it supports for example the
databases for Iberia are hosted at http://birdlaa5.memset.net/ while others
(all?) are hosted at http://www.worldbirds.org/. The country code makes it
easier to specify which database to use and makes it easier to show which
databases the crawler has been tested with.

Supported country codes:

    pt    Portugal Aves, http://birdlaa5.memset.net/worldbirds/portugal.php


The following setting also control the behaviour of the crawler:

    WORLDBIRDS_DOWNLOAD_DIR: the directory where the downloaded checklists will
    by written in JSON format. The value defined in the settings uses the
    temporary used by python but it can be set to any path. Filenames use the
    name of the source and the checklist identifier so running the crawler
    multiple times will overwrite any existing files but will not destroy any
    data. This also allows the same directory to be used for all crawlers.

    WORLDBIRDS_DURATION: the number of days to fetch checklists for.

Settings can be changed by either editing checklisting/settings.py or changing
the settings when the crawler is run. For example:

    scrapy crawl worldbirds ... -s WORLDBIRDS_DOWNLOAD_DIR=.


