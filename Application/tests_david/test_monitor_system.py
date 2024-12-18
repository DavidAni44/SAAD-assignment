import unittest
from unittest.mock import patch
from app.services.database import user_collection, media_collection, branch_collection  # Import necessary collections
from app.services.monitor_system import get_users, get_media, get_branches, get_media_by_branch  # Import functions to test

# Mock collections for testing
mock_user_collection = [
    {"_id": 1, "name": "John Doe", "email": "john.doe@example.com"},
    {"_id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"},
]

mock_media_collection = [
    {"_id": 1, "title": "Book A", "genre": "Fiction"},
    {"_id": 2, "title": "Book B", "genre": "Non-Fiction"},
    {"_id": 3, "title": "Book A", "genre": "Fiction"},  # Duplicate title
]

mock_branch_collection = [
    {"_id": 1, "name": "Main Library", "media": [1, 2]},
    {"_id": 2, "name": "Branch A", "media": []},  # Branch with no media
]


class TestLibraryFunctions(unittest.TestCase):

    @patch('app.services.database.user_collection.find', return_value=iter(mock_user_collection))
    def test_get_users(self, mock_find):
        """Tests the get_users function."""
        users = get_users()
        self.assertEqual(len(users), 2)
        self.assertIn({"name": "John Doe", "email": "john.doe@example.com"}, users)
        self.assertIn({"name": "Jane Smith", "email": "jane.smith@example.com"}, users)

    @patch('app.services.database.media_collection.find', return_value=iter(mock_media_collection))
    def test_get_media(self, mock_find):
        """Tests the get_media function."""
        media_count = get_media()
        self.assertEqual(media_count, 2)  # Expect 2 unique titles

    @patch('app.services.database.branch_collection.find', return_value=iter(mock_branch_collection))
    def test_get_branches(self, mock_find):
        """Tests the get_branches function."""
        branches = get_branches()
        self.assertEqual(len(branches), 2)
        self.assertIn({"name": "Main Library"}, branches)
        self.assertIn({"name": "Branch A"}, branches)

    @patch('app.services.database.branch_collection.find', return_value=iter(mock_branch_collection))
    def test_get_media_by_branch(self, mock_find):
        """Tests the get_media_by_branch function."""
        branches_with_media = get_media_by_branch()
        self.assertEqual(len(branches_with_media), 2)
        self.assertIn({"branch": {"name": "Main Library"}, "media": [1, 2]}, branches_with_media)
        self.assertIn({"branch": {"name": "Branch A"}, "media": []}, branches_with_media)

if __name__ == '__main__':
    unittest.main()