from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://localhost:27017" # Default value
    DATABASE_NAME: str = "resume_builder_db"    # Default value
    SECRET_KEY: str = "YOUR_SECRET_KEY"          # Default value, SHOULD BE OVERRIDDEN IN ENV
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # New AI Service settings
    AI_SERVICE_API_KEY: str = "YOUR_DEFAULT_AI_API_KEY" # Placeholder, SHOULD BE OVERRIDDEN IN ENV
    AI_SERVICE_ENDPOINT: str = "https://api.example.com/v1/completions" # Placeholder

    # For Pydantic V2, model_config is used
    # It allows loading from an .env file and ignoring extra fields.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

settings = Settings()
