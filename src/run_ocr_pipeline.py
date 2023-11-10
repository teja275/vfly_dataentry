import io
import zipfile
from concurrent.futures import (
    as_completed,
    ThreadPoolExecutor,
)  # Import ThreadPoolExecutor

from PIL import Image

from config import OCR_API_URL, OCR_API_KEY
from src.data.make_df import generate_df_from_response
from src.data.clean_df import clean_df
from src.data.make_images import split_image_to_chunks
from src.models.ocr_predict import get_ocr_response


def process_chunk(
    chunk_count, image_chunk, output_filename_prefix, ocr_api_url, ocr_api_key
):
    print(f"Processing chunk {chunk_count + 1}")
    response = get_ocr_response(
        ocr_api_url,
        ocr_api_key,
        image_chunk,
        f"{output_filename_prefix}_image_chunk_{chunk_count + 1}.jpg",
    )
    if chunk_count == 0:
        df_table = generate_df_from_response(response, header_present=True)
    else:
        df_table = generate_df_from_response(response, header_present=False)
    df_table = clean_df(df_table)
    excel_data = io.BytesIO()
    df_table.to_excel(excel_data, index=False)
    return (chunk_count, excel_data)


def get_excel_from_image(
    input_image_file,
    num_chunks,
    num_records,
    output_filename_prefix,
    ocr_api_url,
    ocr_api_key,
    hpatch_size=1,
    vpatch_size=1,
):
    image = Image.open(input_image_file)
    image_chunks = split_image_to_chunks(
        image, num_chunks, num_records, hpatch_size, vpatch_size
    )
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    process_chunk,
                    i,
                    chunk,
                    output_filename_prefix,
                    ocr_api_url,
                    ocr_api_key,
                )
                for i, chunk in enumerate(image_chunks)
            ]
            for future in as_completed(futures):
                chunk_count, excel_data = future.result()
                zipf.writestr(
                    f"{output_filename_prefix}_chunk_{chunk_count + 1}.xlsx",
                    excel_data.getvalue(),
                )
    zip_buffer.seek(0)
    return zip_buffer


if __name__ == "__main__":
    image_file = "/Users/aryan/Downloads/work_demo.gif"
    num_chunks = 1
    num_records = 60
    output_folder = "/Users/aryan/Downloads"
    get_excel_from_image(
        image_file, num_chunks, num_records, "demo", OCR_API_URL, OCR_API_KEY
    )
