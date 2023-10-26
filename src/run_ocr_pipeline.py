import io
import zipfile

from PIL import Image

from config import OCR_API_URL
from src.data.make_df import generate_df_from_response
from src.data.make_images import split_image_to_chunks
from src.models.ocr_predict import get_ocr_response


def get_excel_from_image(
    input_image_file,
    num_chunks,
    num_records,
    output_filename_prefix,
    ocr_url,
    hpatch_size=1,
    vpatch_size=1,
):
    image = Image.open(input_image_file)
    image_chunks = split_image_to_chunks(
        image, num_chunks, num_records, hpatch_size, vpatch_size
    )
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for chunk_count, image_chunk in enumerate(image_chunks):
            print(f"Processing chunk {chunk_count + 1} for {input_image_file}")
            response = get_ocr_response(
                ocr_url,
                image_chunk,
                f"{output_filename_prefix}_image_chunk_{chunk_count + 1}.jpg",
            )
            if chunk_count == 0:
                df_table = generate_df_from_response(response, header_present=True)
            else:
                df_table = generate_df_from_response(response, header_present=False)
            excel_data = io.BytesIO()
            df_table.to_excel(excel_data, index=False)

            # Add the Excel data to the zip file
            zipf.writestr(
                f"{output_filename_prefix}_chunk_{chunk_count + 1}.xlsx",
                excel_data.getvalue(),
            )

            image_data = io.BytesIO()
            image_chunk.save(image_data, format="PNG")

            # Add the image data to the zip file
            zipf.writestr(
                f"{output_filename_prefix}_image_chunk_{chunk_count + 1}.png",
                image_data.getvalue(),
            )
    zip_buffer.seek(0)
    return zip_buffer


if __name__ == "__main__":
    image_file = "/Users/aryan/Downloads/work_demo.gif"
    num_chunks = 1
    num_records = 60
    output_folder = "/Users/aryan/Downloads"
    get_excel_from_image(image_file, num_chunks, num_records, "demo", OCR_API_URL)
