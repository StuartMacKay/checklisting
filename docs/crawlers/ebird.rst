=====
eBird
=====
eBird has an API which provides access to records submitted to the database for
up to the past 30 days. The records published through the API also include the
checklist identifier which is used to scrape additional data, such as the
protocol used, from the checklist web page.



and, optionally, scrapes data from the web page that displays the checklist on
the eBird site, e.g.
since information such as the checklist protocol and breakdowns of counts by
age and sex are not currently available through the API.

The crawler is run using the crawl command-line tool::

    scrapy crawl ebird -a region=PT-11

The -a option is used by scrapy to pass key-value pairs to the crawler. The
eBird API and websites are public so only the region code, e.g. PT-11 needs to
be passed to the crawler. See the Resources section for links to a full list
of the available region codes.

Settings
========

In addition, three settings also control the behaviour of the crawler:

    CHECKLISTING_DOWNLOAD_DIR: the directory where the downloaded checklists
    will be written in JSON format. The value defined in the settings uses the
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
changing the settings when the crawler is run. For example::

    scrapy crawl ebird -a region=PT-11 -s EBIRD_DURATION=30

Resources
---------

API documentation can be found at https://confluence.cornell.edu/display/CLOISAPI/eBird+API+1.1

An typical checklist web page can be found at http://ebird.org/ebird/view/checklist?subID=S13500933

eBird publishes a full list of region codes in PDF format and as an Excel spreadsheet:

* `State_Country_Codes_10_Nov_2011.pdf <http://help.ebird.org/customer/portal/kb_article_attachments/14685/original.pdf>`_
* `State_Country_Codes_10_Nov_2011.xls <http://help.ebird.org/customer/portal/kb_article_attachments/14684/original.xls>`_
