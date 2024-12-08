import pandas as pd
import io
from datetime import datetime, time


def format_in_time(in_time_str, attendance_date):
    try:
        return pd.to_datetime(in_time_str, format="%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            return pd.to_datetime(in_time_str, format="ISO8601")
        except ValueError:
            # return datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
            return attendance_date.replace(hour=9, minute=0, second=0, microsecond=0)


def format_out_time(out_time_str, attendance_date):
    try:
        return pd.to_datetime(out_time_str, format="%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            return pd.to_datetime(out_time_str, format="ISO8601")
        except ValueError:
            # return datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)
            return attendance_date.replace(hour=17, minute=0, second=0, microsecond=0)


def classify_attendance(intime, outtime):
    if (outtime - intime) < pd.Timedelta(hours=4):
        return "Low Working Hours"
    elif (intime - pd.to_datetime("2024-12-03 09:00:00")) > pd.Timedelta(hours=1.5) or (pd.to_datetime("2024-12-03 17:00:00") - outtime) > pd.Timedelta(hours=1.5):
        return "Half Day Leave"
    elif (intime.time() < pd.to_datetime("09:05:00").time()) and (outtime.time() > pd.to_datetime("15:45:00").time()):
        return "Punctual"
    elif (intime.time() < pd.to_datetime("10:05:00").time()) and (outtime.time() > pd.to_datetime("15:45:00").time()):
        return "Permission - Late In"
    elif (intime.time() < pd.to_datetime("09:05:00").time()) and (outtime.time() < pd.to_datetime("15:45:00").time()):
        return "Permission - Early Out"
    elif (intime.time() < pd.to_datetime("10:05:00").time()) and (outtime.time() < pd.to_datetime("15:45:00").time()):
        return "Permission - Late In Early Out"
    else:
        return "Other"


def create_output_excel(attendance_data):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for value in attendance_data["Attendance"].unique():
            filtered_df = attendance_data[attendance_data['Attendance'] == value]
            filtered_df.to_excel(writer, sheet_name=str(value), index=False)
    output.seek(0)
    return output
