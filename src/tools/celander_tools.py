import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytz
from strands import tool

sys.path.append(str(Path(__file__).parent.parent))
from loguru import logger

from src.schemas.calendar_agent_returns_schema import (
    CalendarCreationReturn,
    CalendarEventInput,
    CalendarEventResponse,
    CalendarEventsListResponse,
)
from src.utils.google_calendar_auth import authenticate_calendar


# Function calling to get calendar events within a specified duration
@tool(
    name="get_events",
    description="Retrieve events from Google Calendar within a specified time period",
)
def get_events(duration: str = "") -> CalendarEventsListResponse:
    """
    Retrieves events from Google Calendar within a specified time period.
    If no duration is specified, it retrieves events for the current week.
    Args:
        duration (str): The duration in days for which to retrieve events. Must be in numeric. For example, if it is 2, it will return events for the next 2 days.
    Returns:
        CalendarEventsListResponse: A structured response containing a list of events, total count, and any error messages."""
    try:
        service = authenticate_calendar()

        now = datetime.now()

        if duration == "":
            start_of_week = now - timedelta(days=now.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            time_min = start_of_week.isoformat() + "Z"
            time_max = end_of_week.isoformat() + "Z"

            logger.info(
                f"Retrieving events for the week starting {start_of_week} to {end_of_week}."
            )
        else:
            time_min = now.isoformat() + "Z"
            time_max = (now + timedelta(days=int(duration))).isoformat() + "Z"

            logger.info(
                f"Retrieving events for the next {duration} days starting from {now.date()}."
            )

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

        logger.info(f"Retrieved {len(events)} events from Google Calendar.")

        # Convert to Pydantic models
        events_list = []
        for event in events:
            event_response = CalendarEventResponse(
                start=event["start"].get("dateTime", event["start"].get("date")),
                end=event["end"].get("dateTime", event["end"].get("date")),
                summary=event.get("summary", "No Title"),
            )
            events_list.append(event_response)

        logger.success(f"Successfully retrieved {len(events_list)} events.")

        return CalendarEventsListResponse(
            events=events_list, total_count=len(events_list)
        )

    except Exception as e:
        logger.error(f"Failed to retrieve events: {str(e)}")
        return CalendarEventsListResponse(events=[], total_count=0)


# Function calling to create an event in calandar
@tool(
    name="create_event",
    description="Create a new event in Google Calendar",
    inputSchema=CalendarEventInput.model_json_schema(),
)
def create_event(
    title: str,
    start_time: str,
    end_time: str,
    description: str = "",
    location: str = "",
) -> CalendarCreationReturn:
    """
    Schedules a new event in Google Calendar.
    Args:
        title (str): Title of the event
        start_time (str): Start time of the event in 'YYYY-MM-DDTHH:MM:SS' format
        end_time (str): End time of the event in 'YYYY-MM-DDTHH:MM:SS' format
        description (str, optional): Description of the event
        location (str, optional): Location of the event
    Returns:
        CalendarCreationReturn: A structured response containing the status, message, event link, and event ID.
    """
    logger.debug(
        f"Creating event: {title} from {start_time} to {end_time} at {location}"
    )

    try:
        service = authenticate_calendar()

        logger.info("Authenticated with Google Calendar successfully.")

        timezone = "Europe/Berlin"  # GMT+1 timezone
        tz = pytz.timezone(timezone)

        event_data = CalendarEventInput(
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description,
            location=location,
        )

        # Parse and localize times
        start_time_dt = tz.localize(datetime.fromisoformat(event_data.start_time))
        end_time_dt = tz.localize(datetime.fromisoformat(event_data.end_time))

        event = {
            "summary": event_data.title,
            "location": event_data.location,
            "description": event_data.description,
            "start": {
                "dateTime": start_time_dt.isoformat(),
                "timeZone": timezone,
            },
            "end": {
                "dateTime": end_time_dt.isoformat(),
                "timeZone": timezone,
            },
        }
        logger.debug(f"Event data prepared: {event}")

        created_event = (
            service.events().insert(calendarId="primary", body=event).execute()
        )

        logger.success(f"Event created successfully: {created_event.get('htmlLink')}")

        return CalendarCreationReturn(
            status="success",
            message="Event created successfully",
            event_link=created_event.get("htmlLink", ""),
            event_id=created_event.get("id", ""),
        )

    except Exception as e:
        logger.error(f"Failed to create event: {str(e)}")

        return CalendarCreationReturn(
            status="error",
            message=f"Failed to create event: {str(e)}",
            event_link="",
            event_id="",
        )
