# application.py
from flask import Flask, render_template, request, Response
from config import OCR_API_URL
from src.run_ocr_pipeline import get_excel_from_image

application = Flask(__name__, template_folder="templates")
application.config["UPLOAD_FOLDER"] = "uploads"


# Define your route for the upload form
@application.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        image = request.files["image"]
        num_chunks = int(request.form["num_chunks"])
        num_records = int(request.form["num_records"])
        output_filename_prefix = request.form["file_prefix"]
        if image:
            # Call your processing script here
            zip_file = get_excel_from_image(
                image, num_chunks, num_records, output_filename_prefix, OCR_API_URL
            )
            return Response(
                zip_file,
                mimetype="application/zip",
                headers={
                    "Content-Disposition": "attachment; filename=image_chunks.zip"
                },
            )
    # Return the form for GET requests
    return render_template("upload_form.html")


if __name__ == "__main__":
    application.run()
