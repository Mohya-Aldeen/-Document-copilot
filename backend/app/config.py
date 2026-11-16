"""
Single source of truth for backend configuration.

Per AGENTS.md: no os.getenv or load_dotenv anywhere else in the app.
Import settings wherever config is needed.
"""

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # --- Supabase (Auth + API) ---
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str

    # --- Postgres (SQLAlchemy models + Alembic migrations) ---
    DATABASE_URL: str

    # --- OpenAI (LLM + embeddings) ---
    OPENAI_API_KEY: str
    OPENAI_CHAT_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_EMBEDDING_DIMENSIONS: int = 1536
    ASSISTANT_MAX_TOOL_ROUNDS: int = 24
    INGEST_CHUNK_MAX_TOKENS: int = 512

    # --- Server ---
    # Hosting platforms inject PORT. Local execution uses 8000 if unset.
    PORT: int = 8000
    # Comma-separated browser origins. Include the deployed frontend origin.
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @computed_field
    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


settings = Settings()
