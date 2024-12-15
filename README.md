# tv_ledbar
A Raspberry Pi, Python based project with 2 modes:
1. LED bar controll to determine the colour of the leds basing on the screen content 
2. Home security:  human detection and remote intrusion information via whatsapp 

## Setup 

## Hardware

## How to get it working

### Setup a Meta Developer's account and a static acces token for whats app message notifications

Use this tutorial for instructions:
https://www.youtube.com/watch?v=Y8kihPdCI_U

### Make a fresh gmail account
1. Make a new gmail account 
2. Setup a 2 step authentication
3. Setup an app password for this google account (we will use this pwd for authentication)
### Make the .env file with content as bellow

'''
RECEPIENT_PHONE_NUMBER="<COUNTRY_CODE><PHONENUMBER>"
META_ACCES_TOKEN = "<PERMANENT_ACCES_TOKEN>"
META_PHONE_NUMBER_ID = "<WHATSAP_PHONE_ID>"
MAIL_EMAIL_ADDRESS = "<YOUR_APP_NEW_EMAIL>"
GMAIL_APP_PASSWORD = "<GMAIL_APP_PWD>"
RECEPIENT_EMAIL = "<RECEPIENT_EMAIL>"
'''

## ZMQ Message topics and message types

### notifier
'''
{
    "whatsapp": {
        "send":bool,
        "message_type":str,
        "text":str,
        "media_path":str
    }
    "email":{
        "send":bool,
        "email_subject":str,
        "email_content":str,
        "atachment_paths":[str,...,str]
    }
}
'''
message_type can be "video","image" or "text"
eg. atachment_paths:["/path/to/file1.png","/path/to/file2.mp4","/path/to/file3.txt"]