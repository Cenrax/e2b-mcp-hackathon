"""Configuration management"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # E2B Configuration
    e2b_api_key: str
    
    # OpenAI Configuration
    openai_api_key: str
    
    # Logging
    log_level: str = "INFO"
    
    # Slack (optional)
    slack_channel: str = "#security-alerts"


# Global settings instance
settings = Settings()
