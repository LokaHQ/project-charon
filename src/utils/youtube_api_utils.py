from googleapiclient.discovery import build
import isodate
import os


class YouTubeMonitor:
    def __init__(self):
        """Initialize the YouTube API client with the API key."""
        api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def get_recent_videos(self, channel_id: str, limit: int = 10):
        """Fetch recent videos from a YouTube channel"""
        # Get uploads playlist ID
        channel_response = (
            self.youtube.channels().list(part="contentDetails", id=channel_id).execute()
        )

        uploads_playlist = channel_response["items"][0]["contentDetails"][
            "relatedPlaylists"
        ]["uploads"]

        playlist_response = (
            self.youtube.playlistItems()
            .list(part="snippet", playlistId=uploads_playlist, maxResults=limit)
            .execute()
        )

        video_ids = [
            item["snippet"]["resourceId"]["videoId"]
            for item in playlist_response["items"]
        ]

        videos_response = (
            self.youtube.videos()
            .list(part="snippet,contentDetails,statistics", id=",".join(video_ids))
            .execute()
        )

        return videos_response["items"]


def parse_duration_to_minutes(duration_str):
    """Convert YouTube duration (PT4M13S) to minutes"""
    duration = isodate.parse_duration(duration_str)
    return duration.total_seconds() / 60
