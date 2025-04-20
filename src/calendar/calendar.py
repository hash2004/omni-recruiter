import datetime
import os.path
from typing import List

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service(creds_path: str = 'credentials.json',
                         token_path: str = 'token.json') -> object:
    """
    Authenticate and return a Calendar API service object.
    """
    creds = None
    # Load saved user credentials
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If no valid creds, go through OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for next run
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def create_event_and_invite(service,
                            summary: str,
                            description: str,
                            start_dt: datetime.datetime,
                            end_dt: datetime.datetime,
                            timezone: str,
                            attendee_emails: List[str],
                            calendar_id: str = 'primary') -> dict:
    """
    Create a Calendar event with attendees and send invitations.
    """
    event_body = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': timezone,
        },
        'attendees': [{'email': email} for email in attendee_emails],
        # ensure invites are sent
        'reminders': {
            'useDefault': True,
        },
    }

    created = service.events().insert(
        calendarId=calendar_id,
        body=event_body,
        sendUpdates='all'   # 'all' | 'externalOnly' | 'none'
    ).execute()

    return created

if __name__ == '__main__':
    # 1) Authenticate & build service
    service = get_calendar_service()

    # 2) Define your event
    now = datetime.datetime.utcnow()
    start = now + datetime.timedelta(days=1)
    end = start + datetime.timedelta(hours=1)

    event = create_event_and_invite(
        service=service,
        summary='Project Kick‑Off',
        description='Discuss roadmap and milestones.',
        start_dt=start,
        end_dt=end,
        timezone='Asia/Karachi',
        attendee_emails=['colleague@example.com', 'client@example.org']
    )

    print(f"Event created: {event.get('htmlLink')}")
