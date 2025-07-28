import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.append(str(Path(__file__).parent.parent))
from src.tools.celander_tools import create_event


@patch("src.utils.google_calendar_auth.authenticate_calendar")
def test_create_event_success(mock_auth):
    """Test that event creation returns success status and correct message."""

    mock_service = Mock()
    mock_events = Mock()
    mock_insert = Mock()

    mock_auth.return_value = mock_service
    mock_service.events.return_value = mock_events
    mock_events.insert.return_value = mock_insert
    mock_insert.execute.return_value = {"id": "some_id", "htmlLink": "some_link"}

    test_event = {
        "title": "Test Meeting",
        "start_time": "2025-07-29T10:00:00",
        "end_time": "2025-07-29T11:00:00",
        "description": "Test description",
        "location": "Test location",
    }

    result = create_event(**test_event)

    assert result.status == "success"
    assert result.message == "Event created successfully"

    print(f"✅ Test passed! Status: {result.status}, Message: {result.message}")


if __name__ == "__main__":
    test_create_event_success()
    print("🎉 All tests passed!")
