import os
import requests
import mimetypes

from dotenv import load_dotenv

load_dotenv()
# Replace these with your actual values
ACCESS_TOKEN = os.getenv("META_ACCES_TOKEN")
PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID")
RECIPIENT_NUMBER = os.getenv("RECEPIENT_PHONE_NUMBER")

# File to upload
file_path = os.path.join(os.path.dirname(__file__), "test_image.png")

# Validate file type
mime_type, _ = mimetypes.guess_type(file_path)
# if mime_type not in ["image/jpeg", "image/png", "image/webp"]:
#     raise ValueError(f"Unsupported file type: {mime_type}")

# Upload URL
url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/media"

# Headers
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# Data and Files
data = {
    "messaging_product": "whatsapp"
}
files = {
    "file": (file_path, open(file_path, "rb"), mime_type)
}

# Send POST request to upload
response = requests.post(url, headers=headers, data=data, files=files)

# Check response
print(response.status_code)
print(response.json())
media_id = response.json()["id"]

# Message payload
payload = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT_NUMBER,
    "type": "image",
    "image": {
        "id": media_id,  # Use the media_id obtained from the upload step
        "caption": "Your custom caption here"  # Optional caption
    }
}

# Headers
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Send POST request to send the message
response = requests.post(
    f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages",
    json=payload,
    headers=headers
)

# Check response
print(response.status_code)
print(response.json())

