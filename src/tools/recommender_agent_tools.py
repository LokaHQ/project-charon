from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from src.utils.substack_api_utils import (
    get_recent_posts,
    get_post_metadata_from_newsletter,
)
from strands import tool
import json
from loguru import logger


@tool
def add_substack_newsletter_to_monitor(newsletter_url: str) -> str:
    """
    Add a Substack newsletter to the monitoring list.

    Args:
        newsletter_url (str): The URL of the Substack newsletter.

    Returns:
        str: Confirmation message.
    """
    path_url = "/home/petar/Documents/project-charon/data/substack_newsletters.json"

    try:
        with open(path_url) as file:
            newsletters = json.load(file)
    except FileNotFoundError:
        logger.error(f"File {path_url} not found")
        newsletters = []

    if newsletter_url in newsletters:
        logger.warning(
            f"Newsletter {newsletter_url} is already in the monitoring list."
        )
        return f"Newsletter {newsletter_url} is already in the monitoring list."

    newsletters.append(newsletter_url)

    with open(path_url, "w") as file:
        json.dump(newsletters, file)
    logger.success(
        f"Newsletter {newsletter_url} has been added to the monitoring list."
    )

    return f"Newsletter {newsletter_url} has been added to your monitoring list."


@tool
def get_all_newsletters() -> list:
    """
    Retrieve all Substack newsletters from the monitoring list.

    Returns:
        list: List of Substack newsletter URLs.
    """
    path_url = "/home/petar/Documents/project-charon/data/substack_newsletters.json"

    try:
        with open(path_url) as file:
            newsletters = json.load(file)
        logger.info(
            f"Retrieved {len(newsletters)} newsletters from the monitoring list."
        )
        return newsletters
    except FileNotFoundError:
        logger.error(f"File {path_url} not found")
        return []


@tool
def get_recent_posts_from_newsletter(newsletter_url: str, limit: int = 5) -> list:
    """
    Get recent posts from a Substack newsletter.

    Args:
        newsletter_url (str): The URL of the Substack newsletter.
        limit (int): The number of recent posts to fetch.

    Returns:
        list: List of recent posts with metadata.
    """
    try:
        posts = get_recent_posts(newsletter_url, limit)
        logger.info(f"Retrieved {len(posts)} recent posts from {newsletter_url}.")
        metadata = [
            get_post_metadata_from_newsletter(newsletter_url, limit) for post in posts
        ]
        logger.info(f"Extracted metadata for {len(metadata)} posts.")
        return metadata

    except Exception as e:
        logger.error(f"Error fetching posts from {newsletter_url}: {e}")
        return [f"Error fetching posts from {newsletter_url}: {e}"]
