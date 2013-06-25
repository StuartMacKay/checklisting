"""Validate each entry of the downloaded checklists.

Validation Tests:

   Entry:
       1. the entry is a dict.

   EntryCount:
       1. count is an integer.
       2. count is positive.

"""
from checklisting.tests.sites import checklists, ValidationTestCase


class Entry(ValidationTestCase):
    """Validate the entry in the downloaded checklists."""

    def setUp(self):
        """Initialize the test."""
        self.entries = []
        for checklist in checklists:
            self.entries.extend(checklist['entries'])

    def test_entry_type(self):
        """Verify the entry field contains a dict."""
        for entry in self.entries:
            self.assertIsInstance(entry, dict)


class EntryCount(ValidationTestCase):
    """Validate the entry count in the downloaded checklists."""

    def setUp(self):
        """Initialize the test."""
        self.entries = []
        for checklist in checklists:
            self.entries.extend(checklist['entries'])

    def test_count_type(self):
        """Verify the entry count is an integer."""
        for entry in self.entries:
            self.assertIsInstance(entry['count'], int)

    def test_count_positive(self):
        """Verify the entry count is a positive integer."""
        for entry in self.entries:
            self.assertTrue(entry['count'] >= 0)
