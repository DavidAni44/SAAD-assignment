import pandas as pd
from flask import jsonify
from reportlab.lib.pagesizes import letter,landscape
import os
from app.services.database import user_collection, media_collection, transaction_collection, branch_collection
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def export_to_excel(data, file_name):
    flat_data = []
    for entry in data:
        if "Borrowed Media Details" in entry or "Reserved Media Details" in entry:
            for media in entry.get("Borrowed Media Details", []):
                flat_data.append({
                    "User Name": entry.get("User Name"),
                    "Email": entry.get("Email"),
                    "Media ID": media.get("Media ID"),
                    "Borrowed Date": media.get("Borrowed Date"),
                    "Due Date": media.get("Due Date"),
                    "Return Date": media.get("Return Date"),
                    "Returned": media.get("Returned"),
                    "Delivery Type": media.get("Delivery Type"),
                    "Delivery Address": str(media.get("Delivery Address")),
                    "Postage": ", ".join(map(str, media.get("Postage", []) or [])),
                    "Payment Method": media.get("Payment Method"),
                })

            for media in entry.get("Reserved Media Details", []):
                flat_data.append({
                    "User Name": entry.get("User Name"),
                    "Email": entry.get("Email"),
                    "Media ID": media.get("Media ID"),
                    "Home Branch": entry.get("Branch Name"),
                    "Available Copies": media.get("Available Copies"),
                    "Total Copies": media.get("Total Copies"),
                })

        else:
            flat_data.append(entry)

    df = pd.DataFrame(flat_data)

    if df.empty:
        raise ValueError("The data could not be converted into a table format.")
    file_path = os.path.join(os.getcwd(), f"{file_name}.xlsx")
    df.to_excel(file_path, index=False)

    print(f"Data exported to Excel successfully at: {file_path}")
    return file_path


def export_to_csv(data, file_name):
    flat_data = []
    for entry in data:
        if "Borrowed Media Details" in entry or "Reserved Media Details" in entry:
            for media in entry.get("Borrowed Media Details", []):
                flat_data.append({
                    "User Name": entry.get("User Name"),
                    "Email": entry.get("Email"),
                    "Media ID": media.get("Media ID"),
                    "Borrowed Date": media.get("Borrowed Date"),
                    "Due Date": media.get("Due Date"),
                    "Return Date": media.get("Return Date"),
                    "Returned": media.get("Returned"),
                    "Delivery Type": media.get("Delivery Type"),
                    "Delivery Address": str(media.get("Delivery Address")),
                    "Postage": ", ".join(map(str, media.get("Postage", []) or [])),
                    "Payment Method": media.get("Payment Method"),
                })

            for media in entry.get("Reserved Media Details", []):
                flat_data.append({
                    "User Name": entry.get("User Name"),
                    "Email": entry.get("Email"),
                    "Media ID": media.get("Media ID"),
                    "Home Branch": entry.get("Branch Name"),
                    "Available Copies": media.get("Available Copies"),
                    "Total Copies": media.get("Total Copies"),
                })

        else:
            flat_data.append(entry)

    df = pd.DataFrame(flat_data)

    if df.empty:
        raise ValueError("The data could not be converted into a table format.")

    file_path = os.path.join(os.getcwd(), f"{file_name}.csv")
    df.to_csv(file_path, index=False)
    print(f"Data exported to CSV successfully at: {file_path}")
    return file_path




def convert_excel_to_pdf(excel_file):
    try:
        excel_data = pd.read_excel(excel_file)
        data = [excel_data.columns.tolist()] + excel_data.values.tolist()
        base_name = os.path.splitext(os.path.basename(excel_file))[0]
        pdf_file = os.path.join(os.path.dirname(excel_file), f"{base_name}.pdf")
        doc = SimpleDocTemplate(pdf_file, pagesize=landscape(letter))
        page_width = landscape(letter)[0] - 50
        num_columns = len(data[0]) if data else 1
        col_width = page_width / num_columns if num_columns > 0 else page_width
        styles = getSampleStyleSheet()
        
        styled_data = []
        for row in data:
            styled_row = [Paragraph(str(cell), styles['BodyText']) for cell in row]
            styled_data.append(styled_row)
        
        table = Table(styled_data, colWidths=[col_width] * num_columns)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        doc.build([table])
        os.remove(excel_file)
        return pdf_file
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    
    


def export_as(format_type, report_data, report_name):
    try:
        if not report_data:
            return jsonify({"message": "No data available for the report."}), 404
        
        if format_type == 'excel':
            file_path = export_to_excel(report_data, report_name)
        elif format_type == 'csv':
            file_path = export_to_csv(report_data, report_name)
        elif format_type == 'pdf':
            file_path = export_to_excel(report_data, report_name)
            convert_excel_to_pdf(file_path)
        else:
            return jsonify({"error": "Invalid format type requested"}), 400

        return jsonify({"message": f"Report generated successfully. File saved at {file_path}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def borrow_report():
    report_name = "Borrow_Report"
    users = user_collection.find({"borrowed_media": {"$exists": True, "$ne": []}})
    
    report_data = []
    for user in users:
        user_name = user.get("name", "Unknown User")
        user_email = user.get("email", "No Email")
        user_id = user.get("_id")
        borrowed_media_list = user.get("borrowed_media", [])
        
        media_details = []
        for media_id in borrowed_media_list:
            transaction = transaction_collection.find_one({"user_id": user_id, "media_id": media_id})
            if transaction:
                media_details.append({
                    "Media ID": media_id,
                    "Borrowed Date": transaction.get("borrowed_date", "Unknown"),
                    "Due Date": transaction.get("due_date", "Unknown"),
                    "Return Date": transaction.get("return_date", "Not Returned"),
                    "Returned": transaction.get("returned", False),
                    "Delivery Type": transaction.get("delivery_type", "Unknown"),
                    "Delivery Address": transaction.get("delivery_address", {}),
                    "Postage": transaction.get("postage", []),
                    "Payment Method": transaction.get("payment_method", "Unknown"),
                })

        report_data.append({
            "User Name": user_name,
            "Email": user_email,
            "Borrowed Media Details": media_details,
        })

    return report_data, report_name

def reserve_report():
    report_name = "Reserve_Report"
    users = user_collection.find()
    
    report_data = []
    for user in users:
        user_id = user.get("_id")
        user_name = user.get("name", "Unknown User")
        user_email = user.get("email", "No Email")
        user_branch_id = user.get("branch_id")
        reserved_media = user.get("reserved_media", [])

        if not reserved_media:
            continue

        branch = branch_collection.find_one({"_id": user_branch_id})
        if not branch:
            continue

        branch_name = branch.get("name", "Unknown Branch")
        branch_media = branch.get("media", [])

        reserved_media_details = []
        for media_id in reserved_media:
            media_item = next((media for media in branch_media if media['media_id'] == media_id), None)
            if media_item:
                reserved_media_details.append({
                    "Media ID": media_id,
                    "Available Copies": media_item['available_copies'],
                    "Total Copies": media_item['total_copies'],
                })

        report_data.append({
            "User Name": user_name,
            "Email": user_email,
            "Branch Name": branch_name,
            "Reserved Media Details": reserved_media_details,
        })

    return report_data, report_name




def branch_report():
    report_name = "Branch_Report"
    report_data = []
    branches = branch_collection.find()
    for branch in branches:
        branch_id = branch.get("_id", "Unknown Branch ID")
        branch_name = branch.get("name", "Unknown Branch")
        library_id = branch.get("library_id", "Unknown Library ID")
        address = branch.get("address", "No Address Provided")
        email = branch.get("email", "No Email Provided")
        media_list = branch.get("media", [])

        for media in media_list:
            report_data.append({
                "Branch ID": branch_id,
                "Branch Name": branch_name,
                "Library ID": library_id,
                "Address": address,
                "Email": email,
                "Media ID": media.get("media_id", "Unknown Media ID"),
                "Available Copies": media.get("available_copies", 0),
                "Total Copies": media.get("total_copies", 0),
            })

    return report_data, report_name



def report_selection(report_choice):
    if report_choice == "Borrowed Media":
        report_data, report_name = borrow_report()
        return report_data, report_name
    elif report_choice == "Reserved Media":
        report_data, report_name = reserve_report()
        return report_data, report_name
    elif report_choice == "Branch Media":
        report_data, report_name = branch_report()
        return report_data, report_name
