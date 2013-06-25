"""Validate the locations in the downloaded checklists.

Validation Tests:

   Location:
       1. the location is a dict.

   LocationIdentifier (optional):
       1. identifier is a string.
       2. identifier is set.
       3. identifier does not have leading/trailing whitespace.

   LocationName:
       1. name is a string.
       2. name is set.
       3. name does not have leading/trailing whitespace.

   LocationCounty (optional):
       1. county is a string.

   LocationRegion (optional):
       1. region is a string.

   LocationCountry:
       1. country is a string.

   LocationCoordinates
       1. latitude and longitude are floats.

"""
from checklisting.tests.sites import checklists, ValidationTestCase


class Location(ValidationTestCase):
    """Validate the locations in the downloaded checklists."""

    def setUp(self):
        """Initialize the test."""
        self.locations = [checklist['location'] for checklist in checklists]

    def test_location_type(self):
        """Verify the locations field contains a dict."""
        for location in self.locations:
            self.assertIsInstance(location, dict)


class LocationIdentifier(ValidationTestCase):
    """Validate the location identifier in the downloaded checklists.

    This field is optional.
    """

    def setUp(self):
        """Initialize the test."""
        self.identifiers = [checklist['location']['identifier']
                            for checklist in checklists
                            if 'identifier' in checklist['location']]

    def test_identifier_type(self):
        """Verify the location identifier is a unicode string."""
        for identifier in self.identifiers:
            self.assertIsInstance(identifier, unicode)

    def test_identifier_set(self):
        """Verify the location identifier is set."""
        for identifier in self.identifiers:
            self.assertTrue(identifier)

    def test_identifier_stripped(self):
        """Verify the location identifier has no extra whitespace."""
        for identifier in self.identifiers:
            self.assertStripped(identifier)


class LocationName(ValidationTestCase):
    """Validate the location name in the downloaded checklists."""

    def setUp(self):
        """Initialize the test."""
        self.locations = [checklist['location'] for checklist in checklists]

    def test_name_type(self):
        """Verify the location name is a unicode string."""
        for location in self.locations:
            self.assertIsInstance(location['name'], unicode)

    def test_name_set(self):
        """Verify the location name is set."""
        for location in self.locations:
            self.assertTrue(location['name'])

    def test_name_stripped(self):
        """Verify the location name has no extra whitespace."""
        for location in self.locations:
            self.assertStripped(location['name'])


class LocationCounty(ValidationTestCase):
    """Validate the location county name in the downloaded checklists.

    This field is optional.
    """

    def setUp(self):
        """Initialize the test."""
        self.counties = [checklist['location']['county']
                         for checklist in checklists
                         if 'county' in checklist['location']]

    def test_county_type(self):
        """Verify the location county is a unicode string."""
        for county in self.counties:
            self.assertIsInstance(county, unicode)


class LocationRegion(ValidationTestCase):
    """Validate the location region name in the downloaded checklists.

    This field is optional.
    """

    def setUp(self):
        """Initialize the test."""
        self.regions = [checklist['location']['region']
                        for checklist in checklists
                        if 'region' in checklist['location']]

    def test_region_type(self):
        """Verify the location county is a unicode string."""
        for region in self.regions:
            self.assertIsInstance(region, unicode)


class LocationCountry(ValidationTestCase):
    """Validate the location country name in the downloaded checklists."""

    def setUp(self):
        """Initialize the test."""
        self.locations = [checklist['location'] for checklist in checklists]

    def test_country_type(self):
        """Verify the location country is a unicode string."""
        for location in self.locations:
            self.assertIsInstance(location['country'], unicode)


class LocationCoordinates(ValidationTestCase):
    """Validate the latitude and longitude fields."""

    def setUp(self):
        """Initialize the test."""
        self.locations = [checklist['location'] for checklist in checklists]

    def test_latitude(self):
        """Verify the location latitude is a unicode string."""
        for location in self.locations:
            self.assertIsInstance(location['lat'], float)

    def test_longitude(self):
        """Verify the location longitude is a unicode string."""
        for location in self.locations:
            self.assertIsInstance(location['lon'], float)
