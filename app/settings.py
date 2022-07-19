"""
module with application configuration
"""
from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Main setting for application
    """
    app_name: str

settings = Settings()
