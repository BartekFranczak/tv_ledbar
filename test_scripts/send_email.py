import os
from dotenv import load_dotenv
import yagmail

load_dotenv()
GMAIL_EMAIL_ADDRESS = os.getenv("GMAIL_EMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RECEPIENT_EMAIL = os.getenv("RECEPIENT_EMAIL")

# Initialize yagmail
yag = yagmail.SMTP(GMAIL_EMAIL_ADDRESS, GMAIL_APP_PASSWORD)

# Email content
subject = "Test Email with Attachments"
body = "Hello, this email has attachments."

# Attachments
file_path_1 = os.path.join(os.path.dirname(__file__), "test_image.png")
file_path_2 = os.path.join(os.path.dirname(__file__), "test_video.mp4")

attachments = [file_path_1, file_path_2] 

# Send the email
response = yag.send(
    to=RECEPIENT_EMAIL,
    subject=subject,
    contents=body,
    attachments=attachments
)
print(response)

print("Email sent successfully!")
