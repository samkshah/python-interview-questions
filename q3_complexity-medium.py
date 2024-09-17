# Description: This script fetches posts and users from an API and processes them. It includes a retry mechanism for handling HTTP errors.
# - API endpoint: https://jsonplaceholder.typicode.com
# - Retry mechanism: The script retries the request up to 3 times with exponential backoff if an HTTP error occurs.
# - Processing: The script filters the posts to keep only those with userId == 1.
# - Logging: The script logs information about the number of posts fetched and processed.
# - Error handling: The script catches HTTP errors and logs them, and raises an exception if the maximum number of retries is reached.
# - Configuration: The API URL is configurable via environment variables with a default value.
# - Pydantic: The script uses Pydantic for configuration management.
# - Asynchronous: The script uses asyncio and httpx to make asynchronous requests to the API.
#
# ****************************************
#
# Expected Output (Fix the script to get below output):
# - The script should print the first 5 processed posts.
# - The script should log the number of posts fetched and processed.
# - The script should print all users with username starting with 'K'
# - The script should log the number of users fetched and processed.

# Also, provide an analysis of the following aspects of the script:
# - Time complexity
# - Algorithmic complexity
# - Data structures used
# - Potential bottlenecks
# - Possible improvements
# You can provide your analysis as comments in the code or as a separate text explanation.

import httpx
import asyncio
import logging
from typing import List, Dict, Callable, Any
from pydantic_settings import BaseSettings
import time
import random
import functools


# Configuration using Pydantic
class Settings(BaseSettings):
    api_url: str = "https://jsonplaceholder.typicode.om"

    class Config:
        env_file = ".env"
        extra = "ignore"
        frozen = True


settings = Settings()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def retry(retries: int = 3, backoff_in_seconds: int = 1):
    def decorator_retry(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper_retry(*args, **kwargs) -> Any:
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except httpx.HTTPStatusError as e:
                    logger.error(
                        f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
                    )
                    logger.error(f"Attempt {attempt + 1} failed: {e}")
                except httpx.RequestError as e:
                    logger.error(f"Request error occurred: {e}")
                    logger.error(f"Attempt {attempt + 1} failed: {e}")
                except Exception as e:
                    logger.error(f"An unexpected error occurred: {e}")
                    raise
                if attempt < retries - 1:
                    backoff_time = backoff_in_seconds * (2**attempt) + random.uniform(
                        0, 1
                    )
                    logger.info(f"Retrying in {backoff_time:.2f} seconds...")
                    await asyncio.sleep(backoff_time)
            raise Exception(f"Failed after {retries} attempts")

        return wrapper_retry

    return decorator_retry


class APIClient:
    def __init__(self, base_url: str, retries: int = 3, backoff_in_seconds: int = 1):
        self.base_url = base_url
        self.retries = retries
        self.backoff_in_seconds = backoff_in_seconds

    @retry(retries=3, backoff_in_seconds=1)
    async def get(self, endpoint: str) -> List[Dict]:
        url = self.base_url + endpoint
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Fetched {len(data)} items from {endpoint}")
            return data


async def fetch_posts(api_client: APIClient) -> List[Dict]:
    return await api_client.get("/posts")


async def fetch_users(api_client: APIClient) -> List[Dict]:
    return await api_client.get("/users")


def process_posts(posts: List[Dict]) -> List[Dict]:
    filtered_posts = [post for post in posts if post["userId"] == 1]
    logger.info(f"Filtered down to {len(filtered_posts)} posts with userId == 1")
    return filtered_posts


def process_users(users: List[Dict]) -> List[Dict]:
    filtered_users = [user for user in users if user["userId"] == 1]
    logger.info(f"Filtered down to {len(filtered_users)} users with userId == 1")
    return filtered_users


async def main():
    api_client = APIClient(settings.api_url)
    posts = await fetch_posts(api_client)
    processed_posts = process_posts(posts)
    for post in processed_posts[:5]:  # Print the first 5 processed posts
        print(post)

    # get data from /users endpoint
    users = await fetch_users(api_client)
    processed_users = process_users(users)
    for user in processed_users[:5]:  # Print the first 5 processed users
        print(user)


if __name__ == "__main__":
    asyncio.run(main())
