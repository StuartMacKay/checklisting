
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
for conservation, environmental managment or education. Aggregating the 
observations with the crawlers makes this task a lot easier. 

Related projects
----------------
`Django-checklists <http://github.com/StuartMacKay/django-checklists>`_ is 
a database system writen in python that can be used to load the observations
downloaded by the crawlers. It is the database that was used for Birding 
Lisboa. It has an administration application that can beused to manage the 
database and an Application Programming Interface (API) that makes it easy 
to extract the data for analysis or publishing.

Installing
----------
Checklisting is available from PyPI. The crawlers typically require some
configuration so the installation is broken down into steps. First the
dependencies are installed::

    pip install scrapy

Next download and unpack the package::

    pip install --no-deps --no-install checklisting

The directory where the package is downloaded will depend on your local 
environment and whether you are using virtualenv. It can be found either in

  * the main temporary directory used by your operating system,
    "<OS temp dir>/pip-build-<username>"
  * a subdirectory of the current directory,
    "./build/checklisting"
  * relative to the root directory of your virtualenv,
    "<virtualenv-root>/build/checklisting.

Configure the crawlers by editing the file, local_settings.py, found in the
root directory of the project and saving it to the checklisting sub-directory
where the main settings file, settings.py is located, e.g::

    .../build/checklisting/checklisting/local_settings.py

Most of the settings have sensible defaults, for example, download observations
for the past seven days, so the only settings that need to be defined are those
that specify the mail server and the email addresses that are sent out when a
crawler completes downloading observations from a given source. This status 
report contains details of any errors or warnings and so it's important to 
check it to see whether there are possible issues when loading the checklists
into a database.

Now build and install the package::

    python setup.py install

Everything is now ready to run.

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

    scrapy crawl worldbirds -a username=<user> -a password=<pass> -a country=uk

See the docs for each spider to get a list of the command line arguments and
settings.

