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
        self.myemail = self.service.users().getProfile(userId = 'me').execute()['emailAddress']
        
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

    def createEmailMessage(self, message_dict):
        message = MIMEText(message_dict['body'])
        message['to'] = message_dict['to']
        message['from'] = self.myemail
        message['subject'] = message_dict['subject']
        message['cc'] = message_dict['cc']
        message['bcc'] = message_dict['bcc']
        raw_message = {'raw': urlsafe_b64encode(message.as_bytes()).decode()} #encode message
        return raw_message
    
    def send_message(self, message_dict):
        self.service.users().messages().send(userId="me",
        body= self.createEmailMessage(message_dict)).execute()
        
    def cleanTxt(self, txt):
        cleantxt = ''
        firstChar = False

        for c in txt:
            if firstChar:
                cleantxt += c
            else:
                if c != ' ':
                    cleantxt += c
                    firstChar = True
        return cleantxt
            
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
                    #print(head.get('value'))
                    from_info = head.get('value').split(" <")
                    if (len(from_info) > 1):
                        from_info[1] = from_info[1][0:-1]
                    else:
                        from_info*=2
                    temp_email['from name'] = self.cleanTxt(from_info[0].replace('"', ' '))
                    temp_email['from email'] = from_info[1]
                    

                if(head.get('name') == 'Subject'):
                    temp_email['subject'] = head.get('value')
                
                if (head.get("name") == 'Date'):
                    temp_date = head.get('value').split(' ')
                    temp_email['date'] =  temp_date[1] + ' ' + temp_date[2] + ' ' + temp_date[3] 

            temp_email['snippet'] =  email['snippet']

            emails.append(temp_email)
        
        return emails 

if __name__ == "__main__":
    email_hand = email_handler()
    email_message = {
        'to':'',
        'subject':'',
        'body':'',
        }
    user_choice = 0
    while user_choice != '-1':
        print('-1: Exit\n',
              '0 : Send Email\n')
        
        user_choice = input('What do you want to do?\n')
        if user_choice == '-1':
            continue
        elif user_choice == '0':
            email_message['to'] = input('What is the email address you are sending an email to?\n')
            email_message['subject'] = input('What is the subject of this email?\n')
            email_message['body'] = input('What is the body of this email?\n')

            email_hand.send_message(email_message)
        
        




