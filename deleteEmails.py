#!/usr/bin/env python3
"""
Gmail Bulk Delete Script
Deletes all emails from Inbox and Sent folders
"""

import os.path
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.pickle
SCOPES = ['https://mail.google.com/']

def authenticate_gmail():
    """Authenticate and return Gmail API service"""
    creds = None
    
    # Token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)

def delete_emails_from_label(service, label_name):
    """Delete all emails from a specific label/folder"""
    try:
        print(f"\n{'='*50}")
        print(f"Processing: {label_name}")
        print(f"{'='*50}")
        
        # Get the label ID
        if label_name == 'INBOX':
            label_id = 'INBOX'
        elif label_name == 'SENT':
            label_id = 'SENT'
        else:
            label_id = label_name
        
        deleted_count = 0
        page_token = None
        
        while True:
            # Get messages in batches of 500
            results = service.users().messages().list(
                userId='me',
                labelIds=[label_id],
                maxResults=500,
                pageToken=page_token
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print(f"No more messages found in {label_name}")
                break
            
            print(f"Found {len(messages)} messages in this batch...")
            
            # Delete messages in this batch
            message_ids = [msg['id'] for msg in messages]
            
            # Batch delete (faster than individual deletes)
            batch_delete_request = {
                'ids': message_ids
            }
            
            service.users().messages().batchDelete(
                userId='me',
                body=batch_delete_request
            ).execute()
            
            deleted_count += len(message_ids)
            print(f"Deleted {len(message_ids)} messages (Total: {deleted_count})")
            
            # Check if there are more pages
            page_token = results.get('nextPageToken')
            if not page_token:
                break
        
        print(f"\n✓ Successfully deleted {deleted_count} messages from {label_name}")
        return deleted_count
        
    except HttpError as error:
        print(f"An error occurred: {error}")
        return 0

def main():
    """Main function to delete all emails"""
    print("Gmail Bulk Delete Script")
    print("=" * 50)
    print("⚠️  WARNING: This will permanently delete emails!")
    print("=" * 50)
    
    confirmation = input("\nType 'DELETE ALL' to confirm: ")
    if confirmation != 'DELETE ALL':
        print("Cancelled. No emails were deleted.")
        return
    
    print("\nAuthenticating with Gmail...")
    service = authenticate_gmail()
    print("✓ Authentication successful!")
    
    # Delete from Inbox
    inbox_deleted = delete_emails_from_label(service, 'INBOX')
    
    # Delete from Sent
    sent_deleted = delete_emails_from_label(service, 'SENT')
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Inbox emails deleted: {inbox_deleted}")
    print(f"Sent emails deleted: {sent_deleted}")
    print(f"Total emails deleted: {inbox_deleted + sent_deleted}")
    print("\n✓ Process complete!")

if __name__ == '__main__':
    main()
