import unittest
from unittest.mock import patch, MagicMock
from app.services.media_procurement_service import (
    mediaToOrder, procure_media, create_order, get_branch_email,
    prepare_email, send_email, track_order, edit_order_status
)
from bson import ObjectId
from flask import Flask, jsonify
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)


#These tests are for the media procurement service, ensuring we can make an order and seeing if we can track it.
class TestMediaProcurementService(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    #Tests that all media can be loaded to then choose from
    @patch('app.services.media_procurement_service.media_collection')
    def test_mediaToOrder(self, mock_media_collection):
        mock_media_list = [
            {"_id": ObjectId("60c72b2f5f1b2c001fbbd663"), "title": "Book Title", "author": "Author Name", "type": "Book", "description": "A good book", "price_per_item": 10, "vendor_name": "Vendor Name", "vendor_contact": "vendor@example.com"},
        ]
        mock_media_collection.find.return_value = mock_media_list

        result = mediaToOrder()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], "Book Title")
        self.assertIsInstance(result[0]['_id'], str)


    #Testing that an order can be created
    @patch('app.services.media_procurement_service.media_collection.find_one')
    def test_create_order(self, mock_find_one):
        mock_find_one.return_value = {
            "_id": ObjectId("675eca2bcb8b111922dc731d"),
            "title": "Book Title",
            "vendor_name": "Vendor Name",
            "vendor_contact": "vendor@example.com",
            "price_per_item": 10
        }

        order_id = create_order("675eca2bcb8b111922dc731d", "Branch1", 5, "2024-12-15")
        
        
    #Testing that an order can go through
    @patch('app.services.media_procurement_service.create_order')
    @patch('app.services.media_procurement_service.prepare_email')
    def test_procure_media(self, mock_prepare_email, mock_create_order):
        mock_create_order.return_value = "60c72b2f5f1b2c001fbbd663"

        response, status_code = procure_media("60c72b2f5f1b2c001fbbd663", "Branch1", 5, "2024-12-15")

        self.assertEqual(response.json['message'], "Media procured successfully.")
        self.assertEqual(status_code, 200)

    #Testing that a branches email can be found
    @patch('app.services.media_procurement_service.branch_collection.find_one')
    def test_get_branch_email(self, mock_find_one):
        mock_find_one.return_value = {
            "_id": "Branch1",
            "name": "Branch Name",
            "email": "branch@example.com"
        }

        email = get_branch_email("Branch1")

        self.assertEqual(email, "branch@example.com")


    #Testing that an email can be written
    @patch('app.services.media_procurement_service.media_collection.find_one')
    @patch('app.services.media_procurement_service.send_email')
    def test_prepare_email(self, mock_send_email, mock_find_one):
        mock_find_one.side_effect = lambda query: {
            "673c85daede0ec4def1bca71": {
                "_id": ObjectId("673c85daede0ec4def1bca71"),
                "title": "Book Title",
                "branch_id": "branch_id_8"
            }
        }[str(query['_id'])]

        prepare_email("branch_id_8", 5, "673c85daede0ec4def1bca71", "order_id_5", "2024-12-15")

        mock_send_email.assert_called_once()

    #Testing sending email confirmation
    @patch('app.services.media_procurement_service.smtplib.SMTP')
    def test_send_email(self, MockSMTP):
        mock_server = MockSMTP.return_value
        subject = "Test Subject"
        body = "Test Body"
        emails = ["test1@example.com"]

        message = MIMEMultipart()
        message["From"] = "xclwright@gmail.com"
        message["To"] = "test1@example.com"
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        send_email(subject, body, emails)

        mock_server.sendmail.assert_any_call("xclwright@gmail.com", "test1@example.com", message.as_string())



#The tests for Tracking and Editing an order were not written.
#Due to time constraints in development we weren't able to fully implement these.
#The functions written in the service file use old versions of the database, so would not be testable at this stage.
    
    
if __name__ == '__main__':
    unittest.main()
    

#python -m unittest app.services.test_media_procurement_service
