from io import BytesIO
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_ocr_response(url, api_key, image_chunk, filename):
    # Create a session with retry settings
    session = requests.Session()
    retry = Retry(
        total=3,  # Maximum number of retries
        backoff_factor=0.5,  # Exponential backoff factor for delay between retries
        status_forcelist=[500, 502, 503, 504],  # HTTP status codes to retry on
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    image_chunk = image_chunk.convert("RGB")
    # Convert the PIL Image to bytes
    image_bytes = BytesIO()
    image_chunk.save(image_bytes, format="JPEG")  # Adjust the format if necessary

    # Send the image bytes as a file in the request
    data = {"file": (filename, image_bytes.getvalue())}

    try:
        response = session.post(
            url,
            auth=requests.auth.HTTPBasicAuth(api_key, ""),
            files=data,
        )
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.exceptions.RequestException as e:
        # Handle or log the exception as needed
        print(f"Request failed: {str(e)}")
        response = None

    return response
