"""A crawler downloading checklists from eBird.

This crawler creates checklists for recent observations for a given region
using the eBird API. Additional information for each checklist is also
scraped from the checklist web page.
"""

import copy
import json
import os
import re

from scrapy import log
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

from checklisting.spiders import CHECKLIST_FILE_FORMAT_VERSION, \
    CHECKLIST_FILE_LANGUAGE
from checklisting.spiders.utils import remove_whitespace, select_keys, dedup, \
    save_json_data


class JSONParser(object):

    """Extract checklists from JSON data returned from the eBird API."""

    location_keys = [
        'locID',
        'locName',
        'subnational1Name',
        'subnational2Name',
        'countryName',
        'lat',
        'lng',
    ]

    checklist_keys = [
        'firstName',
        'lastName',
        'obsDt',
        'subID',
    ] + location_keys

    def __init__(self, response):
        """Initialize the parser with a JSON encoded response.

        Args:
            response (str): an encoded string containing the JSON data returned
                by a call to the eBird API.

        Returns:
            JSONParser: a JSONParser object with the records decided from
            the JSON data.
        """
        self.records = json.loads(response.body_as_unicode())

    def get_checklists(self):
        """Get the set of checklists from the observations."""
        filtered = dedup(select_keys(self.records, self.checklist_keys))
        checklists = [self.get_checklist(record) for record in filtered]
        for checklist in checklists:
            checklist['entries'] = [self.get_entry(r) for r in self.records
                                    if r['subID'] == checklist['identifier']]
        return checklists

    def get_checklist(self, record):
        """Get the fields for a checklist from an observation.

        Args:
            record (dict): the observation record.

        Returns:
            dict: a dictionary containing the checklist fields.
        """
        first_name = record['firstName'].strip()
        last_name = record['lastName'].strip()

        if ' ' in record['obsDt']:
            time = record['obsDt'].strip().split(' ')[1]
        else:
            time = '12:00:00'

        return {
            'version': CHECKLIST_FILE_FORMAT_VERSION,
            'language': CHECKLIST_FILE_LANGUAGE,
            'identifier': record['subID'].strip(),
            'location': self.get_location(record),
            'date': record['obsDt'].strip().split(' ')[0],
            'time': time,
            'submitted_by': first_name + ' ' + last_name,
            'observers': [first_name + ' ' + last_name],
            'source': 'eBird',
        }

    def get_locations(self):
        """Get the set of locations from the observations.

        Returns:
            list(dict): a list of dicts containing the fields for a location.
        """
        filtered = dedup(select_keys(self.records, self.location_keys))
        return [self.get_location(record) for record in filtered]

    def get_location(self, record):
        """Get the fields for a location from an observation.

        Returns:
            dict: a dictionary containing the fields for a location.

        If a given field is not present in the record then the value defaults
        to an empty string. This allows the method to process records that
        contain either the simple results fields or the full results fields.
        """
        return {
            'identifier': record['locID'],
            'name': record['locName'],
            'county': record.get('subnational2Name', ''),
            'region': record.get('subnational1Name', ''),
            'country': record.get('countryName', ''),
            'lat': record['lat'],
            'lon': record['lng'],
        }

    def get_entry(self, record):
        """Get the fields for an entry from an observation.

        Returns:
            dict: a dictionary containing the fields for a checklist entry.
        """
        return {
            'identifier': record['obsID'],
            'species': self.get_species(record),
            'count': record.get('howMany', 0),
        }

    def get_species(self, record):
        """Get the species fields for an entry from an observation.

        Args:
            record (dict); the observation record,

        Returns:
            dict: a dictionary containing the fields for a species.
        """
        return {
            'name': record['comName'],
            'scientific_name': record['sciName'],
        }


class HTMLParser(object):

    """Extract information from the checklist web page.

    Only the information not available through the API is extracted, with the
    exception of the counts for each species- which has the associated details
    dictionary which contains a breakdown of the count based on age and sex.
    """

    def __init__(self, response):
        """Initialize the parser with an HTML encoded response.

        Args:
            response (str): the contents of the checklist web page.

        Returns:
            HTMLParser: an HTMLParser object containing the contents of the
                checklist web page and a dict containing the main checklist
                attributes.
        """
        self.docroot = HtmlXPathSelector(response)
        self.attributes = self.get_attributes(self.docroot)

    def get_attributes(self, node):
        """Get the checklist attributes.

        Args:
            node (HtmlXPathSelector): an XML node,

        Returns:
            dict: a dictionary containing the fields and values of a checklist.
        """
        keys = node.select('//dl/dt/text()').extract()
        keys = remove_whitespace(keys)
        values = node.select('//dl/dd/text()').extract()
        values = remove_whitespace(values)
        return dict(zip(keys, values))

    def get_checklist(self):
        """Get the checklist fields extracted ffrom the HTML response.

        Returns:
            dict: a checklist containing the fields extract from the HTML.

        Only the fields not available through the API are extracted from the
        HTML. The parser can be sub-classed to extract any more information.
        """
        return {
            'observer_count': self.get_observer_count(),
            'observers': self.get_observers(),
            'protocol': self.get_protocol(),
            'entries': self.get_entries(),
        }

    def get_protocol(self):
        """Get the protocol used for the checklist.

        Returns:
            dict: a dictionary containing the fields describing the protocol
                used to count the birds recorded in the checklist.
        """
        protocol_name = self.attributes.get('Protocol:', None)

        duration_str = self.attributes.get('Duration:', '')
        if 'hour' in duration_str:
            duration_hours = int(re.search(
                r'(\d+) h', duration_str).group(1))
        else:
            duration_hours = 0
        if 'min' in duration_str:
            duration_minutes = int(re.search(
                r'(\d+) m', duration_str).group(1))
        else:
            duration_minutes = 0

        distance_str = self.attributes.get('Distance:', '0 kilometer(s)')
        if 'kilometer' in distance_str:
            distance = int(float(re.search(
                r'([\.\d]+) k', distance_str).group(1)) * 1000)
        else:
            distance = int(float(re.search(
                r'([\.\d]+) m', distance_str).group(1)) * 1609)

        return {
            'name': protocol_name,
            'duration_hours': duration_hours,
            'duration_minutes': duration_minutes,
            'distance': distance,
            'area': 0,
        }

    def get_observers(self):
        """Get the additional observers.

        Returns:
            list(str): the observers, excluding the person who submitted the
                checklist.
        """
        return remove_whitespace(
            self.attributes.get('Observers:', '').split(','))

    def get_observer_count(self):
        """Get the number of observers present.

        Returns:
           int: the number of observers for the checklist. Defaults to zero
               if the data is missing from the HTML or there is an error
               converting it to an int.
        """
        try:
            count = int(self.attributes.get('Party Size:', '0'))
        except ValueError:
            count = 0
        return count

    def get_entries(self):
        """Get the checklist entries with any additional details for the count.

        Returns:
            list(dict): a list of dicts contains the fields for a checklist
                entry. In turn each contains a list of dicts containing the
                fields describing the breakdown of the entry count by age and
                sex.
        """
        entries = []
        for selector in self.docroot.select('//tr[@class="spp-entry"]'):
            name = selector.select(
                './/h5[@class="se-name"]/text()').extract()[0].strip()
            count = selector.select(
                './/h5[@class="se-count"]/text()').extract()[0].strip()

            species = {
                'name': name,
            }

            try:
                count = int(count)
            except ValueError:
                count = 0

            entries.append({
                'species': species,
                'count': count,
                'details': self.get_entry_details(selector),
                'comment': self.get_entry_comment(selector),
            })
        return entries

    def get_entry_comment(self, node):
        """Get any comment for a checklist entry.

        Args:
            node (HtmlXPathSelector): the node in the tree from where to
                extract the comment.

        Returns:
            str: any comment associated with a checklist entry.
        """
        comment = ''
        selection = node.select('.//p[@class="obs-comments"]/text()')\
            .extract()
        if selection:
            comment = selection[0].strip()
        return comment

    def get_entry_details(self, node):
        """Get the details for each count.

        Args:
            node (HtmlXPathSelector): the node in the tree from where to
                extract the entry details.

        Returns:
            list(dict): a list of dicts containing the fields that describe
                the breakdown of the checklist entry count by age and sex.
        """
        details = []

        xpath = './/div[@class="sd-data-age-sex"]//tr'
        names = node.select(xpath).select('./th/text()').extract()

        for selector in node.select(xpath):
            ages = selector.select('./td')

            if not ages:
                continue

            sex = ages[0].select('./text()').extract()[0]

            for index, age in zip(range(1, 5), names):
                values = ages[index].select('./text()').extract()
                if values:
                    details.append({
                        'age': age,
                        'sex': sex,
                        'count': int(values[0])
                    })
        return details


class EBirdSpider(BaseSpider):
    """Extract checklists recently added to eBird.

    The spider starts by using the API to return the observations for the
    last <n> days for the selected region. The recent observations for a region
    only contain the simple results fields so additional requests are generated
    for the recent observations for each location which contain the full result
    fields. Not all the useful information for a checklist is available through
    the API so the checklist web page from eBird.org is also parsed to extract
    information such as the type of protocol used, breakdowns by age and sex of
    the counts for each species, etc. The completed checklist is then written
    in JSON format to a file.

    Details on the eBird API and the different sets of fields returned can be
    found at https://confluence.cornell.edu/display/CLOISAPI/eBird+API+1.1

    Three settings control the behaviour of the spider:

    CHECKLISTING_DOWNLOAD_DIR: the directory where the downloaded checklists
    will be written in JSON format. The directory will be created if it does
    not exist.

    EBIRD_DURATION: the number of days to fetch observations for. The eBird
    API allows access to observations up to 30 days old.

    EBIRD_INCLUDE_HTML: include data from the checklist web page.

    The spider keeps a list of checklists downloaded and save along with any
    errors raised. These are used to create a status report by the extension,
    SpiderStatusReport which is emailed out when the spider finishes.
    """

    name = 'ebird'
    allowed_domains = ["ebird.org", "secure.birds.cornell.edu"]
    api_parser = JSONParser
    html_parser = HTMLParser

    region_url = "http://ebird.org/ws1.1/data/obs/region/recent?" \
                 "rtype=subnational1&r=%s&back=%d&fmt=json"
    location_url = "http://ebird.org/ws1.1/data/obs/loc/recent?" \
                   "r=%s&detail=full&back=%d&includeProvisional=true&fmt=json"
    checklist_url = "http://ebird.org/ebird/view/checklist?subID=%s"

    def __init__(self, region, **kwargs):
        """Initialize the spider.

        Args:
            region (str): the code identifying the eBird region to fetch
                observations for.

        Returns:
            EBirdSpider: a Scrapy crawler object.
        """
        super(EBirdSpider, self).__init__(**kwargs)
        if not region:
            raise ValueError("You must specify an eBird region")
        self.region = region
        self.log("Downloading checklists for region: %s" % self.region,
                 log.INFO)

        self.checklists = []
        self.errors = []

    def start_requests(self):
        """Configure the spider and issue the first request to the eBird API.

        Returns:
            Request: yields a single request for the recent observations for
                an eBird region.
        """
        self.duration = int(self.settings['EBIRD_DURATION'])
        self.log("Fetching observations for the past %d days" % self.duration,
                 log.INFO)

        self.directory = self.settings['CHECKLISTING_DOWNLOAD_DIR']
        if self.directory and not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.log("Writing checklists to %s" % self.directory, log.INFO)

        self.include_html = self.settings['EBIRD_INCLUDE_HTML']
        if self.include_html:
            self.log("Downloading checklists from API and web pages", log.INFO)
        else:
            self.log("Downloading checklists from API only", log.INFO)

        url = self.region_url % (self.region, self.duration)
        return [Request(url, callback=self.parse_region)]

    def parse_region(self, response):
        """Request the recent observations for each location.

        Args:
            response (Response): the result of calling the eBird API to get the
                recent observations for a region.

        Returns:
            Request: yields a series of requests to the eBird API to get the
                recent observations for each location extracted from the
                recent observations for the region.
        """
        for location in self.api_parser(response).get_locations():
            url = self.location_url % (location['identifier'], self.duration)
            yield Request(url, callback=self.parse_locations)

    def parse_locations(self, response):
        """Create the checklists from the observations.

        Args:
            response (Response): the result of calling the eBird API to get the
                recent observations for a location.

        Returns:
            Request: (when the attribute include_html is True) yields a series
                of requests to the eBird website to get web page used to
                display the details of a checklist.

        Even with the full results fields there is still useful information
        missing so additional requests are generated for the checklist web
        page. Whether the spider continues and processes the checklist web
        page is controlled by the EBIRD_INCLUDE_HTML setting.
        """
        checklists = self.api_parser(response).get_checklists()
        for checklist in checklists:
            if self.include_html:
                url = self.checklist_url % checklist['identifier']
                yield Request(url, callback=self.parse_checklist,
                              dont_filter=True, meta={'checklist': checklist})
            else:
                self.save_checklist(checklist)

    def parse_checklist(self, response):
        """Parse the missing checklist data from the web page.

        Args:
            response (str): the contents of the checklist web page.

        The checklist first extracted from the call the eBird API is passed
        through the parse_region() and parse_locations() methods using the
        metadata attribute on the Request and Response objects. It is then
        merged with the data has been extracted from the web page and written
        to a file in the directory specified when the spider was created.

        ISSUE: If the setting CONCURRENT_REQUEST != 1 then the checklist data
        in the response sometimes does not match the checklist in the request
        metadata. The problem appears to be intermittent, but for a given run
        of the spider it usually happens after the 4th or 5th response. The
        cause is not known. If the problem occurs then an error is logged and
        the checklist is discarded.
        """
        if not response.url.endswith(response.meta['checklist']['identifier']):
            self.log("Checklists in response and request don't match."
                     "Identifiers: %s != %s" % (
                         response.url[-9:],
                         response.meta['checklist']['identifier']
                     ), log.ERROR)
            return

        update = self.html_parser(response).get_checklist()
        original = response.meta['checklist']
        checklist = self.merge_checklists(original, update)
        checklist['url'] = response.url
        self.save_checklist(checklist)

    def merge_checklists(self, original, update):
        """Merge two checklists together.

        Args:
           original (dict): the checklist extracted from the JSON data.
           update (dict): the checklist extracted from the web page.

        Returns:
           dict: a deep copy of the JSON checklist updated with values from
               the checklist obtained from the web page.
        """
        result = copy.deepcopy(original)

        result['observers'] = original['observers'] + update['observers']
        result['observer_count'] = update['observer_count']
        result['protocol'] = update['protocol']

        entries = {entry['species']['name']: entry
                   for entry in result['entries']}

        for entry in update['entries']:
            key = entry['species']['name']
            if key in entries:
                entries[key].update(entry)
            else:
                entries[key] = entry

        result['entries'] = entries.values()

        return result

    def save_checklist(self, checklist):
        """Save the checklist in JSON format.

        Args:
        checklist (dict); the checklist.

        The filename using the source, in this case 'ebird' and the checklist
        identifier so that the data is always written to the same file. The
        directory where the files are written is defined by the setting
        CHECKLISTING_DOWNLOAD_DIR. If the directory attribute is set to None
        then the checklist is not saved (used for testing).

        The saved checklist is added to the list of checklists downloaded so
        far so it can be used to generate a status report once the spider has
        finished.
        """
        if self.directory:
            path = os.path.join(self.directory, "%s-%s.json" % (
                checklist['source'], checklist['identifier']))
            save_json_data(path, checklist)
            self.checklists.append(checklist)

            self.log("Wrote %s: %s %s (%s)" % (
                path, checklist['date'], checklist['location']['name'],
                checklist['submitted_by']), log.DEBUG)
