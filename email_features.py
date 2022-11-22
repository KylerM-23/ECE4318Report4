# Tutorial for Reference: https://www.thepythoncode.com/article/use-gmail-api-in-python#Enabling_Gmail_API
import os
import pickle
import sys
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
our_email = 'bobthebuilder420@gmail.com'
working_directory = '.'#; depends on your local computer
#working_directory=r'C:\Users\lyndo\Downloads\ECE4318\gmail_api'
#os.chdir(working_directory)

def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists(working_directory+"\\token.pickle"):
        with open(working_directory+"\\token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(working_directory+'\\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open(working_directory+"\\token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

# get the Gmail API service
service = gmail_authenticate()

# Adds the attachment with the given filename to the given message
def add_attachment(message, filename):
    '''
    Adds attachments to email (called in build_message())
    
    Args:
        message (instance of MIMEText or MIMEMultipart) 
        attachments (list of string): email attachments; example: ['pic.png', 'text.txt', 'docum.pdf']
    '''
    content_type, encoding = guess_mime_type(filename)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(filename, 'rb')
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(filename, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(filename, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(filename, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

def build_message(destination, cc, bcc, obj, body, attachments=[]):
    '''
    Build and encode the email message (called in send_message())
    
    Args:
        destination (string of email address list): email address being send to; examples: "CEOofMcDonald@gmail.com" or "mushroom@gmail.com,market@gmail.com,mochi@gmail.com"
        cc (string of email address list): example: "mushroom@gmail.com,market@gmail.com,mochi@gmail.com"
        bcc (string of email address list): example: "mushroom@gmail.com,market@gmail.com,mochi@gmail.com"
        obj (string): the subject/title of the email
        body (string): the body/main content of the email
        attachments (list of string): email attachments; example: ['pic.png', 'text.txt', 'docum.pdf']
    '''
    #for cc/bcc https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python
    if not attachments: # no attachments given
        message = MIMEText(body)
        message['to'] = destination
        message['cc'] = cc
        message['bcc'] = bcc
        message['from'] = our_email
        message['subject'] = obj
    else:
        message = MIMEMultipart()
        message['to'] = destination
        message['cc'] = cc
        message['bcc'] = bcc
        message['from'] = our_email
        message['subject'] = obj
        message.attach(MIMEText(body))
        for filename in attachments:
            add_attachment(message, working_directory+"\\"+filename)
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, destination, cc, bcc, obj, body, attachments=[]):
    '''
    Build and send email message
    
    Args:
        service: comes from this 'service = gmail_authenticate()'
        destination (string): email address being send to
        cc (string of email address list): example: "mushroom@gmail.com,market@gmail.com,mochi@gmail.com"
        bcc (string of email address list): example: "mushroom@gmail.com,market@gmail.com,mochi@gmail.com"
        obj (string): the subject/title of the email
        body (string): the body/main content of the email
        attachments (list of string): email attachments; example: ['pic.png', 'text.txt', 'docum.pdf']
    '''
    return service.users().messages().send(
      userId="me",
      body=build_message(destination, cc, bcc, obj, body, attachments)
    ).execute()

def search_messages(service, query):
    '''
    Search email messages (widely called because of usefulness)
    returns list of message-related objects; each objects matched the search query
    
    Args:
        service: comes from this 'service = gmail_authenticate()'
        query (string): search query; the thing you type in a search bar
    '''
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

# utility functions
def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format (called in parse_parts())
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"
def clean(text):
    '''
    clean text (no spaces/special characters) for creating a folder (called in read_message(), which creates folders when reading emails)
    
    Args:
        text (path)
    '''
    return "".join(c if c.isalnum() else "_" for c in text)
def parse_parts(service, parts, folder_name, message):
    """
    Parses the content of an email partition and save any HTML files into folders (called in read_message())
    Most of the time, the email message body should be in the 'text' variable in the "text/plain" block
    
    Args:
        service: comes from this 'service = gmail_authenticate()'
        parts: comes from 'parts = payload.get("parts")' in read_message()
        folder_name (path of folder_name)
        message: an input to read_message(), input was generated by search_messages()
    """
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                parse_parts(service, part.get("parts"), folder_name, message)
            if mimeType == "text/plain":
                # if the email part is text plain
                if data:
                    text = urlsafe_b64decode(data).decode()
                    print(text)
            elif mimeType == "text/html":
                # if the email part is an HTML content
                # save the HTML file and optionally open it in the browser
                if not filename:
                    filename = "index.html"
                filepath = os.path.join(folder_name, filename)
                print("Saving HTML to", filepath)
                with open(filepath, "wb") as f:
                    f.write(urlsafe_b64decode(data))
            else:
                # attachment other than a plain text or HTML
                for part_header in part_headers:
                    part_header_name = part_header.get("name")
                    part_header_value = part_header.get("value")
                    if part_header_name == "Content-Disposition":
                        if "attachment" in part_header_value:
                            # we get the attachment ID 
                            # and make another request to get the attachment itself
                            print("Saving the file:", filename, "size:", get_size_format(file_size))
                            attachment_id = body.get("attachmentId")
                            attachment = service.users().messages() \
                                        .attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                            data = attachment.get("data")
                            filepath = os.path.join(folder_name, filename)
                            if data:
                                with open(filepath, "wb") as f:
                                    f.write(urlsafe_b64decode(data))

def read_message(service, message):
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
        - Most email informations like dates and subject can be founded here; the email message body is founded in parse_parts()
        
    Args:
        service: comes from this 'service = gmail_authenticate()'
        message: comes from search_messages(); search_messages() may return multiple messages, so for-loop may be needed to read each message 1-by-1
    """
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = working_directory+"\\email"
    has_subject = False
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                # we print the From address
                print("From:", value)
            if name.lower() == "to":
                # we print the To address
                print("To:", value)
            if name.lower() == "subject":
                # make our boolean True, the email has "subject"
                has_subject = True
                # make a directory with the name of the subject
                folder_name = clean(working_directory+"\\"+value)
                # we will also handle emails with the same subject name
                folder_counter = 0
                while os.path.isdir(folder_name):
                    folder_counter += 1
                    # we have the same folder name, add a number next to it
                    if folder_name[-1].isdigit() and folder_name[-2] == "_":
                        folder_name = f"{folder_name[:-2]}_{folder_counter}"
                    elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                        folder_name = f"{folder_name[:-3]}_{folder_counter}"
                    else:
                        folder_name = f"{folder_name}_{folder_counter}"
                os.mkdir(folder_name)
                print("Subject:", value)
            if name.lower() == "date":
                # we print the date when the message was sent
                print("Date:", value)
    if not has_subject:
        # if the email does not have a subject, then make a folder with "email" name
        # since folders are created based on subjects
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
    parse_parts(service, parts, folder_name, message)
    print("="*50)

def mark_as_read(service, query):
    '''
    Search for and mark email messages as read
    
    Args:
        service: comes from this 'service = gmail_authenticate()'
        query (string): search query; the thing you type in a search bar
    '''
    messages_to_mark = search_messages(service, query)
    print(f"Matched emails: {len(messages_to_mark)}")
    return service.users().messages().batchModify(
      userId='me',
      body={
          'ids': [ msg['id'] for msg in messages_to_mark ],
          'removeLabelIds': ['UNREAD']
      }
    ).execute()

def mark_as_unread(service, query):
    '''
    Search for and mark email messages as unread
    
    Args:
        service: comes from this 'service = gmail_authenticate()'
        query (string): search query; the thing you type in a search bar
    '''
    messages_to_mark = search_messages(service, query)
    print(f"Matched emails: {len(messages_to_mark)}")
    # add the label UNREAD to each of the search results
    return service.users().messages().batchModify(
        userId='me',
        body={
            'ids': [ msg['id'] for msg in messages_to_mark ],
            'addLabelIds': ['UNREAD']
        }
    ).execute()

def delete_messages(service, query):
    '''
    Search for and delete email messages
    
    Args:
        service: comes from this 'service = gmail_authenticate()'
        query (string): search query; the thing you type in a search bar
    '''
    messages_to_delete = search_messages(service, query)
    # it's possible to delete a single message with the delete API, like this:
    # service.users().messages().delete(userId='me', id=msg['id'])
    # but it's also possible to delete all the selected messages with one query, batchDelete
    return service.users().messages().batchDelete(
      userId='me',
      body={
          'ids': [ msg['id'] for msg in messages_to_delete]
      }
    ).execute()

if __name__ == "__main__":
    email_source = input('What is the email address you are signing in to?\n')
    our_email = email_source
    user_choice = 0
    while user_choice != '-1':
        print('-1: Exit\n',
              '0 : Change Source Email\n',
              '1 : Send Email\n',
              '2 : Read Email\n',
              '3 : Delete Email\n',
              '4 : Mark Email Read\n', 
              '5 : Mark Email Unread')
        user_choice = input('What do you want to do? (0-5, or -1 to exit)\n')
        if user_choice == '-1':
            continue
        elif user_choice == '0':
            email_source = input('What is the email address you are signing in to?\n')
            our_email = email_source

        elif user_choice == '1':
            email_destination = input('What are the email addresses you are sending an email to (format like: mushroom@gmail.com,market@gmail.com,mochi@gmail.com)?\n')
            email_cc = input('What are the email addresses you are CCing to (format like: mushroom@gmail.com,market@gmail.com,mochi@gmail.com)?\n')
            email_bcc = input('What are the email addresses you are BCCing to (format like: mushroom@gmail.com,market@gmail.com,mochi@gmail.com)?\n')
            email_subject = input('What is the subject of this email?\n')
            email_body = input('What is the body of this email?\n')
            email_attachments = [] #attached files must be in the working directory
            attachment = ''
            while attachment.lower() != "none":
                attachment = input('Enter one-by-one, what are the file name of the attachment to this email (type "None" to stop adding attachments)?\n')
                if attachment.lower() != "none":
                    email_attachments.append(attachment)
            send_message(service=service, 
                         destination=email_destination,
                         cc=email_cc,
                         bcc=email_bcc,
                         obj=email_subject, #subject; objective
                         body=email_body,
                         attachments=email_attachments
                        )

        elif user_choice == '2':
            search_query = input('What emails do you want to read?\n')
            results = search_messages(service, search_query)
            print(f"Found {len(resutls)} results.\n")
            for msg in results:
                read_message(service, msg)

        elif user_choice == '3':
            search_query = input('What emails do you want to delete?\n')
            delete_messages(service, search_query)

        elif user_choice == '4':
            search_query = input('What emails do you want to mark as read?\n')
            mark_as_read(service, search_query)

        elif user_choice == '5':
            search_query = input('What emails do you want to mark as unread?\n')
            mark_as_unread(service, search_query)

        else:
            print("Invalid Choice\n")
        
        

