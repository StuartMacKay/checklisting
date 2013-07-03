"""Local settings over-riding values in checklisting/settings.py.

This is an example file. Copy it to local_settings.py and uncomment the
existing settings or add new ones to override the values in the main settings
file, checklisting/settings.py.
"""

#
# Settings for sending status reports by email
#

# Enable sending of  status reports by email
#SPIDER_STATUS_REPORT_RECIPIENTS = [
#    'user@example.com',
#]

# The email address of the sender
#MAIL_FROM = ''

# The name of the SMTP host used to send the email
#MAIL_HOST = ''

# The port to use on the SMTP host.
#MAIL_PORT = 25

# The username for authenticating with the SMTP host.
#MAIL_USER = ''

# The password for authenticating with the SMTP host.
#MAIL_PASS = ''

# Parameters used the in the suite of tests which runs each crawlers to verify
# the checklists can be downloaded from real sites. Each entry contains the
# name of the spider and a dictionary containing the arguments used to run it.
#CHECKLISTING_SITES_TEST = [
#    ('ebird', {'region': '<code>'}),
#    ('worldbirds', {'username': '<username>', 'password': '<password>', 'country': '<code>'}})
#]
