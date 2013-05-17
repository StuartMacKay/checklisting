Checklisting is a set of web crawlers for downloading checklists from
third-party databases.

Crawlers available:

   ebird      Download recently submitted checklists from http://ebird.org
              for a given region.


The crawler for eBird uses the official API:

    https://confluence.cornell.edu/display/CLOISAPI/eBird+API+1.1

and also scrapes data from the web page that displays the checklist on the
eBird site, e.g. http://ebird.org/ebird/view/checklist?subID=S13500933 since
information such as the checklist protocol and breakdowns of counts by age
and sex are not currently available through the API.

The crawler requires three arguments:

    region     the region code used by Cornell to identify all the different
               regions supported by the database, e.g. PT-11

    duration   the number of days to fetch checklists for. eBird allows 
               checklists to be fetched for up to the previous 30 days.
               Checklists for earlier than this are not available through
               the API, instead a request for the data should be submitted
               to eBird.

    directory  the directory where the downloaded checklists will be written.
               Files are written in JSON format.
