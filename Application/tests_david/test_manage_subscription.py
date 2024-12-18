import unittest
from unittest.mock import patch, Mock
from app import create_app  # Import your Flask app factory or instance
from app.services.subscription_services import edit_subscription, get_subscription, get_users_with_subscriptions
from bson import ObjectId

# Mock collections for testing
mock_user_collection = [
    {"_id": "user_53", "name": "John Doe", "email": "john.doe@example.com", "subscription_id": "subscription_id_1"},
    {"_id": "user_55", "name": "Jane Smith", "email": "jane.smith@example.com", "subscription_id": None},
]

mock_subscription_collection = [
    {"_id": ObjectId("648682c63160263b00873c72"), "subscription_id": "subscription_id_1", "subscription_name": "Basic", "subscription_price_per_month": 9.99},
    {"_id": ObjectId("648682c63160263b00873c74"), "subscription_id": "subscription_id_2", "subscription_name": "Premium", "subscription_price_per_month": 19.99},
]

class TestSubscriptionServices(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up Flask app context for all tests."""
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        """Clean up Flask app context after all tests."""
        cls.app_context.pop()

    @patch('app.services.database.user_collection.update_one')
    def test_edit_subscription_success(self, mock_update_one):
        """Tests successful subscription update."""
        mock_result = Mock()
        mock_result.matched_count = 1
        mock_result.modified_count = 1
        mock_update_one.return_value = mock_result

        user_id = "user_53"
        new_subscription = "subscription_id_2"

        response = edit_subscription(user_id, new_subscription)
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0].json, {"message": "Subscription updated successfully."})

    @patch('app.services.database.user_collection.update_one')
    def test_edit_subscription_user_not_found(self, mock_update_one):
        """Tests subscription update for non-existent user."""
        mock_result = Mock()
        mock_result.matched_count = 0
        mock_result.modified_count = 0
        mock_update_one.return_value = mock_result

        user_id = "user_123"  # Non-existent user
        new_subscription = "subscription_id_3"

        response = edit_subscription(user_id, new_subscription)
        self.assertEqual(response[1], 404)
        self.assertEqual(response[0].json, {"error": "User not found"})

    @patch('app.services.database.user_collection.update_one')
    def test_edit_subscription_no_changes(self, mock_update_one):
        """Tests subscription update with no changes."""
        mock_result = Mock()
        mock_result.matched_count = 1
        mock_result.modified_count = 0
        mock_update_one.return_value = mock_result

        user_id = "user_53"
        new_subscription = "subscription_id_1"  # Same as existing subscription

        response = edit_subscription(user_id, new_subscription)
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0].json, {"message": "Subscription already matches value entered ."})

    @patch('app.services.database.subscription_collection.find')
    def test_get_subscription(self, mock_find):
        """Tests get_subscription function."""
        mock_find.return_value = iter(mock_subscription_collection)

        subscriptions = get_subscription()
        self.assertEqual(len(subscriptions), 2)
        self.assertIn({"id": "subscription_id_1", "subscription_name": "Basic", "subscription_price_per_month": 9.99}, subscriptions)
        self.assertIn({"id": "subscription_id_2", "subscription_name": "Premium", "subscription_price_per_month": 19.99}, subscriptions)

    @patch('app.services.database.user_collection.find')
    @patch('app.services.database.subscription_collection.find_one')
    def test_get_users_with_subscriptions(self, mock_find_one, mock_find):
        """Tests get_users_with_subscriptions function with detailed debugging."""
        # Debugging: Print initial mock collections
        print("Mock User Collection:", mock_user_collection)
        print("Mock Subscription Collection:", mock_subscription_collection)

        # Mock the cursor returned by find()
        mock_cursor = Mock()
        mock_cursor.skip.return_value = mock_cursor  # Allow chaining skip()
        mock_cursor.limit.return_value = iter(mock_user_collection)  # Allow chaining limit()
        mock_find.return_value = mock_cursor  # Mock find() to return the cursor

        # Correct side effects for find_one to include the "_id" field
        mock_find_one.side_effect = [
            {"_id": "648682c63160263b00873c72", "subscription_id": "subscription_id_1", "subscription_name": "Basic", "subscription_price_per_month": 9.99},
            None,  # No subscription for second user
        ]

        # Debugging: Print the find_one side_effect
        print("Mock find_one Side Effect:", mock_find_one.side_effect)

        # Call the function under test
        print("\n--- Calling get_users_with_subscriptions ---")
        users_with_subscriptions = get_users_with_subscriptions()

        # Debugging: Print the result
        print("Users with Subscriptions Result:", users_with_subscriptions)

        # Assertions
        self.assertEqual(len(users_with_subscriptions), 2)

        # Check first user with a subscription
        expected_user_1 = {
            "user_id": mock_user_collection[0]["_id"],
            "name": mock_user_collection[0]["name"],
            "email": mock_user_collection[0]["email"],
            "subscription_id": "648682c63160263b00873c72",  # Now matches "_id"
            "subscription_name": "Basic",
            "subscription_price_per_month": 9.99,
        }
        print("Expected User 1:", expected_user_1)
        self.assertIn(expected_user_1, users_with_subscriptions)

        # Check second user with no subscription
        expected_user_2 = {
            "user_id": mock_user_collection[1]["_id"],
            "name": mock_user_collection[1]["name"],
            "email": mock_user_collection[1]["email"],
            "subscription_id": None,
            "subscription_name": None,
            "subscription_price_per_month": None,
        }
        print("Expected User 2:", expected_user_2)
        self.assertIn(expected_user_2, users_with_subscriptions)



if __name__ == '__main__':
    unittest.main()
