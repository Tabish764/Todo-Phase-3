import os
from typing import List
import logging


class Settings:
    """
    Application settings loaded from environment variables
    """
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "your-32-char-secret-here-make-it-secure")
    BETTER_AUTH_URL: str = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_AI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    @property
    def openai_api_key(self) -> str:
        """
        Get the OpenAI API key
        """
        return self.OPENAI_API_KEY

    @property
    def google_ai_api_key(self) -> str:
        """
        Get the Google AI API key
        """
        return self.GOOGLE_AI_API_KEY

    @property
    def jwks_url(self) -> str:
        """
        Get the JWKS URL from the frontend application
        """
        return f"{self.BETTER_AUTH_URL}/.well-known/jwks.json"


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create a single instance of settings
settings = Settings()