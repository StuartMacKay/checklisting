"""Extensions for customizing scrapy."""

import datetime
import unicodedata

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
    un-accented equivalents (where possible). However the conversion process
    is relatively simple and not all characters may be changed so the message
    is encoded as UTF-8. Some characters may not display correctly as a result.
    This does not affect the contents of the checklists which are downloaded
    and encoded as UTF-8 strings so all characters are preserved.
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

    def remove_accents(self, input_str):
        nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
        return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

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
                if 'protocol' in checklist:
                    time = checklist['protocol']['time']
                else:
                    time = '--:--'
                summary.append("%s %s, %s (%s)" % (
                    checklist['date'],
                    time,
                    self.remove_accents(checklist['location']['name']),
                    self.remove_accents(checklist['submitted_by'])
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
                if 'protocol' in checklist:
                    time = checklist['protocol']['time']
                else:
                    time = '--:--'
                summary.append("%s %s, %s (%s)" % (
                    checklist['date'],
                    time,
                    self.remove_accents(checklist['location']['name']),
                    self.remove_accents(checklist['submitted_by'])
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
