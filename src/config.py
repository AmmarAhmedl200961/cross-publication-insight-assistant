"""
Configuration settings for the Publication Assistant system
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Agent Configuration
AGENT_SETTINGS = {
    "verbose": True,
    "memory": True,
    "step_callback": None,
    "system_template": None,
    "prompt_template": None,
}

# Tool Configuration
TOOL_SETTINGS = {
    "timeout": 30,
    "max_retries": 3,
    "retry_delay": 1,
}

# Crew Configuration
CREW_SETTINGS = {
    "verbose": True,
    "memory": True,
    "cache": True,
    "max_rpm": 25,
    "max_iter": 15,
    "share_crew": False,
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": ["console", "file"],
    "file_path": "logs/publication_assistant.log",
}

# Validation
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")
