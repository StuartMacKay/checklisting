=======
Install
=======

Checklisting is available from PyPI so you can install it using pip::

    pip install checklisting

However this uses the default settings so you will have to override them on
the command-line when you run the crawlers::

    scrapy crawl ebird -a region=PT-11 -s CHECKLISTING_DOWNLOAD_DIR=.

This works if you only have a couple of changes that take a single value
however for settings such as CHECKLISTING_STATUS_REPORT_RECIPIENTS (which
defines the list of email addresses that status reports are sent to) the
settings must be edited or more specifically you create a local_settings.py
file which is used to override the default settings. The process is quite
simple.

1. First install the dependencies (scrapy)::

   pip install scrapy

2. Next download and unpack the package::

       pip install --no-deps --no-install checklisting

   If you are using a virtualenv then the package can be found relative to the
   environment's root directory: "<virtualenv-root>/build/checklisting"
   otherwise it will either be downloaded to a sub-directory of the main temp
   directory, "<OS temp dir>/pip-build-<username>" or to the current directory.

   You can download the package to any directory of your choosing using::

       pip install -d <dir> checklisting

   then unpack the package using::

       tar zxvf checklisting-<version>.tar.gz


3. Now edit the file local_settings.py in the root directory of the package to
   specify the mail server and addresses to use for sending out status reports
   when a crawler completes downloading checklists from a given source.

   There are other settings in checklisting/settings.py which you can override
   in the local settings files but these should all have sane defaults.

   Save the edited local_settings.py to the checklisting sub-directory (where
   the settings.py file is located).

4. Finally build and install the package::

    python setup.py install


Scrapyd
-------
To install the crawlers in a scrapy daemon, repeat the previous steps but omit
the final install (Step 4). Instead edit the scrapy config file, scrapy.cfg in
the package directory and in the [deploy] section change 'url' to the URL of
your scrapy server. You can then deploy the crawlers using::

    scrapy deploy

For more information on installing and managing a scrapyd server please see
the docs at http://scrapyd.readthedocs.org/en/latest/.
