=======
Install
=======

Checklisting is available from PyPI so you can install it using pip::

    pip install checklisting

Once installed the first step is to configure the runtime environment for
the scrapy engine and the crawlers. Rather than creating configuration files
or editing the package settings this is done using environment variables
which makes it easier to deploy the package and to customize the environment
each time the crawlers are run.

First tell the scrapy engine where to find the package settings, e.g. using
the bash shell::

    export SCRAPY_SETTINGS_MODULE=checklisting.settings

The settings file then in turn loads the values used to configure the crawlers
from the set of environment variables described here. (The settings for the
scrapy engine can also be defined in a config file which should be placed
the in the directory from where the crawlers are run. An example is included
in the project).

Next define the variables common to all the crawlers:

    CHECKLISTING_DOWNLOAD_DIR: the directory where the crawlers will download
    the checklists to. Filenames use the name of the source and the checklist
    identifier so running the crawler multiple times will overwrite any
    existing files but will not destroy any data. If this variable is not
    set then the checklists will be downloaded to the current directory when
    the crawlers are run.

    CHECKLISTING_DURATION: Download checklists for the previous <n> days. If
    this is not set then checklists will be downloaded for the previous 7 days.

    CHECKLISTING_REPORT_RECIPIENTS: When each crawler is run a status report
    is generated listing the checklists that were downloaded along with any
    errors or warnings encountered. This variable contains a comma-separated
    list of email addresses that the report will be sent to. If this is not
    set then the default value is an empty list and no reports will be sent.

If status reports are being sent out then the following variables must also
be defined:

    CHECKLISTING_MAIL_HOST: the name of the SMTP server used to send the
    status reports.

    CHECKLISTING_MAIL_PORT: the port number for the SMTP server. If not set
    then the default port number is 25.

    CHECKLISTING_MAIL_USER: the username of the account on the mail server.

    CHECKLISTING_MAIL_PASS: the password for the account on the mail server.

    CHECKLISTING_MAIL_FROM: the from address used to indicate who sent the
    status report. If not defined then an empty string is used however it is
    likely that the SMTP server will require this to be set to either the
    accounts main email address or at least to a domain known to the server
    in order to avoid having the email classified as SPAM.

Logging is handled by:

    CHECKLISTING_LOG_LEVEL: The level at which messages are logged, either
    'CRITICAL', 'ERROR', 'WARNING', 'INFO' or 'DEBUG'. If the variable is not
    set then a default value of 'INFO' is used. The level can also be set on
    the command line when the crawler is run using the --loglevel or -L option.

    CHECKLISTING_LOG_FILE: The path to the file where the log messages are
    written. If the variable is not set a default path of 'checklisting.log'
    is used and the file will be written to the directory from where the
    crawlers are run. This can also be set when the crawler is run using the
    --logfile command line option.

Next are the variables used to configure the individual crawlers. Currently
only the eBird crawler has a specific configuration parameter:

    EBIRD_INCLUDE_HTML: whether checklists downloaded from eBird should also
    scrape data from the checklist web page. The eBird API provides basic
    information for each observation however the checklist web page also has
    information on subspecies, the names of observers, any comments, etc.
