import asyncio
import logging
import sys
import os

# Add the parent directory to the Python path for module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import necessary classes from modules
from everything.config import Config
from device_data.device_data import DeviceData
from user_data.user_data import UserData
from everything.everything import EVERYTHING

async def main():
    """Main function to run the simulation."""
    try:
        # Initialise user and device data
        user = UserData(name="Dan")  # Create a UserData instance for Dan
        devices = DeviceData(user)    # Create DeviceData instance linked to the user
        config = Config()             # Load configuration settings

        # Create an instance of EVERYTHING with user, devices, and config
        ai = EVERYTHING(user, devices, config)

        # Simulate a day in Dan's life with EVERYTHING AI
        await ai.simulate_day()       # Await the simulation process
    except Exception as e:
        # Log any errors that occur during the simulation
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Set up logging configuration
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    # Run the main function using asyncio
    asyncio.run(main())
