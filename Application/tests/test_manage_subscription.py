import unittest
from unittest.mock import patch, Mock
from app.services.database import user_collection, subscription_collection  # Import necessary collections
from app.services.subscription_services import edit_subscription, get_subscription, get_users_with_subscriptions  # Import functions to test
from bson import ObjectId

# Mock collections for testing
mock_user_collection = [
    {"_id": ObjectId("648682c53160263b00873c71"), "name": "John Doe", "email": "john.doe@example.com", "subscription_id": "subscription_id_1"},
    {"_id": ObjectId("648682c53160263b00873c73"), "name": "Jane Smith", "email": "jane.smith@example.com", "subscription_id": None},
]

mock_subscription_collection = [
    {"_id": ObjectId("648682c63160263b00873c72"), "subscription_id": "subscription_id_1", "subscription_name": "Basic", "subscription_price_per_month": 9.99},
    {"_id": ObjectId("648682c63160263b00873c74"), "subscription_id": "subscription_id_2", "subscription_name": "Premium", "subscription_price_per_month": 19.99},
]

class TestSubscriptionServices(unittest.TestCase):

    @patch('app.services.database.user_collection.update_one')
    def test_edit_subscription_success(self, mock_update_one):
        """Tests successful subscription update."""
        mock_update_one.return_value = {'updated_count': 1, 'matched_count': 1}
        user_id = ObjectId("648682c53160263b00873c71")
        new_subscription = "subscription_id_2" 
        response = edit_subscription(user_id, new_subscription)
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0].json, {"message": "Subscription updated successfully."})

    @patch('app.services.database.user_collection.update_one')
    def test_edit_subscription_user_not_found(self, mock_update_one):
        """Tests subscription update for non-existent user."""
        mock_update_one.return_value = {'updated_count': 0, 'matched_count': 0}
        user_id = ObjectId() 
        new_subscription = "subscription_id_2"
        response = edit_subscription(user_id, new_subscription)
        self.assertEqual(response[1], 404)
        self.assertEqual(response[0].json, {"error": "User not found"})

    @patch('app.services.database.user_collection.update_one')
    def test_edit_subscription_no_changes(self, mock_update_one):
        """Tests subscription update with no changes."""
        mock_update_one.return_value = {'updated_count': 0, 'matched_count': 1}
        user_id = ObjectId("648682c53160263b00873c71")
        new_subscription = "subscription_id_1"  # Same as existing subscription
        response = edit_subscription(user_id, new_subscription)
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0].json, {"message": "Subscription already matches value entered ."})

    @patch('app.services.database.subscription_collection.find', return_value=iter(mock_subscription_collection))
    def test_get_subscription(self, mock_find):
        """Tests get_subscription function."""
        subscriptions = get_subscription()
        self.assertEqual(len(subscriptions), 2)
        self.assertIn({"id": "subscription_id_1", "subscription_name": "Basic", "subscription_price_per_month": 9.99}, subscriptions)
        self.assertIn({"id": "subscription_id_2", "subscription_name": "Premium", "subscription_price_per_month": 19.99}, subscriptions)

    @patch('app.services.database.user_collection.find')
    @patch('app.services.database.subscription_collection.find_one')
    def test_get_users_with_subscriptions(self, mock_find_one, mock_find):
        """Tests get_users_with_subscriptions function."""
        mock_find = Mock()
        mock_find.skip.return_value = self
        mock_find.limit.return_value = iter(mock_user_collection) 
        mock_find_one.side_effect = [
            mock_subscription_collection[0],  # Match for first user
            None,                          # No match for second user
        ]
        users_with_subscriptions = get_users_with_subscriptions()
        self.assertEqual(len(users_with_subscriptions), 2)
        self.assertIn({
            "user_id": str(mock_user_collection[0]["_id"]),
            "name": mock_user_collection[0]["name"],
            "email": mock_user_collection[0]["email"],
            "subscription_id": mock_subscription_collection[0]["subscription_id"],
            "subscription_name": mock_subscription_collection[0]["subscription_name"],
            "subscription_price_per_month": mock_subscription_collection[0]["subscription_price_per_month"],
        }, users_with_subscriptions)
        self.assertIn({
            "user_id": str(mock_user_collection[1]["_id"]),
            "name": mock_user_collection[1]["name"],
            "email": mock_user_collection[1]["email"],
            "subscription_id": None,
            "subscription_name": None,
            "subscription_price_per_month": None,
        }, users_with_subscriptions)

if __name__ == '__main__':
    unittest.main()