import pandas as pd
from flask import request, jsonify
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.services.database import user_collection, media_collection, transaction_collection, branch_collection


def export_to_excel(data, file_name):
    df = pd.DataFrame(data)
    file_path = f"{file_name}.xlsx"
    df.to_excel(file_path, index=False)
    return file_path

def export_to_csv(data, file_name):
    df = pd.DataFrame(data)
    file_path = f"{file_name}.csv"
    df.to_csv(file_path, index=False)
    return file_path

def export_to_pdf(data, file_name):
    file_path = f"{file_name}.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    y_position = 750
    c.drawString(100, y_position + 20, "Borrowed Media Report")
    y_position -= 30

    for item in data:
        user_details = f"User: {item['User Name']} (Email: {item['Email']})"
        c.drawString(100, y_position, user_details)
        y_position -= 20

        borrowed_media = item["Borrowed Media"]
        c.drawString(120, y_position, f"Borrowed Media: {borrowed_media}")
        y_position -= 40

        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = 750

    c.save()
    return file_path

def report():
    try:
        format_type = request.json.get('format', 'excel') 
        users = user_collection.find({"borrowed_media": {"$exists": True, "$ne": []}})
        
        report_data = []
        for user in users:
            user_name = user.get("name", "Unknown User")
            user_email = user.get("email", "No Email")
            borrowed_media = ", ".join(user.get("borrowed_media", [])) if user.get("borrowed_media") else "None"

            report_data.append({
                "User Name": user_name,
                "Email": user_email,
                "Borrowed Media": borrowed_media
            })

        if not report_data:
            return jsonify({"message": "No users with borrowed media found."}), 404

        if format_type == 'excel':
            file_path = export_to_excel(report_data, "borrowed_media_report")
        elif format_type == 'csv':
            file_path = export_to_csv(report_data, "borrowed_media_report")
        elif format_type == 'pdf':
            file_path = export_to_pdf(report_data, "borrowed_media_report")
        else:
            return jsonify({"error": "Invalid format type requested"}), 400

        return jsonify({"message": f"Borrowed media report generated successfully. File saved at {file_path}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
