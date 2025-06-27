import os

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "ZEUS NXTLVL API")
    api_port: int = int(os.getenv("API_PORT", 8000))
    metrics_port: int = int(os.getenv("METRICS_PORT", 9100))

settings = Settings()
