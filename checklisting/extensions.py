"""Extensions for customizing scrapy."""

import datetime

from unidecode import unidecode

from scrapy import log
from scrapy import signals
from scrapy.mail import MailSender


class SpiderStatusReport(object):
    """Email a status report when a spider finishes.

    The report contains a list of the checklists downloaded.

    Reports are sent to the list of email addresses in the setting
    REPORT_RECIPIENTS. Set this to an empty list (the default) in order to
    disable sending the reports.

    The report is is sent as a regular (ASCII) email message and not in MIME
    format. Accented characters are removed by converting them into their
    un-accented equivalents using unidecode.
    """

    template = """Spider: %(spider)s
Date: %(date)s
Time: %(time)s

-------------------------
  Checklists downloaded
-------------------------
%(checklists)s

----------
  Errors
----------
%(errors)s

------------
  Warnings
------------
%(warnings)s

"""

    @classmethod
    def from_crawler(cls, crawler):
        extension = cls()
        crawler.signals.connect(extension.spider_closed,
                                signal=signals.spider_closed)
        return extension

    def spider_closed(self, spider):
        recipients = [recipient.strip() for recipient in
                      spider.settings['REPORT_RECIPIENTS'].split(',')]

        if not recipients:
            spider.log("No recipients listed to receive status report",
                       log.INFO)
            return

        spider.log("Generating status report", log.INFO)

        now = datetime.datetime.today()

        context = {
            'spider': spider.name,
            'date': now.strftime("%d %b %Y"),
            'time': now.strftime("%H:%M"),
            'checklists': 'No checklists downloaded',
            'errors': 'No errors reported',
            'warnings': 'No warnings reported',
        }

        checklists = getattr(spider, 'checklists', [])
        spider.log("%d checklists downloaded" % len(checklists), log.INFO)

        if checklists:
            summary = []
            for checklist in checklists:
                if 'protocol' in checklist and 'time' in checklist['protocol']:
                    time = checklist['protocol']['time']
                else:
                    time = '--:--'
                summary.append("%s %s, %s (%s)" % (
                    checklist['date'],
                    time,
                    unidecode(checklist['location']['name']),
                    unidecode(checklist['source']['submitted_by'])
                ))
            context['checklists'] = '\n'.join(summary).encode('utf-8')

        errors = getattr(spider, 'errors', [])
        spider.log("%d errors reported" % len(errors), log.INFO)

        if errors:
            summary = []
            for url, failure in errors:
                summary.append("URL: %s\n%s\n\n" % (
                    url,
                    failure.getTraceback()
                ))
            context['errors'] = '\n'.join(summary).encode('utf-8')

        warnings = getattr(spider, 'warnings', [])
        spider.log("%d warnings reported" % len(warnings), log.INFO)

        if warnings:
            summary = []

            for checklist, messages in warnings:
                if 'protocol' in checklist and 'time' in checklist['protocol']:
                    time = checklist['protocol']['time']
                else:
                    time = '--:--'
                summary.append("%s %s, %s (%s)" % (
                    checklist['date'],
                    time,
                    unidecode(checklist['location']['name']),
                    unidecode(checklist['source']['submitted_by'])
                ))
                summary.extend(messages)
                summary.append('\n')

            context['warnings'] = '\n'.join(summary).encode('utf-8')

        mailer = MailSender.from_settings(spider.settings)
        mailer.send(
            to=recipients,
            subject="%s Status Report" % spider.name,
            body=self.template % context
        )


class ErrorLogger(object):

    @classmethod
    def from_crawler(cls, crawler):
        extension = cls()
        crawler.signals.connect(extension.spider_error,
                                signal=signals.spider_error)
        return extension

    def spider_error(self, failure, response, spider):
        spider.errors.append((response.url, failure))
