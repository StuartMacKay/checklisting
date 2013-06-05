=======
Install
=======

Checklisting is available from PyPI so you can install it using pip::

    pip install checklisting

However this uses the default settings so you will have to override them on
the command-line when you run the crawlers::

    scrapy crawl ebird -a region=PT-11 -s EBIRD_DOWNLOAD_DIR=.

This works if you only have a couple of changes that take a single value
however for settings such as CHECKLISTING_STATUS_REPORT_RECIPIENTS (which
defines the list of email addresses that status reports are sent to) the
settings must be edited or more specifically you create a local_settings.py
file which is used to override the default settings. The process is quite
simple.

1. First install the dependencies (scrapy)

       pip install scrapy

2. Next download and unpack the package::

       pip install --no-deps --no-install checklisting

3. Now edit the local settings to suit your configuration and save it to the
   checklisting module (where the settings.py file is located)::

       cd <virtualenv>/build/checklisting
       nano local_settings.py

4. Finally build and install the package::

       python setup.py install

Note: this assumes you are installing the package in a virtualenv. If you are
installing in the global environment then the only difference is the directory
where pip downloads an unpacks the package, which be in main tmp directory,
"<OS temp dir>/pip-build-<username>". You can download the package to any
directory of your choosing using::

    pip install -d <dir> checklisting

then unpack the package using::

    tar zxvf checklisting-<version>.tar.gz

and proceed from step 3, above.

Scrapyd
-------
To install the crawlers in a scrapy daemon, repeat the previous steps but omit
the final install (Step 4). Instead edit the scrapy config file, scrapy.cfg in
the package directory and in the [deploy] section change 'url' to the URL of
your scrapy server. You can then deploy the crawlers using::

    scrapy deploy

For more information on installing and managing a scrapyd server please see
the docs at http://scrapyd.readthedocs.org/en/latest/.
