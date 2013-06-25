"""Validate the protocol in each downloaded checklist.

Validation Tests:

    Protocol:
        1. the protocol is a dict.

    ProtocolName:
        1. name is a string.
        2. name is set.
        3.  name does not have leading/trailing whitespace.

    ProtocolDuration
        1. duration hours is an int.
        2. duration minutes is an int

    ProtocolDistance
        1. distance is an int.

    ProtocolArea
        1. area is an int.

    EbirdProtocolName
        1. The protocol names matches the values used on ebird.

    WorldBirdsProtocolName
        1. The protocol names matches the a default value used for WorldBirds.
"""
from checklisting.tests.sites import checklists, ValidationTestCase


class Protocol(ValidationTestCase):
    """Validate the protocols in the downloaded checklists."""

    def setUp(self):
        """Initialize the test."""
        self.protocols = [checklist['protocol'] for checklist in checklists]

    def test_protocol_type(self):
        """Verify the protocols field contains a dict."""
        for protocol in self.protocols:
            self.assertIsInstance(protocol, dict)


class ProtocolName(ValidationTestCase):
    """Validate the protocol name in the downloaded checklists."""

    def setUp(self):
        """Initialize the test."""
        self.protocols = [checklist['protocol'] for checklist in checklists]

    def test_name_type(self):
        """Verify the protocol name is a unicode string."""
        for protocol in self.protocols:
            self.assertIsInstance(protocol['name'], unicode)

    def test_name_set(self):
        """Verify the protocol name is set."""
        for protocol in self.protocols:
            self.assertTrue(protocol['name'])

    def test_name_stripped(self):
        """Verify the protocol name has no extra whitespace."""
        for protocol in self.protocols:
            self.assertStripped(protocol['name'])


class ProtocolDuration(ValidationTestCase):
    """Validate the duration hours and minutes."""

    def setUp(self):
        """Initialize the test."""
        self.protocols = [checklist['protocol'] for checklist in checklists
                          if checklist['protocol']['name'] == 'Traveling']

    def test_duration_hours(self):
        """Verify the protocol duration in hours is an int."""
        for protocol in self.protocols:
            self.assertIsInstance(protocol['duration_hours'], int)

    def test_duration_minutes(self):
        """Verify the protocol duration in minutes is an int."""
        for protocol in self.protocols:
            self.assertIsInstance(protocol['duration_minutes'], int)


class ProtocolDistance(ValidationTestCase):
    """Validate the distance covered."""

    def setUp(self):
        """Initialize the test."""
        self.protocols = [checklist['protocol'] for checklist in checklists
                          if checklist['protocol']['name'] == 'Traveling']

    def test_distance(self):
        """Verify the protocol duration in hours is an int."""
        for protocol in self.protocols:
            self.assertIsInstance(protocol['distance'], int)


class ProtocolArea(ValidationTestCase):
    """Validate the area covered."""

    def setUp(self):
        """Initialize the test."""
        self.protocols = [checklist['protocol'] for checklist in checklists
                          if checklist['protocol']['name'] == 'Area']

    def test_area(self):
        """Verify the protocol duration in hours is an int."""
        for protocol in self.protocols:
            self.assertIsInstance(protocol['area'], int)


class EbirdProtocolName(ValidationTestCase):
    """Validate the protocol names in the downloaded checklists from ebird."""

    def setUp(self):
        """Initialize the test."""
        self.protocols = [checklist['protocol'] for checklist in checklists
                          if checklist['source'] == 'ebird']

    def test_expected_names(self):
        """Verify the protocol name is expected.

        This compares the protocol name against the list on ebird.org as of
        2013-06-25 and alerts to any changes.
        """
        expected = ['Traveling', 'Stationary', 'Incidental', 'Area', 'Random',
                    'Oiled Birds', 'Nocturnal Flight Call Count',
                    'Greater Gulf Refuge Waterbird Count',
                    'Heron Area Count', 'Heron Stationary Count']
        for protocol in self.protocols:
            self.assertTrue(protocol['name'] in expected)


class WorldBirdsProtocolName(ValidationTestCase):
    """Validate the protocol names in the downloaded checklists from ebird."""

    def setUp(self):
        """Initialize the test."""
        self.protocols = [checklist['protocol'] for checklist in checklists
                          if checklist['source'] == 'worldbirds']

    def test_expected_names(self):
        """Verify the protocol name is expected.

        WorldBirds does not define a specific protocol. However start time
        and duration spent counting are defined so a default protocol name
        of "Timed visit" is used.
        """
        for protocol in self.protocols:
            self.assertEqual(protocol['name'], 'Timed visit')
