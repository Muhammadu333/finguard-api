import os


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing env var: {name}")
    return value


class Settings:
    database_url: str = required_env("DATABASE_URL")
    jwt_secret: str = required_env("JWT_SECRET")
    jwt_issuer: str = os.getenv("JWT_ISSUER", "finguard-api-demo")
    jwt_audience: str = os.getenv("JWT_AUDIENCE", "finguard-api")
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "30"))


settings = Settings()

