# Tutorial for Reference: https://www.thepythoncode.com/article/use-gmail-api-in-python#Enabling_Gmail_API
import os
import pickle
import sys
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

class email_handler:
    SCOPES = ['https://mail.google.com/']
    email = ''
    working_directory = '.'#; depends on your local computer
    service = None
    
    def __init__(self):
        self.service = self.gmail_authenticate() #get the Gmail API service
        self.email = self.service.users().getProfile(userId = 'me').execute()['emailAddress']
        
    def gmail_authenticate(self):
        creds = None
        # The file token.json stores the user authentication token.
        # If there is an existing token, load it.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If a token does not exist, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
                
        service = build('gmail', 'v1', credentials=creds)
        return service

    def send_message(self, message_dict):
        message = MIMEText(message_dict['body'])
        message['to'] = message_dict['to']
        message['from'] = self.email
        message['subject'] = message_dict['subject']
        raw_message = {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
        
        return self.service.users().messages().send(
          userId="me",
          body= raw_message
        ).execute()
    
    def getMessages(self, labels = ['INBOX'], amount = 10):
        #get amount emails with the labels specified
        msgList = self.service.users().messages().list(userId='me',
                labelIds = labels, maxResults = amount).execute() 
        messages = msgList['messages'] #retrieve the messages

        emails = []

        for msg in messages:
            email = self.service.users().messages().get(userId = 'me', id=msg['id'], format='full').execute()
            temp_email = {}
            for head in email['payload']['headers']:
                if (head.get("name") == 'From'):
                    from_info = head.get('value').split(" <")
                    if (len(from_info) > 1):
                        from_info[1] = from_info[1][0:-1]
                    else:
                        from_info*=2
                    temp_email['from name'] = from_info[0]
                    temp_email['from email'] = from_info[1]
                    

                if(head.get('name') == 'Subject'):
                    temp_email['subject'] = head.get('value')
                
                if (head.get("name") == 'Date'):
                    temp_date = head.get('value').split(' ')
                    temp_email['date'] =  temp_date[1] + ' ' + temp_date[2] + ' ' + temp_date[3] 

            snip = email['snippet']
            if (len (snip) > 30):
                snip = snip[0:30] + '...'
            
            temp_email['snippet'] =  snip

            emails.append(temp_email)
        
        return emails    
        #print(emails)

if __name__ == "__main__":
    email_hand = email_handler()
    print(email_hand.getMessages(amount = 10))

        
        




