from os import getenv

REDIS_URI = (
    f"redis://{getenv("REDIS_HOST", "localhost")}:{getenv("REDIS_PORT", "6379")}"
)
