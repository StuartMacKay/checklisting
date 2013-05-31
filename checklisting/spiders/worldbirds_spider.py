"""A crawler downloading checklists from Worldbirds.

This crawler creates checklists for checklists added to the WorldBirds database
from BirdLife International.
"""

import os
import re

from datetime import datetime, timedelta

from scrapy.http import Request, FormRequest
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from checklisting.exceptions import LoginException
from checklisting.spiders.utils import save_json_data


class VisitParser(object):

    """Parser for the Visit Highlights on the Latest News page."""

    def __init__(self, response):
        """Initialize the parser the contents of the Latest News page.

        Args:
            response (Response): the response from the crawler containing the
                contents of the Latest News page.

        Returns:
            VisitParser: a VisitParser object
        """
        self.docroot = HtmlXPathSelector(response)

    def get_checklists(self):
        """Get the checklist identifiers.

        Returns:
            list: a list containing the identifiers for the checklists
                extracted from the Visit Highlights table.
        """
        xpath = '(//table[@class="StandardTable"])[1]/tr/td/' \
                'a[starts-with(@onclick, "doHighlights")]/@onclick'
        return  [int(attr.split(',')[1].strip())
                 for attr in self.docroot.select(xpath).extract()]

    def get_locations(self):
        """Get the location identifiers.

        Returns:
            list: a list containing the identifiers for the locations
                extracted from the Visit Highlights table.
        """
        xpath = '(//table[@class="StandardTable"])[1]/tr/td/' \
                'a[starts-with(@onclick, "doLocation")]/@onclick'
        return [int(re.search(r"\(([0-9]+)\)", val).group(1))
                for val in self.docroot.select(xpath).extract()]

    def get_observers(self):
        """Get the identifiers for the observers.

        Returns:
            list: a list containing the identifiers for the observers who
                submitted the checklists in the Visit Highlights table.
        """
        xpath = '(//table[@class="StandardTable"])[1]/tr/td/' \
                'a[starts-with(@onclick, "doObserver")]/@onclick'
        return [int(re.search(r"\(([0-9]+)\)", val).group(1))
                for val in self.docroot.select(xpath).extract()]

    def get_dates(self):
        """Get the checklist dates.

        Returns:
            list: a list containing the dates for each of the checklists.
        """
        xpath = '(//table[@class="StandardTable"])[1]/tr/td/text()'
        values = [datetime.strptime(val, "%d/%m/%Y")
                  for val in self.docroot.select(xpath).extract()
                  if re.search(r"\d{2}/\d{2}/\d{4}", val)]
        return values

    def get_visits(self):
        """Get the values for the visits.

        Returns:
            list(tuple): a list containing tuples of the visit date and
                checklist, location and observer identifiers respectively.
        """
        return zip(self.get_dates(), self.get_checklists(),
                   self.get_locations(), self.get_observers())


class ChecklistParser(object):

    """Extract the checklist from the popup containing the visit details."""

    def __init__(self, response):
        """Initialize the parser with a JSON encoded response.

        Args:
            response (Response): the response from the crawler containing the
                contents of the popup panel displaying the checklist.

        Returns:
            ChecklistParser: a ChecklistParser object that extracts the
                checklist from the data.
        """
        self.docroot = HtmlXPathSelector(response)
        self.identifier = response.meta['identifiers'][0]
        self.url = response.url

    def get_checklist(self):
        """Get the checklist.

        Returns:
            dict: a dictionary containing the checklist fields.
        """
        xpath = '(//table[@class="PopupTable"])[1]/tr/td/text()'
        rows = self.docroot.select(xpath).extract()

        day, month, year = rows[2].strip().split('-')
        hour, minute = rows[3].split('-')[0].strip().split(':')

        return {
            'identifier': self.identifier,
            'source': 'WorldBirds',
            'url': self.url,
            'date': "%s-%s-%s" % (year, month, day),
            'time': "%s:%s" % (hour, minute),
            'location': self.get_location(),
            'protocol': self.get_protocol(),
            'observers': [name.strip() for name in rows[-2].split(',')],
            'observer_count': int(rows[5].strip()),
            'entries': self.get_entries()
        }

    def get_location(self):
        """Get the location.

        Returns:
            dict: a dictionary containing the fields for a location.
        """
        xpath = '(//table[@class="PopupTable"])[1]/tr/td/text()'
        rows = self.docroot.select(xpath).extract()
        return {
            'name': rows[0].strip(),
        }

    def get_protocol(self):
        """Get the protocol.

        Checklists from WorldBirds do not have a specific protocol defined,
        only the time spent in the field, so a timed visit protocol is used.

        Returns:
            dict: a dictionary containing the fields for a protocol.
        """
        xpath = '(//table[@class="PopupTable"])[1]/tr/td/text()'
        rows = self.docroot.select(xpath).extract()
        start_hour, start_minute = rows[3].split('-')[0].strip().split(':')
        start_time = int(start_hour) * 60 + int(start_minute)
        end_hour, end_minute = rows[3].split('-')[1].strip().split(':')
        end_time = int(end_hour) * 60 + int(end_minute)

        return {
            'type': 'TIM',
            'duration_hours': (end_time - start_time) / 60,
            'duration_minutes': (end_time - start_time) % 60,
        }

    def get_entries(self):
        """Get the list of entries containing the counts for each species.

        Checklists may contain multiple entries for a given species. This is
        useful in situations such as sea-watching where counts are made using
        a fixed interval, e.g. every 10 minutes, over the course of the visit.

        Returns:
            list(dict): a list containing the dictionaries for each entry in
                the checklist.
       """
        xpath = '(//table[@class="TableThin"])[1]/tr'
        rows = self.docroot.select(xpath)[1:]
        entries = []
        for idx, row in enumerate(rows):
            entry = self.get_entry(row)
            entry['identifier'] = str(self.identifier * 1000 + idx)
            entries.append(entry)
        return entries

    def get_entry(self, row):
        """Get the entry for a given row.

        Args:
            row (XPathSelector): a node for the row in the table that contains
                the details of each species recorded.

        Returns:
            dict: a dictionary containing the fields for a checklist entry.
        """
        columns = row.select('./td/text()').extract()

        # If a species was not counted then the checklist displays an image
        # so when the text contents of the table cells are extracts no data
        # is returned.

        if len(columns) == 4:
            count = '0'
        else:
            count = columns[1].strip()

        return {
            'identifier': '',
            'species': self.get_species(row),
            'count': count,
            'comment': columns[3].strip(),
        }

    def get_species(self, row):
        """Get the species for a given row.

        Args:
            row (XPathSelector): a node for the row in the table that contains
                the species name.

        Returns:
            dict: a dictionary containing the fields for a species.

        The species is extracted in a method purely for aesthetic reasons - so
        that each level in the checklist data structure is handled by different
        methods. It could easily be merged into the get_entry() method.
        """
        columns = row.select('./td/text()').extract()
        return {
            'standard_name': columns[0].strip(),
        }


class LocationParser(object):

    """Extract the location from the popup containing the location details."""

    def __init__(self, response):
        """Initialize the parser the contents of the popup panel.

        Args:
            response (Response): the response from the crawler containing the
                contents of the location popup.

        Returns:
            LocationParser: a LocationParser object
        """
        self.docroot = HtmlXPathSelector(response)
        self.checklist = response.meta['checklist']

    def get_checklist(self):
        """Get the checklist updated with the location details.

        Returns:
            dict: the dict containing the checklist data.
        """
        xpath = '(//table[@class="PopupTable"])[1]/tr/td/text()'
        rows = self.docroot.select(xpath).extract()
        location = self.checklist['location']
        location['country'] = rows[1].strip()
        location['comment'] = rows[5].strip()
        location['lat'] = rows[2].split(',')[0].strip()
        location['lng'] = rows[2].split(',')[1].strip()
        return self.checklist


class ObserverParser(object):

    """Extract the observer from the popup containing the observer details."""

    def __init__(self, response):
        """Initialize the parser the contents of the popup panel.

        Args:
            response (Response): the response from the crawler containing the
                contents of the location popup.

        Returns:
            ObserverParser: a ObserverParser object
        """
        self.docroot = HtmlXPathSelector(response)
        self.checklist = response.meta['checklist']

    def get_checklist(self):
        """Get the checklist updated with the observer details.

        Returns:
            dict: the dict containing the checklist data.
        """
        xpath = '(//table[@class="PopupTable"])[1]/tr/td/text()'
        rows = self.docroot.select(xpath).extract()
        self.checklist['submitted_by'] = rows[1].strip()
        return self.checklist


class WorldBirdsSpider(BaseSpider):
    """Extract checklists recently added to WorldBirds.

    The spider starts logging on to the web application for one of the
    countries that WorldBirds supports. The recently added checklists are
    displayed in the Visit Highlights table on the Latest News page. The table
    containing the checklists is paged with 10 visits per page. The displayed
    page is controlled by a form hidden on the page. Each of the entries in the
    table contains the identifiers (possibly a database id) for the checklist,
    location and observer. These are extracted and used to call an undocumented
    URL that is used to display the checklist, location and observer details in
    separate popup panels. From this all the information for the checklist can
    be extracted.

    The WorldBirds databases cannot be browsed. You need to signup for an
    account in order to be able to access the data. There is a reports page
    from where you can download data but it does not appear to be easily
    crawlable so scraping the Latest News page has proved to be the most
    effective approach.

    Worldbirds uses different URLs for the countries it supports for example
    the databases for Iberia are hosted at http://birdlaa5.memset.net/ while
    others (all?) are hosted at http://www.worldbirds.org/. The database to
    access is specified by a two letter (ISO 3166-1) country code, e.g. 'us',
    'uk', 'es', etc.

    Note: the WorldBirds page http://www.worldbirds.org/mapportal/worldmap.php
    gives URLs for databases in most countries but not all of them are part
    of WorldBirds. Most of the entries for the Americas are for eBird.

    The following settings control the behaviour of the spider:

    WORLDBIRDS_DOWNLOAD_DIR: the directory where the downloaded checklists
    will be written in JSON format. The directory will be created if it does
    not exist.

    WORLDBIRDS_DURATION: the number of days to fetch checklists for.

    The spider keeps a list of checklists downloaded and save along with any
    errors raised. These are used to create a status report by the extension,
    SpiderStatusReport which is emailed out when the spider finishes.
    """

    name = "worldbirds"
    allowed_domains = ["birdlaa5.memset.net", 'worldbirds.org']

    visit_parser = VisitParser
    checklist_parser = ChecklistParser
    location_parser = LocationParser
    observer_parser = ObserverParser

    databases = {
        'pt': 'http://birdlaa5.memset.net/worldbirds/portugal.php'
    }

    def __init__(self, username, password, country, **kwargs):
        """Initialize the spider.

        Args:
            username (str): the username of the WorldBirds account used to
                log in to the application.
            password (str): the password of the WorldBirds account used to
                log in to the application.
            country (str): the country code for the WorldBirds database.

        Returns:
            WorldBirdsSpider: a Scrapy crawler object.
        """
        super(WorldBirdsSpider, self).__init__(**kwargs)
        if not username:
            raise ValueError("You must give a username to login.")
        self.username = username
        if not password:
            raise ValueError("You must give a password to login.")
        self.password = password
        if not country:
            raise ValueError("You must give the country code for a database.")
        if country.lower() not in self.databases:
            raise ValueError("Sorry, %s is one of the countries that is not"
                             " (yet) supported by this crawler.")
        self.start_url = self.databases[country.lower()]
        self.server = self.start_url.split('/')[2]
        self.directory = None
        self.duration = 7

        self.checklists = []
        self.errors = []

    def start_requests(self):
        """Configure the spider and get the login page for database.

        Returns:
            Request: yields a single request for the login page of the
                WorldBirds database for the selected country.
        """
        if hasattr(self, '_crawler'):
            self.directory = self.settings['WORLDBIRDS_DOWNLOAD_DIR']
            self.duration = self.settings['WORLDBIRDS_DURATION']

        if self.directory and not os.path.exists(self.directory):
            os.makedirs(self.directory)

        return [Request(url=self.start_url, callback=self.login)]

    def login(self, response):
        """Log in to the application.

        Args:
            response (Response): the login (home) page for the application.

        Returns:
            Request: POST the filled out login form.
        """
        return [FormRequest.from_response(
            response,
            formdata={
                'txtUserName': self.username,
                'txtPassword': self.password},
            callback=self.parse_visits
        )]

    def parse_visits(self, response):
        """Parse the Visit Highlights from the Latest News page.

        Args:
            response (Response): the Latest News page containing the (paged)
                table of Visit Highlights.

        Returns:
            Request: yields a series of Requests for each checklist listed.

        """
        if not response.url.endswith('latest_news.php'):
            raise LoginException()

        limit = datetime.today() - timedelta(days=self.duration)
        visits = self.visit_parser(response).get_visits()

        if 'offset' in response.meta:
            offset = response.meta['offset'] + 10
        else:
            offset = 10

        if visits[-1][0] >= limit:
            yield FormRequest(
                url="http://%s/worldbirds/latestnews.php" % self.server,
                formdata={'hdnVisitStart': '%d' % offset},
                dont_filter=True,
                callback=self.parse_visits,
                meta={'offset': offset}
            )

        url = "http://%s/worldbirds/getdata.php" \
              "?a=VisitHighlightsDetails&id=%s&m=1"

        for values in visits:
            if values[0] >= limit:
                yield Request(
                    url=url % (self.server, values[1]),
                    callback=self.parse_checklist,
                    meta={'identifiers': values[1:]}
                )

    def parse_checklist(self, response):
        """Parse the contents of the checklist popup.

        Args:
            response (Response): the contents of the popup used to display
                the checklist details.

        Returns:
            Request: a request to get the details of the checklist location.
        """
        checklist = self.checklist_parser(response).get_checklist()
        ids = response.meta['identifiers']

        url = "http://%s/worldbirds/getdata.php?a=LocationDetails&id=%s"

        yield Request(
            url=url % (self.server, ids[1]),
            callback=self.parse_location,
            dont_filter=True,
            meta={'identifiers': ids, 'checklist': checklist}
        )

    def parse_location(self, response):
        """Parse the contents of the location popup.

        Args:
            response (Response): the contents of the popup used to display
                the location details.

        Returns:
            Request: a request to get the details of the checklist observer.
        """
        parser = self.location_parser(response)
        ids = response.meta['identifiers']

        url = "http://%s/worldbirds/getdata.php" \
              "?a=ObserverDetails&id=%s"

        yield Request(
            url=url % (self.server, ids[2]),
            callback=self.parse_observer,
            dont_filter=True,
            meta={'identifiers': ids, 'checklist': parser.get_checklist()}
        )

    def parse_observer(self, response):
        """Parse the contents of the observer popup and save the checklist.

        Args:
            response (Response): the contents of the popup used to display
                the details of the observer who submitted the checklist.
        """
        parser = self.observer_parser(response)
        self.save_checklist(parser.get_checklist())

    def save_checklist(self, checklist):
        """Save the checklist in JSON format.

        Args:
            checklist (dict); the checklist.

        The filename using the source, in this case 'worldbirds' and the
        checklist identifier so that the data is always written to the same
        file. The directory where the files are written is defined by the
        setting WORLDBIRDS_DOWNLOAD_DIR. If the directory attribute is set to
        None then the checklist is not saved (used for testing).

        The saved checklist is added to the list of checklists downloaded so
        far so it can be used to generate a status report once the spider has
        finished.
        """
        if self.directory:
            source = checklist['source'].replace(' ', '-').lower()
            path = os.path.join(self.directory, "%s-%s.json" % (
                source, checklist['identifier']))
            save_json_data(path, checklist)
            self.checklists.append(checklist)
