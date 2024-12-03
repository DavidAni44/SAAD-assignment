from unittest.mock import MagicMock, patch
import pytest
from app.services.reserve_service import add_to_reserved_media, check_media_unavaliable, return_staged
from flask import Flask
"""
mock_user_collection = MagicMock()

@pytest.mark.parametrize("user_id, media_id, matched_count, modified_count, expected_response", [
    ({"_id": "user123"}, "media123", 1, 1, {"message": "Media reserved successfully", "status_code": 200}),  # Success
    ({"_id": "user123"}, "media123", 1, 0, {"message": "Media was already reserved", "status_code": 200}),   # Already reserved
    ({"_id": "user123"}, "media123", 0, 0, {"error": "User not found", "status_code": 404}),                # User not found
])
@patch("app.services.reserve_service.user_collection", mock_user_collection)  # Adjust import path
def test_add_to_reserved_media(user_id, media_id, matched_count, modified_count, expected_response):
    mock_user_collection.reset_mock()
    mock_user_collection.update_one.return_value = MagicMock(
        matched_count=matched_count,
        modified_count=modified_count
    )
    response, status_code = add_to_reserved_media(user_id, media_id)
    assert response == expected_response["message"] if "message" in expected_response else expected_response["error"]
    assert status_code == expected_response["status_code"]
    mock_user_collection.update_one.assert_called_once_with(
        {"_id": str(user_id["_id"])},
        {"$addToSet": {"reserved_media": str(media_id)}}
    )


"""



# Mock data
valid_user = {"_id": "user123", "branch_id": "branch123"}
invalid_user = {"_id": "user123", "branch_id": None}  # User has no branch assigned
valid_media_id = "media123"
invalid_media_id = "media999"

valid_branch_data = {
    "_id": "branch123",
    "media": [{"media_id": "media123", "available_copies": 1}]  # Media is available
}

invalid_branch_data = {
    "_id": "branch123",
    "media": []  # No media available in the branch
}

@pytest.mark.parametrize("user, media_id, branch_find_return_value, media_find_return_value, expected_response, expected_status_code", [
    # Test 1: User has no home branch
    (invalid_user, valid_media_id, None, None, {"error": "User does not have a home branch assigned"}, 400),

    # Test 2: Branch not found
    (valid_user, valid_media_id, None, None, {"error": "Branch not found"}, 404),

    # Test 3: Media unavailable in the branch
    (valid_user, valid_media_id, {"_id": "branch123", "media": []}, None, {"error": "Media not found in user's home branch"}, 400),  # media unavailable

    # Test 4: Valid case (media is available)
    (valid_user, valid_media_id, {"_id": "branch123", "media": [{"media_id": "media123", "available_copies": 1}]}, None, {"message": "Media available"}, 200),  # media available
])
@patch("app.services.reserve_service.branch_collection", autospec=True)
def test_check_media_unavaliable(mock_branch_collection, user, media_id, branch_find_return_value, media_find_return_value, expected_response, expected_status_code):
    # Mock the `branch_collection.find_one` function to return the appropriate data
    mock_branch_collection.find_one.side_effect = [branch_find_return_value, media_find_return_value]

    # Set up Flask application context
    app = Flask(__name__)
    with app.app_context():
        # Call the function
        response, status_code = check_media_unavaliable(user, media_id)

        # Assert the response and status code
        assert status_code == expected_status_code
        assert response.json == expected_response

    # Validate that `find_one` was called twice: first to check the branch, then to check the media
    if branch_find_return_value is not None:
        mock_branch_collection.find_one.assert_any_call({"_id": user["branch_id"]})
    if media_find_return_value is not None:
        mock_branch_collection.find_one.assert_any_call({
            "_id": user["branch_id"],
            "media": {
                "$elemMatch": {
                    "media_id": str(media_id),
                    "available_copies": {"$eq": 0}  # Ensures we check for media with 0 available copies
                }
            }
        })
