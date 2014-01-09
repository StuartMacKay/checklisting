
============
Checklisting
============
Checklisting is a set of web crawlers for downloading records from
on-line databases of observations of birds. Crawlers are available for:

:ebird:
    a database hosted by the Laboratory for Ornithology at Cornell University,
    covering the Americas, Oceania and an increasing number of records for
    European countries.

:worldbirds:
    a network of databases hosted by WorldBirds (BirdLife International),
    with good coverage of countries around the Mediterranean and Africa.

The crawlers download only recently submitted records and so must be run on
a regular basis. They are intended to provide a continuous update of records
and so are ideal for mirroring subsets of the records available (for a given
region for example) so you don't have to repeatedly run reports or submit
requests for data.  

So, what is this for?
---------------------
Checklisting was written to aggregate records from different databases for 
publishing in the `Birding Lisboa <http://www.birdinglisoa.com/>`_ news 
service which covers the area around the Tejo estuary, Portugal. All the 
downloaded checklists are loaded into a database which is used to publish
the latest news as well as generate annual reports. 

There are no restrictions on the geographical area that can be covered, though
obviously, the work of managing the database increases, particularly when 
publishing news of recent observations.
 
A similar database could be used for any purpose - analysing observations 
for conservation, environmental management or education. Aggregating the
observations with the crawlers makes this task a lot easier. 

Related projects
----------------
`Django-checklists <http://github.com/StuartMacKay/django-checklists>`_ is 
a database system writen in python that can be used to load the observations
downloaded by the crawlers. It is the database that was used for Birding 
Lisboa. It has an administration application that can be used to manage the
database and an Application Programming Interface (API) that makes it easy 
to extract the data for analysis or publishing.

Installing & Configuring
------------------------
Checklisting is available from PyPI. You can install it with pip or
easy_install::

    pip install checklisting

The crawlers are built using the scrapy engine which uses settings, in the same
way as Django, for configuration and runtime values. The checklisting settings
file is configured to initialize its values from environment variables. That
makes it easy to configure the crawlers, particularly for the most common
use-case, running them from a scheduler such as cron. The only required setting
is to tell scrapy (the engine used by the crawlers) the path to the settings
module::

    export SCRAPY_SETTINGS_MODULE=checklisting.settings

The remaining settings have sensible defaults so only those that are
installation dependent, such as the mail server used for sending out status
reports. Here is this script that is used to run the crawlers for Birding
Lisboa from cron::

    #!/bin/bash

    export SCRAPY_SETTINGS_MODULE=checklisting.settings

    export CHECKLISTING_LOG_LEVEL=INFO

    export CHECKLISTING_DOWNLOAD_DIR=/tmp/birdinglisboa

    export CHECKLISTING_MAIL_FROM=crawlers@birdinglisboa.com
    export CHECKLISTING_MAIL_HOST=mail.example.com
    export CHECKLISTING_MAIL_USER=<user>
    export CHECKLISTING_MAIL_PASS=<password>

    export CHECKLISTING_REPORT_RECIPIENTS=admins@birdinglisboa.com

    source /home/birdinglisboa/venv/bin/activate
    cd /home/birdinglisboa

    scrapy crawl ebird -a region=PT-11
    scrapy crawl ebird -a region=PT-15

The settings can also be defined when the crawlers are run using the -S
option::

    scrapy crawl ebird -a region=PT-15 -s LOG_LEVEL=DEBUG

However this obvious becomes a little cumbersome if more than one or two
settings are involved.

Note that the environment variables use a prefix "CHECKLISTING" as a namespace
to avoid interfering with any other variables. When the setting is defined
using the -s option when running the crawlers, this prefix must be dropped.

Everything is now ready to run.

Crawling
--------
The arguments passed the crawlers on the command line specify value such as
which region to download observations from and login details for crawlers 
that need an account to access the data::

    scrapy crawl ebird -a region=PT-11

    scrapy crawl worldbirds -a username=<user> -a password=<pass> -a country=uk

See the docs for each spider to get a list of the command line arguments and
settings.

If you have defined the settings for a mail server and the setting
CHECKLISTING_REPORT_RECIPIENTS then a status report will be sent out each time
the crawlers are run. The report contains a list of the checklist downloaded
along with an errors (complete with stack traces) and any warnings::

    Spider: ebird
    Date: 03 Jan 2014
    Time: 11:00

    -------------------------
      Checklists downloaded
    -------------------------
    2013-12-27 09:59, Jardim Botanico da Universidade de Lisboa
    2013-12-28 10:20, Baia Cascais
    2013-12-28 13:31, PN Sintra-Cascais--Cabo da Roca
    2013-12-29 07:45, RN Estuario do Tejo--Vala da Saragossa

    ----------
      Errors
    ----------
    URL: http://ebird.org/ebird/view/checklist?subID=S161101101
    Traceback (most recent call last):
      File "/home/birdinglisboa/venv/local/lib/python2.7/site-packages/twisted/internet/base.py", line 1201, in mainLoop
        self.runUntilCurrent()
      File "/home/birdinglisboa/venv/local/lib/python2.7/site-packages/twisted/internet/base.py", line 824, in runUntilCurrent
        call.func(*call.args, **call.kw)
      File "/home/birdinglisboa/venv/local/lib/python2.7/site-packages/twisted/internet/defer.py", line 382, in callback
        self._startRunCallbacks(result)
      File "/home/birdinglisboa/venv/local/lib/python2.7/site-packages/twisted/internet/defer.py", line 490, in _startRunCallbacks
        self._runCallbacks()
    --- <exception caught here> ---
      File "/home/birdinglisboa/venv/local/lib/python2.7/site-packages/twisted/internet/defer.py", line 577, in _runCallbacks
        current.result = callback(current.result, *args, **kw)
      File "/home/birdinglisboa/venv/local/lib/python2.7/site-packages/checklisting/spiders/ebird_spider.py", line 585, in parse_checklist
        checklist = self.merge_checklists(original, update)
      File "/home/birdinglisboa/venv/local/lib/python2.7/site-packages/checklisting/spiders/ebird_spider.py", line 602, in merge_checklists
        original['entries'], update['entries'])
      File "/home/birdinglisboa/venv/local/lib/python2.7/site-packages/checklisting/spiders/ebird_spider.py", line 695, in merge_entries
        if count in key[index]:
    exceptions.TypeError: string indices must be integers

    ------------
      Warnings
    ------------
    2014-01-01 11:55, Parque da Paz
    API: http://ebird.org/ws1.1/data/obs/loc/recent?r=L1127099&detail=full&back=7&includeProvisional=true&fmt=json
    URL: http://ebird.org/ebird/view/checklist?subID=S16160707
    Could not update record from API. There are 2 records that match: species=White Wagtail; count=4.

Checklists downloaded also included the name of the observer, which was removed
here for obvious reasons. The stack traces in the Errors section is useful if
there is a bug but it is also a first indication that the format of the
information being scraped has changed. In either case report it as an issue and
it will get fixed.

Warnings are generally informative. Here a warning is generated because the
checklist contained two equal counts for White Wagtail in the API records -
only the species is reported information on subspecies is dropped. However
the subspecies is reported on the checklist web page. That means when the web
page was scraped it was not possible to distinguish between the two records.
The records should be edited to add any useful information such as comments,
which are only available from the web page.
