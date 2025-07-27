import os
import json
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pytz
from strands import tool

# Scopes for google calendar API
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar",
]


# Google calendar Authentication
def authenticate_calendar():
    creds = None
    if os.path.exists("google_credentials.json"):
        creds = Credentials.from_authorized_user_file("google_credentials.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("google_credentials.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


# Function calling to get calendar events within a specified duration
@tool
def get_events(duration: str = "") -> str:
    """
    Retrieves events from Google Calendar within a specified time period.
    If no duration is specified, it retrieves events for the current week.
    Args:
        duration (str): The duration in days for which to retrieve events. Must be in numeric
    Returns:
        str: A JSON string containing the list of events with their start and end times, and summaries."""
    import json

    service = authenticate_calendar()

    now = datetime.now()

    if duration == "":
        start_of_week = now - timedelta(days=now.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        time_min = start_of_week.isoformat() + "Z"
        time_max = end_of_week.isoformat() + "Z"
    else:
        time_min = now.isoformat() + "Z"
        time_max = (now + timedelta(days=int(duration))).isoformat() + "Z"

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    events_list = []
    for event in events:
        event_data = {
            "start": event["start"].get("dateTime", event["start"].get("date")),
            "end": event["end"].get("dateTime", event["end"].get("date")),
            "summary": event.get("summary", "No Title"),
        }
        events_list.append(event_data)

    return json.dumps(events_list)


# Function calling to create an event in calandar
@tool
def create_event(
    title: str,
    start_time: str,
    end_time: str,
    description: str = "",
    location: str = "",
) -> str:
    """
    Schedules a new event in Google Calendar.
    Args:
        title (str): The title of the event.
        start_time (str): The start time of the event in 'YYYY-MM-DDTHH:MM:SS' format.
        end_time (str): The end time of the event in 'YYYY-MM-DDTHH:MM:SS' format.
        description (str, optional): The description of the event.
        location (str, optional): The location of the event.
    Returns:
        str: A JSON string containing the link to the created event or an error message.
    """
    try:
        service = authenticate_calendar()

        timezone = "Europe/Berlin"  # GMT+1 timezone
        tz = pytz.timezone(timezone)

        # Parse and localize times
        start_time = tz.localize(datetime.fromisoformat(start_time))
        end_time = tz.localize(datetime.fromisoformat(end_time))

        event = {
            "summary": title,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": timezone,  # Fixed: use actual timezone
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": timezone,  # Fixed: use actual timezone
            },
        }

        created_event = (
            service.events().insert(calendarId="primary", body=event).execute()
        )

        # Return a properly formatted response
        result = {
            "status": "success",
            "message": "Event created successfully",
            "event_link": created_event.get("htmlLink"),
            "event_id": created_event.get("id"),
        }
        return json.dumps(result)

    except Exception as e:
        # Return proper error JSON
        error_result = {
            "status": "error",
            "message": f"Failed to create event: {str(e)}",
        }
        return json.dumps(error_result)
