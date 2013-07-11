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

1. First install the dependencies::

       pip install scrapy

2. Next download and unpack the package::

       pip install --no-deps --no-install checklisting

   If you are using a virtualenv then the package can be found relative to the
   environment's root directory: "<virtualenv-root>/build/checklisting"
   otherwise it will either be downloaded to a sub-directory of the main temp
   directory, "<OS temp dir>/pip-build-<username>" or to the current directory.

   Alternatively, you can download the package to any directory of your
   choosing using::

       pip install -d <dir> checklisting

   then unpack the package using::

       tar zxvf checklisting-<version>.tar.gz

3. Configure the crawlers by editing the file, local_settings.py, found in the
   root directory of the project and saving it to the checklisting sub-directory
   where the main settings file, settings.py is located, e.g::

       .../build/checklisting/checklisting/local_settings.py

   Most of the settings have sensible defaults, for example, download
   observations for the past seven days, so the only settings that need to be
   defined are those that specify the mail server and the email addresses that
   are sent out when a crawler completes downloading observations from a given
   source. This status report contains details of any errors or warnings and so
   it's important to check it to see whether there are possible issues when
   loading the checklists into a database.

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
