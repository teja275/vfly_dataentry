# application.py
from flask import Flask, render_template, request, send_file, Response
from werkzeug.utils import secure_filename
import os
from src.run_ocr_pipeline import get_excel_from_image

application = Flask(__name__, template_folder="templates")
application.config["UPLOAD_FOLDER"] = "uploads"


# Define your route for the upload form
@application.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        num_chunks = int(request.form["num_chunks"])
        num_records = int(request.form["num_records"])
        image = request.files["image"]
        if image:
            # filename = secure_filename(image.filename)
            # image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            # image.save(image_path)

            ocr_url = "https://app.nanonets.com/api/v2/OCR/Model/25dda2f2-e3cc-4d91-96aa-ee401d370ca8/LabelFile/?async=false"
            # Call your processing script here
            zip_file = get_excel_from_image(image, num_chunks, num_records, ocr_url)

            return Response(
                zip_file,
                mimetype='application/zip',
                headers={'Content-Disposition': 'attachment; filename=image_chunks.zip'}
            )

    # Return the form for GET requests
    return render_template("upload_form.html")


if __name__ == "__main__":
    application.run()
