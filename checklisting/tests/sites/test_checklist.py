"""Validate the checklist attributes in the downloaded checklists.

Validation Tests:

   Checklist:
       1. the checklist is a dict.

   ChecklistIdentifier:
       1. identifier is a string.
       2. identifier is set.
       3. identifier does not have leading/trailing whitespace.

   ChecklistDate:
       1. date is a string.
       2. date is in the format YYYY-MM-DD

   ChecklistSubmittedBy:
       1. submitted_by is a string.
       2. submitted_by is set.
       3. submitted_by does not have leading/trailing whitespace.

   ChecklistObservers:
       1. observers is a list.
       2. each observer name is a string.
       3. each observer name does not have leading/trailing whitespace.

   ChecklistSource:
       1. source is a string.
       2. source is set.
       3. source does not have leading/trailing whitespace.
"""
from checklisting.tests.sites import checklists, ValidationTestCase


class Checklist(ValidationTestCase):
    """Validate the checklist."""

    def test_checklist_type(self):
        """Verify the checklist is a dict."""
        for checklist in checklists:
            self.assertIsInstance(checklist, dict)


class ChecklistIdentifier(ValidationTestCase):
    """Validate the checklist identifier in the downloaded checklists."""

    def test_checklist_version(self):
        """Verify the checklist identifier is a unicode string."""
        for checklist in checklists:
            self.assertIsInstance(checklist['identifier'], unicode)

    def test_checklist_identifier(self):
        """Verify the checklist identifier is a unicode string."""
        for checklist in checklists:
            self.assertIsInstance(checklist['identifier'], unicode)

    def test_checklist_identifier_set(self):
        """Verify the checklist identifier is set."""
        for checklist in checklists:
            self.assertTrue(checklist['identifier'])

    def test_checklist_identifier_stripped(self):
        """Verify the checklist identifier has no extra whitespace."""
        for checklist in checklists:
            self.assertStripped(checklist['identifier'])


class ChecklistDate(ValidationTestCase):
    """Validate the checklist date in the downloaded checklists."""

    def test_date_type(self):
        """Verify the checklist date is a unicode string."""
        for checklist in checklists:
            self.assertIsInstance(checklist['date'], unicode)

    def test_date_format(self):
        """Verify the checklist date is in the format YYYY-MM-DD."""
        date_format = r'(\d){4}-(\d){2}-(\d){2}'
        for checklist in checklists:
            self.assertRegexpMatches(checklist['date'], date_format)


class ChecklistSubmittedBy(ValidationTestCase):
    """Validate the checklist submitter in the downloaded checklists."""

    def test_submitted_by_type(self):
        """Verify the checklist submitter is a unicode string."""
        for checklist in checklists:
            self.assertIsInstance(checklist['submitted_by'], unicode)

    def test_submitted_by_set(self):
        """Verify the checklist submitter is set."""
        for checklist in checklists:
            self.assertTrue(checklist['submitted_by'])

    def test_submitted_by_stripped(self):
        """Verify the checklist submitter has no extra whitespace."""
        for checklist in checklists:
            self.assertStripped(checklist['submitted_by'])


class ChecklistObservers(ValidationTestCase):
    """Validate the checklist observers in the downloaded checklists."""

    def test_observers_type(self):
        """Verify the observers is a list."""
        for checklist in checklists:
            self.assertIsInstance(checklist['observers'], list)

    def test_observer_names_type(self):
        """Verify the names of the checklist observers."""
        for checklist in checklists:
            for observer in checklist['observers']:
                self.assertIsInstance(observer, unicode)

    def test_observer_names_stripped(self):
        """Verify the observer names don't have extra whitespace."""
        for checklist in checklists:
            for observer in checklist['observers']:
                self.assertStripped(observer)


class ChecklistSource(ValidationTestCase):
    """Validate the checklist source in the downloaded checklists."""

    def test_source_type(self):
        """Verify the checklist source is a unicode string."""
        for checklist in checklists:
            self.assertIsInstance(checklist['source'], unicode)

    def test_source_set(self):
        """Verify the checklist submitter is set."""
        for checklist in checklists:
            self.assertTrue(checklist['source'])

    def test_source_stripped(self):
        """Verify the source has no extra whitespace."""
        for checklist in checklists:
            self.assertStripped(checklist['source'])
