from datetime import time
import openai

class Config:
    """Configuration class for EVERYTHING."""

    # Simulation settings
    SIMULATION_START_TIME = time(7, 0)  # 7:00 AM
    SIMULATION_END_TIME = time(22, 0)  # 10:00 PM
    SIMULATION_INTERVAL = 30  # minutes

    # Recommendation times
    # TODO: Implment time choosing logic instead of hardcoding (based on user's live activity)
    RECOMMENDATION_HOURS = [9, 12, 15, 18]

    # LLM settings
    LLM_MODEL = "gpt-3.5-turbo"
    LLM_MAX_TOKENS = 150
    LLM_TEMPERATURE = 0.7