.. checklisting documentation master file, created by
   sphinx-quickstart on Thu Jul  4 08:53:46 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to checklisting's documentation!
========================================
Checklisting is a series of crawlers that can be used to download records from
various on-line databases available for recording bird observations. While the
databases allow records to be exported the crawlers are designed to create
feeds containing the most recently added checklists. The crawlers all use the
same :doc:`format <format>` for the downloaded data so the aggregated data
can easily be analyzed. Crawlers are available for the following  databases:

.. toctree::
   :maxdepth: 1

   spiders/ebird
   spiders/worldbirds

.. include:: install.rst

Crawling
--------
The crawlers are run using the scrapy crawl command. The first step is to
tell scrapy which settings file to use. This can be done either using an
environment variable, SCRAPY_SETTINGS_MODULE or creating a simple config file
for scrapy::

    export SCRAPY_SETTINGS_MODULE=checklisting.settings

An example config file, which can be found in the root directory of the package,
specifies the settings file using the following directive::

    [settings]
    default = checklisting.settings

The arguments passed the crawlers on the command line specify value such as
which region to download observations from and login details for crawlers
that need an account to access the data::

    scrapy crawl ebird -a region=PT-11

See the docs for each crawler to get a list of the command line arguments and
settings.

Resources
---------

* The checklisting project on `Github <http://github.com/StuartMacKay/checklisting/>`_
* Information on the `Scrapy framework <http://scrapy.org>`_
