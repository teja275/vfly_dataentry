from data.make_df import generate_df_from_response
from data.make_images import split_image_to_chunks
from models.ocr_predict import get_ocr_response
from PIL import Image

import os
import zipfile
import io


def get_excel_from_image(
    input_image_file,
    num_chunks,
    num_records,
    ocr_url,
    output_folder,
    hpatch_size=1,
    vpatch_size=1,
):
    image = Image.open(input_image_file)
    image_chunks = split_image_to_chunks(
        image, num_chunks, num_records, hpatch_size, vpatch_size
    )
    zip_filename = os.path.join(output_folder, "output.zip")

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for chunk_count, image_chunk in enumerate(image_chunks):
            print(f"Processing chunk {chunk_count + 1} for {input_image_file}")
            response = get_ocr_response(ocr_url, image_chunk)
            if chunk_count == 0:
                df_table = generate_df_from_response(response, header_present=True)
            else:
                df_table = generate_df_from_response(response, header_present=False)
            excel_data = io.BytesIO()
            df_table.to_excel(excel_data, index=False)

            # Add the Excel data to the zip file
            zipf.writestr(f"chunk_{chunk_count + 1}.xlsx", excel_data.getvalue())

            image_data = io.BytesIO()
            image_chunk.save(image_data, format="PNG")

            # Add the image data to the zip file
            zipf.writestr(f"image_chunk_{chunk_count + 1}.png", image_data.getvalue())

    return zip_filename


if __name__ == "__main__":
    image = "/Users/bhanuteja/Downloads/work_demo.gif"
    num_chunks = 1
    num_records = 56
    ocr_url = "https://app.nanonets.com/api/v2/OCR/Model/25dda2f2-e3cc-4d91-96aa-ee401d370ca8/LabelFile/?async=false"
    output_folder = "/Users/bhanuteja/Downloads"
    add_patch = True
    get_excel_from_image(
        image, num_chunks, num_records, add_patch, ocr_url, output_folder
    )
