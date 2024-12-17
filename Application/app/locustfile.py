from locust import HttpUser, task, between
import random

class SubscriptionTestUser(HttpUser):
    wait_time = between(1, 3)  # Wait between requests (1-3 seconds)

    @task(1)
    def get_all_subscriptions(self):
        """Fetch all subscriptions."""
        response = self.client.get("/api/subscription/get_all")
        if response.status_code == 200:
            print("Successfully fetched all subscriptions.")
        else:
            print(f"Failed to fetch subscriptions. Status Code: {response.status_code}")

    @task(2)
    def update_user_subscription(self):
        """Test updating a user's subscription."""
        # Simulate updating a subscription for user_id: user_53
        user_id = "user_53"
        payload = {"subscription_id": f"subscription_id_{random.randint(1, 2)}"}  # Randomize subscription ID

        response = self.client.post(
            f"/api/subscription/update_user_subscription/{user_id}",
            json=payload
        )
        if response.status_code == 200:
            print(f"Successfully updated subscription for user {user_id}.")
        else:
            print(f"Failed to update subscription for user {user_id}. Status Code: {response.status_code}")

    @task(2)
    def get_users_with_subscriptions(self):
        """Fetch paginated users with subscriptions."""
        page = random.randint(1, 2)  # Simulate random page access
        limit = 10  # Fixed page size for now

        response = self.client.get(f"/api/subscription/get_subs?page={page}&limit={limit}")
        if response.status_code == 200:
            print(f"Fetched users with subscriptions on page {page}.")
        else:
            print(f"Failed to fetch users with subscriptions. Status Code: {response.status_code}")

    @task(1)
    def manage_subscription(self):
        """Test managing a subscription."""
        payload = {"user_id": "user_53", "new_subscription": "subscription_id_2"}

        response = self.client.post("/api/subscription/manage", json=payload)
        if response.status_code == 200:
            print("Successfully managed subscription.")
        else:
            print(f"Failed to manage subscription. Status Code: {response.status_code}")


class MonitorSystemUser(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def get_users(self):
        user_id = "user_53"
        with self.client.get(f"/api/users/{user_id}", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get users! Status: {response.status_code}")
            else:
                response.success()

    @task(1)
    def get_media(self):
        with self.client.get("/api/media/all_media", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get media! Status: {response.status_code}")
            else:
                response.success()

    @task(1)
    def get_branches(self):
        with self.client.get("/api/media/all_branches", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get branches! Status: {response.status_code}")
            else:
                response.success()

    @task(2)
    def get_media_by_branch(self):
        with self.client.get("/api/media/all_branch_media", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get media by branch! Status: {response.status_code}")
            else:
                response.success()