import os
import requests
from dotenv import load_dotenv

load_dotenv()
# Replace these with your actual values
ACCESS_TOKEN = os.getenv("META_ACCES_TOKEN")
PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID")
RECIPIENT_NUMBER = os.getenv("RECEPIENT_PHONE_NUMBER")

# API endpoint
url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"

# Message payload
payload = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT_NUMBER,
    "type": "template",
    "template": {
        "name": "hello_world",  # Template name from Meta configuration
        "language": {
            "code": "en_US"  # Template language
        }
    }
}

# Headers
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, json=payload, headers=headers)

# Print the response
print(response.status_code)  # Should be 200 for success
print(response.json())  # For detailed response