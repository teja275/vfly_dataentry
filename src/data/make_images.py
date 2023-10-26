import io
import zipfile

from PIL import Image


def split_image_to_chunks(
    input_image, num_chunks=20, num_records=2500, hpatch_size=1, vpatch_size=1
):
    width, height = input_image.size
    chunk_height = height // num_chunks
    hpatch_height = (height // num_records) * hpatch_size
    vpatch_width = (height // num_records) * vpatch_size

    image_chunks = []

    for i in range(num_chunks):
        left = 0
        right = width
        upper = i * chunk_height
        lower = (i + 1) * chunk_height
        cropped_image = input_image.crop((left, upper, right, lower))
        patched_image = Image.new(
            "RGB",
            (width + 2 * vpatch_width, chunk_height + 2 * hpatch_height),
            (255, 255, 255),
        )
        patched_image.paste(cropped_image, (vpatch_width, hpatch_height))
        image_chunks.append(patched_image)
    return image_chunks


def download_image_chunks(
    input_image_file,
    num_chunks,
    num_records,
    output_filename_prefix,
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
    file_name = "/Users/aryan/Downloads/demo.gif"
    image = Image.open(file_name)
    image_chunks = split_image_to_chunks(
        image, num_chunks=1, num_records=60, hpatch_size=1, vpatch_size=1
    )
    for image in image_chunks:
        image.show()
