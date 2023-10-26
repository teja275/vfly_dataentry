# application.py
from flask import Flask, render_template, request, Response
from config import OCR_API_URL
from src.run_ocr_pipeline import get_excel_from_image
from src.data.make_images import download_image_chunks
import git

application = Flask(__name__, template_folder="templates", static_folder="templates")
application.config["UPLOAD_FOLDER"] = "uploads"


# Define your route for the upload form
@application.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo_path = '/home/arya2705/vfly_dataentry'  # Change this to the actual path of your local repository
        try:
            repo = git.Repo(repo_path)
            origin = repo.remotes.origin
            origin.pull()
            return 'Updated PythonAnywhere successfully', 200
        except Exception as e:
            return f'Error: {str(e)}', 500
    else:
        return 'Wrong event type', 400


@application.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        image = request.files["image"]
        num_chunks = int(request.form["num_chunks"])
        num_records = int(request.form["num_records"])
        output_filename_prefix = request.form["file_prefix"]
        processing_option = request.form.get("processing_option")
        if image:
            if processing_option == "Image Chunking & OCR":
                # Call your processing script here
                zip_file = get_excel_from_image(
                    image, num_chunks, num_records, output_filename_prefix, OCR_API_URL
                )
                return Response(
                    zip_file,
                    mimetype="application/zip",
                    headers={
                        "Content-Disposition": f"attachment; filename={output_filename_prefix}_image_and_excel_chunks.zip"
                    },
                )
            elif processing_option == "Image Chunking Only":
                zip_file = download_image_chunks(
                    image, num_chunks, num_records, output_filename_prefix
                )
                return Response(
                    zip_file,
                    mimetype="application/zip",
                    headers={
                        "Content-Disposition": f"attachment; filename={output_filename_prefix}_image_chunks.zip"
                    },
                )

    # Return the form for GET requests
    return render_template("upload_form.html")


if __name__ == "__main__":
    application.run(debug=True)
