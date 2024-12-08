# application_attendance.py
import subprocess
import pandas as pd
from flask import Flask, render_template, request, Response
from datetime import datetime
from src.data.attendance import format_in_time, format_out_time, classify_attendance, create_output_excel

application = Flask(__name__, template_folder="templates", static_folder="templates")
application.config["UPLOAD_FOLDER"] = "uploads"


# Define your route for the upload form
@application.route("/update_server", methods=["POST"])
def webhook():
    if request.method == "POST":
        try:
            subprocess.call(["/bin/bash", "/home/arya2705/vfly_dataentry/pull.sh"])
            return "Pull successful"
        except Exception as e:
            return f"Pull failed: {str(e)}"
    else:
        return "Wrong event type", 400


@application.route("/", methods=["GET", "POST"])
def upload_csv():
    if request.method == "POST":
        csv_file = request.files["csv_file"]
        date_str = request.form["date"]
        if csv_file and date_str:
            # Convert the date string to a datetime object
            selected_date = datetime.strptime(date_str, "%Y-%m-%d")

            # Read the CSV file into a DataFrame
            attendance_data = pd.read_csv(csv_file)

            # Process the attendance data
            attendance_data["In Time"] = attendance_data.apply(lambda row: format_in_time(row["First IN"], selected_date), axis=1)
            attendance_data["Out Time"] = attendance_data.apply(lambda row: format_out_time(row["Last OUT"], selected_date), axis=1)
            # attendance_data["In Time"] = attendance_data["First IN"].apply(format_in_and_out_time)
            # attendance_data["Out Time"] = attendance_data["Last OUT"].apply(format_in_and_out_time)
            attendance_data["Attendance"] = attendance_data.apply(lambda row: classify_attendance(row["In Time"], row["Out Time"]), axis=1)

            # Create the output Excel file
            output = create_output_excel(attendance_data)

            return Response(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=attendance_nnrg.xlsx"}
            )

    return render_template("upload_form.html")


if __name__ == "__main__":
    application.run(debug=True)