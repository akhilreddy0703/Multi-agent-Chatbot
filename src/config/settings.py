# src/config/settings.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str

    # Authentication
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # OpenAI
    openai_api_key: str

    # Pinecone
    pinecone_api_key: str
    pinecone_environment: str
    pinecone_index_name: str

    # LLM
    llm_model: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"

settings = Settings()