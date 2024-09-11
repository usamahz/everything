import os
import asyncio
import logging

from datetime import datetime, timedelta
from typing import List, Dict
from dotenv import load_dotenv

import openai
from openai.error import OpenAIError

from user_data.user_data import UserData
from device_data.device_data import DeviceData

from .config import Config


class EVERYTHING:
    """
    Main class for the EVERYTHING system.
    Manages user interactions, generates recommendations, and simulates a day.
    """

    def __init__(self, user: UserData, devices: DeviceData, config: Config):
        self.user = user
        self.devices = devices
        self.config = config
        self.tasks: List[str] = []  # List to hold tasks for the day
        self.recommendations: List[
            str
        ] = []  # List to hold recommendations for the user

        load_dotenv()

        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OpenAI API key not found in environment variables")

        logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.llm = None  # Remove LangChain initialization

    async def simulate_day(self) -> None:
        """Simulates a day in the user's life with EVERYTHING AI."""
        current_date = datetime.now().date()
        start_time = datetime.combine(current_date, self.config.SIMULATION_START_TIME)
        end_time = datetime.combine(current_date, self.config.SIMULATION_END_TIME)
        current_time = start_time

        await self.start_day(start_time)

        while current_time <= end_time:
            await self.process_time(current_time)
            current_time += timedelta(minutes=self.config.SIMULATION_INTERVAL)

        await self.end_day(end_time)

    async def process_time(self, current_time: datetime) -> None:
        """Processes events and generates recommendations for the current time."""
        events = self.devices.generate_events(
            current_time
        )  # Generate events for the current time
        for event in events:
            await self.handle_event(event, current_time)  # Handle each event

        # Generate recommendations at the start of each recommendation hour
        if (
            current_time.hour in self.config.RECOMMENDATION_HOURS
            and current_time.minute == 0
        ):
            await self.generate_recommendations(current_time)

    async def start_day(self, current_time: datetime) -> None:
        """Starts the day simulation."""
        greeting = await self.generate_personalised_greeting(current_time)
        self.logger.info(f"\n[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] {greeting}")
        self.logger.info(
            f"[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] It's {current_time.strftime('%I:%M %p')}. Here's your day at a glance:"
        )
        await self.generate_tasks(current_time)
        await self.generate_recommendations(current_time)

    async def generate_personalised_greeting(self, current_time: datetime) -> str:
        """Generates a personalised greeting for the user."""
        name = self.user.profile["name"]
        sleep_data = self.user.profile["fitness_data"]["sleep"]["last_night"]

        # Create a prompt for the language model to generate a personalised greeting
        prompt = f"""
        Generate a personalised morning greeting for {name} based on the following data:
        - Sleep data: {sleep_data}
        - Current time: {current_time.strftime('%I:%M %p')}
        """

        # Query the language model for the greeting
        greeting = await self.query_llm(prompt)
        return greeting.strip()

    async def handle_event(self, event: str, current_time: datetime) -> None:
        """Handles an event and generates a proactive action."""
        if "Upcoming event" in event:
            self.logger.info(
                f"\n[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] Heads up, {self.user.name}! {event}"
            )

            event_details = event.split(": ")[1]
            current_location = self.user.get_current_location(
                current_time
            )

            # Create a prompt for the language model
            prompt = f"""Suggest a proactive action for the event: '{event_details}'.
            User's current location: {current_location}
            Current time: {current_time.strftime('%I:%M %p')}
            User's profile: {self.user.profile}
            Suggestion should be helpful, context-aware, and consider the user's preferences and habits.
            And, give the response such that you are speaking to the user"""

            action = await self.query_llm(
                prompt
            )  # Query the language model for an action suggestion
            self.logger.info(
                f"[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] I suggest: {action}"
            )  # Log suggestion to user
            self.logger.info(
                f"[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] Would you like me to take care of anything related to this event?"
            )
            #
            # TODO: Implement a way to get user's input/prompt and act accordingly
            #

    async def end_day(self, current_time: datetime) -> None:
        """Ends the day simulation."""
        self.logger.info(f"\n[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] --- Good evening, {self.user.name}. ---")
        self.logger.info(f"[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] Here's a quick summary of your day:")

        completed_tasks = len(self.tasks)
        steps = self.user.profile["fitness_data"][
            "steps_today"
        ]
        calories = self.user.profile["fitness_data"][
            "calories_burned_today"
        ]

        summary = f"You completed {completed_tasks} tasks today, took {steps} steps, and burned {calories} calories. Great job!"

        if steps > self.user.profile["fitness_data"]["average_daily_steps"]:
            summary += " You exceeded your average daily step count!"

        self.logger.info(f"[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] {summary}")
        self.logger.info(
            f"\n[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] Here are some key recommendations for tomorrow:"
        )
        for rec in self.recommendations[-3:]:  # Show last three recommendations
            self.logger.info(f"[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] - {rec}")

        self.logger.info(
            f"\n[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] Is there anything else you'd like me to help with before you call it a day?"
        )
        await self.simulate_user_response(
            "Is there anything else you'd like me to help with before you call it a day?"
        )

    async def generate_tasks(self, current_time: datetime) -> None:
        """Generates proactive tasks for the user."""
        profile = self.user.profile  # Get user profile
        calendar = self.user.get_upcoming_events(
            hours=24
        )
        
        # Create a prompt for the language model to generate tasks
        prompt = f"""Generate 3 proactive tasks for {self.user.name} based on their profile and calendar:
        Profile: {profile}
        Calendar: {calendar}
        Current time: {current_time.strftime('%I:%M %p')}
        Tasks should be specific and actionable."""

        response = await self.query_llm(prompt)
        self.tasks = response.split("\n")
        self.logger.info(f"[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] Today's tasks:")

        for task in self.tasks:
            self.logger.info(f"[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] - {task}")

    async def generate_recommendations(self, current_time: datetime) -> None:
        """Generates personalised recommendations for the user."""
        profile = self.user.profile  # Get user profile
        social_media = self.user.social_media  # Get user's social media data
        spotify = self.user.spotify_playlists  # Get user's Spotify playlists
        current_location = self.user.get_current_location(
            current_time
        )

        # Create a prompt for the language model to generate recommendations
        prompt = f"""Generate a personalised recommendation for {self.user.name} based on their profile, social media, music preferences, current location, and time of day. Additionally, classify the recommendation as 'urgent', 'important', or 'normal':
        Profile: {profile}
        Social Media: {social_media}
        Spotify Playlists: {spotify}
        Current location: {current_location}
        Current time: {current_time.strftime('%I:%M %p')}
        Recommendation should be specific, tailored to the user's interests, current location, and the time of day. Please include a classification at the end of the response."""

        response = await self.query_llm(
            prompt
        )  # Query the language model for recommendations
        self.recommendations.append(response.strip())  # Add recommendation to the list
        self.logger.info(
            f"\n[{current_time.strftime('%I:%M %p')}] [AI's Brain] Generated recommendation: {response.strip()}"
        )

        # Check urgency and importance of the recommendation
        if "urgent" in response.lower() or "important" in response.lower():
            self.logger.info(f"[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] Important recommendation: {response.strip()}")
            # Optionally, add an event based on the recommendation
            new_event = {
                "date": current_time.strftime("%Y-%m-%d"),
                "time": current_time.strftime("%H:%M"),
                "event": response.strip(),
                "duration": "1"  # Default duration, can be adjusted but 1 for now!
            }
            await self.add_event(new_event)  # Add the event to the calendar
        else:
            self.logger.info(f"[{current_time.strftime('%I:%M %p')}] [NOTIFICATION] I have a new suggestion for you, {self.user.name}. Would you like to hear it?")
            # TODO: Implement a way to get user's input/prompt and act accordingly

    async def query_llm(self, prompt: str) -> str:
        """Queries the language model with the given prompt using OpenAI API."""
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: openai.ChatCompletion.create(
                    model=self.config.LLM_MODEL,  # Specify the model to use
                    messages=[
                        {"role": "user", "content": prompt}
                    ],  # Prepare the message for the model
                    max_tokens=self.config.LLM_MAX_TOKENS,  # Set max tokens for the response
                    n=1,  # Number of responses to generate
                    temperature=self.config.LLM_TEMPERATURE,  # Set the randomness of the response
                ),
            )
            return response.choices[0].message.content.strip()  # Return the generated response
        except OpenAIError as e:
            self.logger.error(f"OpenAI API error: {str(e)}")
            return "An error occurred while processing your request."

    async def simulate_user_response(self, prompt: str) -> str:
        """Simulates a user response to the AI assistant's prompt."""
        user_response_prompt = f"""Given the AI assistant's prompt: '{prompt}', generate a natural, conversational response."""
        response = await self.query_llm(user_response_prompt)  # Query the model for a simulated user response

        self.logger.info(f"[{datetime.now().strftime('%I:%M %p')}] [NOTIFICATION] Simulated user response: {response}")
        return response

    async def add_event(self, event: Dict[str, str]) -> None:
        """Adds a new event to the user's calendar, based on the recommendation. Ex: Run, Break, etc"""
        # Maybe TODO: Add when there is only a free slot in the calendar?
        # Currently it just adds the event and let user decide what's best for them
        self.user.calendar.append(event)
        self.logger.info(f"[Event added] {event}")
