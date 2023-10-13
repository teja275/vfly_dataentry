from PIL import Image


def split_image_to_chunks(
    input_image, num_chunks=20, num_records=2500, add_patch=False
):
    width, height = input_image.size
    chunk_height = height // num_chunks
    record_height = height // num_records

    image_chunks = []

    for i in range(num_chunks):
        left = 0
        right = width
        upper = i * chunk_height
        lower = (i + 1) * chunk_height

        if i > 0:
            upper = upper - record_height

        if add_patch:
            # Create a white patch image
            patch = Image.new("RGB", (width, record_height), (255, 255, 255))

            # Add the white patch to the top and bottom
            chunk = Image.new(
                "RGB", (width, chunk_height + 2 * record_height), (255, 255, 255)
            )
            chunk.paste(patch, (0, 0))
            chunk.paste(
                input_image.crop((left, upper, right, lower)), (0, record_height)
            )
        else:
            chunk = input_image.crop((left, upper, right, lower))
        image_chunks.append(chunk)
    return image_chunks
