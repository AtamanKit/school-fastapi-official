from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the application.
    """

    db_url: str
    db_url_test: str
    testing: bool


settings = Settings()
