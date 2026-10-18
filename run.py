import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"Starting {settings.APP_NAME} v{settings.VERSION} ({settings.TEAM_NAME})...")
    print(f"Open http://{settings.HOST}:{settings.PORT} in your web browser.")
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
