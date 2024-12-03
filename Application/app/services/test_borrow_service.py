import pytest
from unittest.mock import patch, MagicMock
import smtplib
from app.services.borrow_service import send_user_email, check_media_avaliable, create_transaction
from flask import Flask


"""
#Test Send User Email Function

mock_user = {'_id': 'user_id', 'branch_id': '123', 'email': 'user@example.com', 'name': 'Test User'}


@pytest.mark.parametrize("email, should_fail", [
    ('valid.email@example.com', False),  # valid email
    ('another.valid@email.com', False),  # valid email
    ('invalid-email.com', True),         # invalid email
    ('invalid@domain', True),            # invalid email
    ('', True)                           # empty/invalid email
])

def test_send_user_email(email, should_fail):
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        if should_fail:
            mock_server.sendmail.side_effect = smtplib.SMTPException("Failed to send email")
        else:
            mock_server.sendmail.side_effect = None  
        
        try:
            send_user_email("Test Subject", "Test Body", email)

            if should_fail:
                pytest.fail(f"Expected error for email {email} but it was sent successfully.")
            else:
                mock_smtp.assert_called_with("smtp.gmail.com", 587)
                mock_server.sendmail.assert_called_once()

                args, kwargs = mock_server.sendmail.call_args
                actual_from, actual_to, actual_body = args

                assert actual_from == "xclwright@gmail.com"
                assert actual_to == email
                assert "Test Body" in actual_body 
        
        except smtplib.SMTPException as e:
            if not should_fail:
                pytest.fail(f"Unexpected error sending email to {email}: {str(e)}")
            else:
                assert str(e) == "Failed to send email"
"""

"""

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    with app.app_context():
        yield app.test_client()

valid_media_id = "media123"
invalid_media_id = "z14sgye4"

valid_user = {"branch_id": "branch123"}
invalid_user = {"branch_id": None} 

valid_branch_data = {
    "_id": "branch123",
    "media": [
        {"media_id": valid_media_id, "available_copies": 5},  
        {"media_id": invalid_media_id, "available_copies": 0}  
    ]
}

invalid_branch_data = None  


# Test case 1: Valid user with valid branch and valid media
def test_check_media_avaliable_valid_user_valid_branch_valid_media(client):
    with patch("app.services.borrow_service.branch_collection.find_one", side_effect=[valid_branch_data, valid_branch_data]):
        result = check_media_avaliable(valid_user, valid_media_id)
        assert result == valid_branch_data  # Branch data should be returned as media is available

# Test case 2: Valid user with valid branch but invalid media (media not available)
def test_check_media_avaliable_valid_user_valid_branch_invalid_media(client):
    with patch("app.services.borrow_service.branch_collection.find_one", side_effect=[valid_branch_data, valid_branch_data]):
        result = check_media_avaliable(valid_user, invalid_media_id)
        assert result is None  # No matching media found in the branch

# Test case 3: Valid user with invalid branch and valid media
def test_check_media_avaliable_valid_user_invalid_branch_valid_media(client):
    with patch("app.services.borrow_service.branch_collection.find_one", side_effect=[invalid_branch_data, None]):
        result = check_media_avaliable(valid_user, valid_media_id)
        assert result[1] == 404  # Should return status 404
        assert result[0].json["error"] == "Branch not found"

# Test case 4: Valid user with invalid branch and invalid media
def test_check_media_avaliable_valid_user_invalid_branch_invalid_media(client):
    with patch("app.services.borrow_service.branch_collection.find_one", side_effect=[invalid_branch_data, None]):
        result = check_media_avaliable(valid_user, invalid_media_id)
        assert result[1] == 404  # Should return status 404
        assert result[0].json["error"] == "Branch not found"

# Test case 5: Invalid user with valid branch and valid media
def test_check_media_avaliable_invalid_user_valid_branch_valid_media(client):
    with patch("app.services.borrow_service.branch_collection.find_one", side_effect=[valid_branch_data, valid_branch_data]):
        result = check_media_avaliable(invalid_user, valid_media_id)
        assert result[1] == 400  # Should return status 400
        assert result[0].json["error"] == "User does not have a home branch assigned"

# Test case 6: Invalid user with invalid branch and valid media
def test_check_media_avaliable_invalid_user_invalid_branch_valid_media(client):
    with patch("app.services.borrow_service.branch_collection.find_one", side_effect=[invalid_branch_data, None]):
        result = check_media_avaliable(invalid_user, valid_media_id)
        assert result[1] == 400  # Should return status 400
        assert result[0].json["error"] == "User does not have a home branch assigned"

"""

"""
#Test Create Transaction

mock_transaction_collection = MagicMock()

valid_user = {
    "_id": "user123",
    "branch_id": "branch123",
    "email": "user@example.com",
    "name": "Test User",
    "address": "123 Main St, City, Country",
    "payment_method": "Credit Card"
}

valid_media_id = "media123"
valid_delivery_choice = "Home Delivery"
valid_borrow_until = "2024-12-31"

invalid_users = [
    None,  
    {},  
    {"_id": None, "branch_id": None},  
]

invalid_media_ids = [
    None,  
    "",  
]

invalid_delivery_choices = [
    None,  
    "",  
    "Unknown Delivery", 
]

invalid_borrow_until_dates = [
    None,  
    "",  
    "2023-01-01",  
]

@patch("app.services.borrow_service.transaction_collection", mock_transaction_collection)
def test_create_transaction_valid():
    # Test with all valid inputs
    mock_transaction_collection.insert_one.return_value = MagicMock(inserted_id="transaction123")

    transaction_id = create_transaction(valid_user, valid_media_id, valid_delivery_choice, valid_borrow_until)

    assert transaction_id == "transaction123", "Expected a valid transaction ID"
    mock_transaction_collection.insert_one.assert_called_once()

@patch("app.services.borrow_service.transaction_collection", mock_transaction_collection)
@pytest.mark.parametrize("user", invalid_users)
def test_create_transaction_invalid_user(user):
    with pytest.raises(Exception):
        create_transaction(user, valid_media_id, valid_delivery_choice, valid_borrow_until)

@patch("app.services.borrow_service.transaction_collection", mock_transaction_collection)
@pytest.mark.parametrize("media_id", invalid_media_ids)
def test_create_transaction_invalid_media_id(media_id):
    with pytest.raises(Exception):
        create_transaction(valid_user, media_id, valid_delivery_choice, valid_borrow_until)

@patch("app.services.borrow_service.transaction_collection", mock_transaction_collection)
@pytest.mark.parametrize("delivery_choice", invalid_delivery_choices)
def test_create_transaction_invalid_delivery_choice(delivery_choice):
    with pytest.raises(Exception):
        create_transaction(valid_user, valid_media_id, delivery_choice, valid_borrow_until)

@patch("app.services.borrow_service.transaction_collection", mock_transaction_collection)
@pytest.mark.parametrize("borrow_until", invalid_borrow_until_dates)
def test_create_transaction_invalid_borrow_until_date(borrow_until):
    with pytest.raises(Exception):
        create_transaction(valid_user, valid_media_id, valid_delivery_choice, borrow_until)
"""