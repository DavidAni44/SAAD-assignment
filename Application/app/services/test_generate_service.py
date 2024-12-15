import unittest
from flask import Flask
app = Flask(__name__)
from unittest.mock import MagicMock, patch
import pandas as pd
from app.services.report_service import (
    borrow_report,
    reserve_report,
    branch_report,
    report_selection,
    export_as,
    export_to_csv,
    export_to_excel,
    convert_excel_to_pdf
)

#These test cases are for the Generate Report service. 
#We're testing that each report type can be made, and exported in the relevant formats.

class TestLibraryReports(unittest.TestCase):
    
    #this tests that borrow reports are working
    @patch("app.services.database.user_collection.find")
    @patch("app.services.database.transaction_collection.find_one")
    def test_borrow_report(self, mock_find_one, mock_find):
        mock_users = [
            {
                "_id": "user1",
                "name": "John Doe",
                "email": "johndoe@example.com",
                "borrowed_media": ["media1", "media2"]
            }
        ]
        mock_find.return_value = mock_users

        mock_find_one.side_effect = [
            {
                "media_id": "media1",
                "borrowed_date": "2023-12-01",
                "due_date": "2023-12-15",
                "return_date": "2023-12-10",
                "returned": True,
                "delivery_type": "Pickup",
                "delivery_address": {"street": "123 Main St"},
                "postage": ["Postage1"],
                "payment_method": "Credit Card"
            },
            {
                "media_id": "media2",
                "borrowed_date": "2023-12-05",
                "due_date": "2023-12-20",
                "return_date": None,
                "returned": False,
                "delivery_type": "Delivery",
                "delivery_address": {"street": "456 Elm St"},
                "postage": ["Postage2"],
                "payment_method": "PayPal"
            }
        ]

        report_data, report_name = borrow_report()

        self.assertEqual(report_name, "Borrow_Report")
        self.assertEqual(len(report_data), 1)
        self.assertEqual(report_data[0]["User Name"], "John Doe")
        self.assertEqual(len(report_data[0]["Borrowed Media Details"]), 2)
    
    #this tests that reserve reports are working
    @patch("app.services.database.user_collection.find")
    @patch("app.services.database.branch_collection.find_one")
    def test_reserve_report(self, mock_find_one, mock_find):
        mock_users = [
            {
                "_id": "user1",
                "name": "Jane Doe",
                "email": "janedoe@example.com",
                "branch_id": "branch1",
                "reserved_media": ["media1"]
            }
        ]
        mock_find.return_value = mock_users

        mock_find_one.return_value = {
            "_id": "branch1",
            "name": "Central Library",
            "media": [
                {"media_id": "media1", "available_copies": 2, "total_copies": 5}
            ]
        }

        report_data, report_name = reserve_report()

        self.assertEqual(report_name, "Reserve_Report")
        self.assertEqual(len(report_data), 1)
        self.assertEqual(report_data[0]["User Name"], "Jane Doe")
        self.assertEqual(len(report_data[0]["Reserved Media Details"]), 1)

    #this tests that branch reports are working
    @patch("app.services.database.branch_collection.find")
    def test_branch_report(self, mock_find):
        mock_branches = [
            {
                "_id": "branch1",
                "name": "Central Library",
                "library_id": "lib1",
                "address": "123 Main St",
                "email": "library@example.com",
                "media": [
                    {"media_id": "media1", "available_copies": 3, "total_copies": 10},
                    {"media_id": "media2", "available_copies": 1, "total_copies": 4}
                ]
            }
        ]
        mock_find.return_value = mock_branches

        report_data, report_name = branch_report()

        self.assertEqual(report_name, "Branch_Report")
        self.assertEqual(len(report_data), 2)
        self.assertEqual(report_data[0]["Branch Name"], "Central Library")
        self.assertEqual(report_data[0]["Available Copies"], 3)


    #this tests that report selecting works correctly
    @patch("app.services.report_service.borrow_report")
    @patch("app.services.report_service.reserve_report")
    @patch("app.services.report_service.branch_report")
    def test_report_selection(self, mock_branch_report, mock_reserve_report, mock_borrow_report):
        mock_borrow_report.return_value = ([{"sample": "data"}], "Borrow_Report")
        mock_reserve_report.return_value = ([{"sample": "data"}], "Reserve_Report")
        mock_branch_report.return_value = ([{"sample": "data"}], "Branch_Report")

        report_data, report_name = report_selection("Borrowed Media")
        self.assertEqual(report_name, "Borrow_Report")

        report_data, report_name = report_selection("Reserved Media")
        self.assertEqual(report_name, "Reserve_Report")

        report_data, report_name = report_selection("Branch Media")
        self.assertEqual(report_name, "Branch_Report")

        with self.assertRaises(ValueError):
            report_selection("Invalid Choice")


    #this tests that export as works correctly
    @patch("app.services.report_service.export_to_excel")
    @patch("app.services.report_service.convert_excel_to_pdf")
    def test_export_as(self, mock_convert_pdf, mock_export_excel):
        mock_export_excel.return_value = "app/static\\file.xlsx"
        mock_convert_pdf.return_value = "app/static\\file.pdf"

        with app.app_context():
            response, status_code = export_as("excel", [{"sample": "data"}], "Test_Report")
            self.assertEqual(status_code, 200)

        with app.app_context():
            response, status_code = export_as("pdf", [{"sample": "data"}], "Test_Report")
            self.assertEqual(status_code, 200)

        with app.app_context():
            response, status_code = export_as("csv", [{"sample": "data"}], "Test_Report")
            self.assertEqual(status_code, 200)

        with app.app_context():
            response, status_code = export_as("invalid", [{"sample": "data"}], "Test_Report")
            self.assertEqual(status_code, 400)


    #this tests exporting to csv
    @patch("app.services.report_service.pd.DataFrame.to_csv")
    @patch("app.services.report_service.os.makedirs")
    @patch("app.services.report_service.os.getcwd", return_value="")
    def test_export_to_csv(self, mock_getcwd, mock_makedirs, mock_to_csv):
        data = [{"User Name": "John Doe", "Email": "johndoe@example.com"}]
        file_name = "Test_Report"

        result_path = export_to_csv(data, file_name)

        self.assertEqual(result_path, "app/static\\Test_Report.csv")
        mock_makedirs.assert_called_once_with("app/static", exist_ok=True)
        mock_to_csv.assert_called_once()


    #This tests that excel to pdf works, using mocked data
    @patch("app.services.report_service.os.path.exists", return_value=True)
    @patch("app.services.report_service.pd.read_excel")
    @patch("app.services.report_service.SimpleDocTemplate")
    @patch("app.services.report_service.os.remove")
    def test_convert_excel_to_pdf(
        self, mock_remove, mock_doc_template, mock_read_excel, mock_path_exists
    ):
        mock_read_excel.return_value = pd.DataFrame(
            {"Column1": ["Value1"], "Column2": ["Value2"]}
        )
        mock_doc = MagicMock()
        mock_doc_template.return_value = mock_doc
        pdf_file = convert_excel_to_pdf("app/static\\Test_Report.xlsx")

        self.assertEqual(pdf_file, "app/static\\Test_Report.pdf")
        mock_doc.build.assert_called_once()
        mock_remove.assert_called_once_with("app/static\\Test_Report.xlsx")






    #This tests export to excel, using mocked data
    @patch("app.services.report_service.pd.DataFrame.to_csv")
    @patch("app.services.report_service.os.makedirs")
    @patch("app.services.report_service.os.getcwd", return_value="")
    def test_export_to_excel(self, mock_getcwd, mock_makedirs, mock_to_csv):
        data = [
            {
                "User Name": "John Doe",
                "Email": "johndoe@example.com",
                "Borrowed Media Details": [
                    {
                        "Media ID": "media1",
                        "Borrowed Date": "2023-12-01",
                        "Due Date": "2023-12-15",
                        "Return Date": "2023-12-10",
                        "Returned": True,
                        "Delivery Type": "Pickup",
                        "Delivery Address": {"street": "123 Main St"},
                        "Postage": ["Postage1"],
                        "Payment Method": "Credit Card",
                    }
                ],
            }
        ]
        file_name = "Test_Report"

        file_path = export_to_excel(data, file_name)

        expected_file_path = "app/static\\Test_Report.xlsx"
        self.assertEqual(file_path, expected_file_path)
        mock_makedirs.assert_called_once_with("app/static", exist_ok=True)
        mock_to_csv.assert_called_once()

if __name__ == "__main__":
    unittest.main(testRunner=CustomTestRunner())

#python -m unittest app.services.test_generate_service