============
Checklisting
============
Checklisting is a set of web crawlers for downloading checklists from
third-party databases. Crawlers are available for:

:ebird:
    Download recently submitted checklists from http://ebird.org for a given
    region.

:worldbirds:
    Download recently submitted checklists from the network of databases
    hosted by WorldBirds (BirdLife International). See the docs for the
    `Worldbirds crawler <http://www.github.com/StuartMacKay/checklisting/docs/spiders/worldbirds.rst>`_
    for a list of the supported databases.


Installing
----------
Checklisting is available from PyPI. The crawlers typically require some
configuration so the installation is broken down into steps. First the
dependencies are installed::

    pip install scrapy

Next download and unpack the package::

    pip install --no-deps --no-install

Now edit the local settings to suit your configuration and save it to the
checklisting module (where the settings.py file is located)::

    cd <virtualenv>/build/checklisting
    nano local_settings.py

Finally build and install the package::

    python setup.py install


You could simply run 'pip install checklisting' but then you would have to
override any settings on the command line when running the crawlers. You can
also install the crawlers in a scrapy daemon. Both options are discussed in
more detail in the `Install Guide <http://www.github.com/StuartMacKay/checklisting/docs/install.rst>`_.


Crawling
--------
The crawlers are run using the scrapy crawl command. The first step is to
tell scrapy which settings file to use. This can be done either using an
environment variable, SCRAPY_SETTINGS_MODULE or creating a simple config file
for scrapy::

    export SCRAPY_SETTINGS_MODULE=checklisting.settings

While the contents of the config file, scrapy.cfg are::

    [settings]
    default = checklisting.settings

The run-time parameters for the crawlers are passed on the command line, for
example::

    scrapy crawl ebird -a region=PT-11

    scrapy crawl worldbirds -a username=<user> -a password=<pass> -a country=uk

See the docs for each spider to get a list of the command line arguments and
settings.

