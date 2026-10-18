import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "AI Export Manager"
    VERSION: str = "1.0.0"
    TEAM_NAME: str = "CoreTech Innovation"
    TEAM_LEAD: str = "Sufyan Arain"
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "coretech-export-manager-secret-2026")
    DEFAULT_CURRENCY: str = "USD"
    MOCK_MODE: bool = True

settings = Settings()
