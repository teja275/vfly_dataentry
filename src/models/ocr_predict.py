from io import BytesIO

import requests


def get_ocr_response(url, api_key, image_chunk, filename):
    image_chunk = image_chunk.convert("RGB")
    # Convert the PIL Image to bytes
    image_bytes = BytesIO()
    image_chunk.save(image_bytes, format="JPEG")  # Adjust the format if necessary

    # Send the image bytes as a file in the request
    data = {"file": (filename, image_bytes.getvalue())}
    response = requests.post(
        url,
        auth=requests.auth.HTTPBasicAuth(api_key, ""),
        files=data,
    )
    return response
