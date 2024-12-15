import zmq
import yagmail

from zmq_class import ZMQClass

class Notifier(ZMQClass):
    """This class is used to notify the user about homie intrusion via Whatsapp"""
    def __init__(self, pub_port, sub_port, sub_topics):
        self.super().__init__(pub_port, sub_port, sub_topics)
        
        # Load enviromental variables for Whatsapp notifications
        load_dotenv()
        self.ACCESS_TOKEN = os.getenv("META_ACCES_TOKEN")
        self.PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID")
        self.RECIPIENT_NUMBER = os.getenv("RECEPIENT_PHONE_NUMBER")
        self.GMAIL_EMAIL_ADDRESS = os.getenv("GMAIL_EMAIL_ADDRESS")
        self.GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
        self.RECEPIENT_EMAIL = os.getenv("RECEPIENT_EMAIL")

        self.yag = yagmail.SMTP(self.GMAIL_EMAIL_ADDRESS, self.GMAIL_APP_PASSWORD)


    def work(self):
        while True:
            topic, message = self.poll_messages()
            if topic == "notifier":
                try:
                    message_json = json.loads(message)
                    self.handle_notifier_message(message_json)
                except json.JSONDecodeError:
                    print("Invalid JSON received")

    def handle_notifier_message(self, message_json):
        if(message_json["whatsapp"]["send"]):
            if(message_json["whatsapp"]["message_type"] == "text"):
                response = self.send_whatsapp_plain_text(message_json["whatsapp"]["text"])

            elif(message_json["whatsapp"]["message_type"] == "video" ormessage_json["whatsapp"]["message_type"] == "image"):
                response, media_id = self.upload_media_to_meta(message_json["whatsapp"]["media_path"], 
                                                                message_json["whatsapp"]["message_type"])
                if (response == 200):
                    response = self.send_whatsapp_media_text(message_json["whatsapp"]["text"], 
                                                            media_id, 
                                                            message_json["whatsapp"]["message_type"])
            if(response == 200):
                self.send_notifier_response('{"type": "whatsapp","sending_status":true}')
            else:
                self.send_notifier_response('{"type": "whatsapp","sending_status":false}')

        if(message_json["email"]["send"]):
            try:
                self.send_email(message_json["email"]["email_subject"],
                                message_json["email"]["email_content"], 
                                message_json["email"]["atachment_paths"])
                self.send_notifier_response('{"type": "email","sending_status":true}')
            except:
                self.send_notifier_response('{"type": "email","sending_status":false}')


    def send_notifier_response(self, response_string):
        topic = "notifier_response"
        message = response_string.encode()
        self.socket_pub.send_multipart([topic.encode(), message.encode()])


    def send_whatsapp_plain_text(self, text):
        """Send a whatsapp text message"""
        payload = {
            "messaging_product": "whatsapp",
            "to": RECIPIENT_NUMBER,  # WhatsApp phone number in international format
            "type": "text",
            "text": {
                "body": text
                }
            }
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
            }
        response = requests.post(
            f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages",
            json=payload,
            headers=headers
            )
        return response.status_code

    def send_whatsapp_media_text(self, text, media_id, media_type):
        """Send file up to 16MB and a adjusted text message"""

        payload = {
            "messaging_product": "whatsapp",
            "to": self.RECIPIENT_NUMBER,
            "type": media_type,
            "video": {
                "id": media_id,
                "caption": text  
            }
        }

        headers = {
            "Authorization": f"Bearer {self.ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            f"https://graph.facebook.com/v21.0/{self.PHONE_NUMBER_ID}/messages",
            json=payload,
            headers=headers
        )
        return response.status_code

        

    def upload_media_to_meta(self, media_path, media_type):
        # Validate file type
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type not in ["video/mp4", "video/3gpp","image/jpeg", "image/png", "image/webp"]:
            raise ValueError(f"Unsupported file type: {mime_type}")

        url = f"https://graph.facebook.com/v21.0/{self.PHONE_NUMBER_ID}/media"
        
        headers = {
            "Authorization": f"Bearer {self.ACCESS_TOKEN}"
            }
        data = {
            "messaging_product": "whatsapp"
            }
        files = {
            "file": (media_path, open(media_path, "rb"), mime_type)
            }
        response = requests.post(url, headers=headers, data=data, files=files)
        
        if response.status_code == 200:
            media_id = response.json().get("id")
        else:
            raise Exception(f"Failed to upload media: {response.json()}")
        
        return response.status_code, media_id
    
    def send_email(self, subject, body, list_attachemnt_paths = []):
        if type(list_attachemnt_paths) is list:
            attachments = list_attachemnt_paths
        else:
            attachments = []
        
        send_ret = self.yag.send(
                                to=RECEPIENT_EMAIL,
                                subject=subject,
                                contents=body,
                                attachments=attachments
                                )
        return send_ret

if __name__ == "__main__":
    # Get project configuration
    file_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(file_path, "r") as file:
            config_json = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON: {e}")
    except FileNotFoundError:
        print("File not found.")
    
    pub_port = config_json["zmq_pub_socket"]
    sub_port = config_json["zmq_sub_socket"]
    sub_topics = ["notifier"]

    notifier = Notifier(pub_port, sub_port, sub_topics)

    notifier.work()