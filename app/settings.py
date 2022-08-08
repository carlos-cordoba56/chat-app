"""
module with application configuration
"""
from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Main setting for application
    """
    app_name: str
    database_username: str
    database_password: str
    database_hostname: str
    database_port: str
    database_name: str
    
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

settings = Settings()
