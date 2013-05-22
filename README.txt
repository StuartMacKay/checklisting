Checklisting is a set of web crawlers for downloading checklists from
third-party databases.

Crawlers available:

   ebird      Download recently submitted checklists from http://ebird.org
              for a given region.


The crawler for eBird uses the official API:

    https://confluence.cornell.edu/display/CLOISAPI/eBird+API+1.1

and, optionally, scrapes data from the web page that displays the checklist on
the eBird site, e.g. http://ebird.org/ebird/view/checklist?subID=S13500933
since information such as the checklist protocol and breakdowns of counts by
age and sex are not currently available through the API.

The crawler is run using the crawl command-line tool:

    scrapy crawl ebird -a region=PT-11

where,

    region     the region code used by Cornell to identify all the different
               regions supported by the database, e.g. PT-11.

               A full list of region codes can be found in the Supplemental
               Documents section of the guide, "Uploading Data to eBird",
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
