from typing import List, Dict
from user_data.user_data import UserData
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DeviceData:
    """Manages device-related data and generates events."""

    def __init__(self, user: UserData):
        self.user = user

    def generate_events(self, current_time: datetime) -> List[str]:
        """Generates events based on the user's location and upcoming events."""
        current_location = self.user.get_current_location(current_time)
        
        # Retrieve upcoming events within the next 2 hours
        upcoming_events = self.user.get_upcoming_events(hours=2, current_time=current_time)

        # Start the events list with the current location message
        events = [f"{self.user.name} is currently at {current_location}"]

        for event in upcoming_events:
            # Parse event date and time from the event dictionary
            event_time = datetime.strptime(f"{event['date']} {event['time']}", "%Y-%m-%d %H:%M")
            
            # Calculate the time difference between the event time and current time
            time_diff = event_time - current_time
            
            # Convert the time difference to minutes
            minutes_until = int(time_diff.total_seconds() / 60)
            
            # Append the upcoming event message to the events list
            events.append(f"Upcoming event in {minutes_until} minutes: {event['event']}")
            logging.info(f"[Event Notification] Upcoming event in {minutes_until} minutes: {event['event']}")
        
        # Return the complete list of events
        return events
