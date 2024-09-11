import json
import csv
from typing import List, Dict, Any
from datetime import datetime, timedelta


class UserData:
    """Manages user-related data and provides methods to access and manipulate it."""

    def __init__(self, name: str):
        self.name = name
        # Load user profile and data from various sources
        self.profile: Dict[str, Any] = self.load_profile()
        self.location_data: List[Dict[str, str]] = self.load_location_data()
        self.calendar: List[Dict[str, str]] = self.load_calendar()
        self.social_media: Dict[str, Any] = self.load_social_media()
        self.spotify_playlists: Dict[str, Any] = self.load_spotify_playlists()

    def load_profile(self) -> Dict[str, Any]:
        """Loads user profile from JSON file."""
        with open(f"data/user_data/user_profile.json", "r") as f:
            return json.load(f)

    def load_location_data(self) -> List[Dict[str, str]]:
        """Loads location data from CSV file."""
        locations = []
        with open(f"data/device_data/location.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                locations.append(row)  # Append each location row to the list
        return locations

    def load_calendar(self) -> List[Dict[str, str]]:
        """Loads calendar data from CSV file."""
        events = []
        with open(f"data/device_data/calendar.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                events.append(row)  # Append each event row to the list
        return events

    def load_social_media(self) -> Dict[str, Any]:
        """Loads social media data from JSON file."""
        with open(f"data/user_data/social_media.json", "r") as f:
            return json.load(f)

    def load_spotify_playlists(self) -> Dict[str, Any]:
        """Loads Spotify playlists data from JSON file."""
        with open(f"data/user_data/spotify_playlists.json", "r") as f:
            return json.load(f)

    def get_current_location(self, current_time: datetime = None) -> str:
        """Gets the user's current location based on the given time."""
        if current_time is None:
            current_time = datetime.now()  # Use current time if not provided

        current_location = "Unknown"  # Default location
        latest_time = datetime.min  # Initialize latest time

        # Iterate through location data to find the most recent location
        for location in self.location_data:
            loc_time = datetime.strptime(location["timestamp"], "%Y-%m-%d %H:%M:%S")

            if loc_time <= current_time and loc_time > latest_time:
                latest_time = loc_time
                current_location = location["location"]  # Update current location

        return current_location

    def get_upcoming_events(
        self, hours: int = 2, current_time: datetime = None
    ) -> List[Dict[str, str]]:
        """Gets upcoming events within the specified number of hours from the current time.

        The default 2-hour window is chosen to show soon-to-happen events
        without listing too many future ones. This helps keep the information
        relevant and not overwhelming for the user.
        """
        if current_time is None:
            current_time = datetime.now()  # Use current time if not provided

        upcoming = []  # List to hold upcoming events

        for event in self.calendar:
            event_time = datetime.strptime(
                f"{event['date']} {event['time']}", "%Y-%m-%d %H:%M"
            )
            if current_time <= event_time and event_time <= current_time + timedelta(hours=hours):
                upcoming.append(event)  # Add event to upcoming list if within range
        return upcoming
