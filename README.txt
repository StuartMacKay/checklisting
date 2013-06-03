Checklisting is a set of web crawlers for downloading checklists from
third-party databases.

Crawlers available:

   ebird       Download recently submitted checklists from http://ebird.org
               for a given region.

   worldbirds  Download recently submitted checklists from the network of
               databases hosted by WorldBirds (BirdLife International).


eBird
-----
The crawler for eBird uses the official API:

    https://confluence.cornell.edu/display/CLOISAPI/eBird+API+1.1

and, optionally, scrapes data from the web page that displays the checklist on
the eBird site, e.g. http://ebird.org/ebird/view/checklist?subID=S13500933
since information such as the checklist protocol and breakdowns of counts by
age and sex are not currently available through the API.

The crawler is run using the crawl command-line tool:

    scrapy crawl ebird -a region=PT-11

where,

    region  the region code used by Cornell to identify all the different
            regions supported by the database, e.g. PT-11.

A full list of region codes can be found in "Uploading Data to eBird",
http://help.ebird.org/customer/portal/articles/973915-uploading-data-to-ebird#supplemental-documents

In addition, three settings also control the behaviour of the crawler:

    EBIRD_DOWNLOAD_DIR: the directory where the downloaded checklists will be
    written in JSON format. The value defined in the settings uses the
    temporary used by python but it can be set to any path. Filenames use the
    name of the source and the checklist identifier so running the crawler
    multiple times will overwrite any existing files but will not destroy any
    data.

    EBIRD_DURATION: the number of days to fetch checklists for. The value
    defined in the settings is 7 however eBird allows checklists to be fetched
    for up to the previous 30 days.

    EBIRD_INCLUDE_HTML: not all the useful data for a checklist is available
    through the API. If this setting is True (the default) then the crawler
    will also parse the checklist's web page.

These settings can be changed by either editing checklisting/settings.py or
changing the settings when the crawler is run. For example:

    scrapy crawl ebird -a region=PT-11 -s EBIRD_DURATION=30


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


Install
-------

Checklisting is available from PyPI so you can install it using pip

    pip install checklisting

To run the crawlers you have to tell scrapy which settings to use. This is
done using the SCRAPY_SETTINGS_MODULE environment variable (currently you 
cannot specify the settings file as part of the scrapy command). For 
example a bash shell use:

    export SCRAPY_SETTINGS_MODULE=checklisting.settings

    scrapy crawl ebird -a region=PT-11

There's no simple way to override the settings with a local_settings.py but 
all the settings can be overridden from the command line with the -s option:

    scrapy crawl ebird -a region=PT-11 -s EBIRD_DOWNLOAD_DIR=.
