import sys
from pathlib import Path

from strands import tool

sys.path.append(str(Path(__file__).parent.parent))
import json
import os
from datetime import datetime
from typing import Optional

import requests
from dotenv import load_dotenv
from loguru import logger


load_dotenv()


@tool
def get_movies_and_show_list() -> str:
    """
    Get the complete movie/show watchlist and watch history.
    The agent will analyze this data to make personalized recommendations.

    Returns:
        str: JSON string containing full movie/show data
    """
    # config=load_config()

    list_path = "/home/petar/Documents/project-charon/data/movie_and_show.json"

    try:
        with open(list_path) as f:
            movies = json.load(f)

        total_to_watch = len(movies.get("to_watch", []))
        total_watched = len(movies.get("watched", []))

        result = f"MOVIE DATA (To Watch: {total_to_watch}, Watched: {total_watched})\n"
        result += "=" * 50 + "\n\n"
        result += json.dumps(movies, indent=2)

        return result
    except Exception as e:
        return f"Error reading movie data: {str(e)}"


@tool
def add_movie_or_show_to_watchlist(
    title: str,
    year: Optional[int] = None,
    genre: Optional[str] = None,
    director: Optional[str] = None,
    notes: Optional[str] = None,
) -> str:
    """
    Add a movie to the watchlist.

    Args:
        title: Movie/show title
        year: Release year
        genre: Movie/show genre
        director: Director/showrunner name
        notes: Any additional notes or context

    Returns:
        str: Confirmation message
    """
    list_path = "/home/petar/Documents/project-charon/data/movie_and_show.json"
    try:
        with open(list_path) as f:
            movies = json.load(f)

        # Check if movie already exists
        existing = next(
            (m for m in movies["to_watch"] if m["title"].lower() == title.lower()), None
        )
        if existing:
            return f"'{title}' is already in your watchlist!"

        new_movie = {
            "title": title,
            "year": year,
            "genre": genre,
            "director": director,
            "notes": notes,
            "added_date": datetime.now().isoformat()[:10],
        }

        movies["to_watch"].append(new_movie)

        with open(list_path, "w") as f:
            json.dump(movies, f, indent=2)

        return f"Added '{title}' to your watchlist!"
    except Exception as e:
        return f"Error adding movie: {str(e)}"


@tool
def mark_movie_or_show_watched(
    title: str, rating: Optional[float] = None, notes: Optional[str] = None
) -> str:
    """
    Mark a movie as watched and move it to the watched list.

    Args:
        title: Movie/show title (must match existing title in watchlist)
        rating: Your rating out of 10
        notes: Your thoughts about the movie

    Returns:
        str: Confirmation message
    """
    list_path = "/home/petar/Documents/project-charon/data/movie_and_show.json"

    try:
        with open(list_path) as f:
            movies = json.load(f)

        # Find movie in to_watch list
        movie_index = None
        for i, movie in enumerate(movies["to_watch"]):
            if movie["title"].lower() == title.lower():
                movie_index = i
                break

        if movie_index is None:
            return f"'{title}' not found in your watchlist. Make sure the title matches exactly."

        # Move movie to watched list
        watched_movie = movies["to_watch"].pop(movie_index)
        watched_movie["watched_date"] = datetime.now().isoformat()[:10]

        if rating is not None:
            watched_movie["rating"] = rating
        if notes:
            watched_movie["notes"] = notes

        movies["watched"].append(watched_movie)

        with open(list_path, "w") as f:
            json.dump(movies, f, indent=2)

        return f"Marked '{title}' as watched! {f'Rated {rating}/10. ' if rating else ''}Great job!"
    except Exception as e:
        return f"Error marking movie as watched: {str(e)}"


@tool
def search_omdb_movie_or_show(title: str, year: str = "", type="") -> str:
    """
    Search for movie/show information and metadata using the free OMDB API.
    Args:
        title: movie title to search by
        year: year to filter by, if available.
        type: movie, tv show, or eppisode

    Returns:
        str: A string of jsons that the api matched to th search
    """
    api_key = os.getenv("OMDB_API_KEY")
    url = "http://www.omdbapi.com/"
    params = {"apikey": api_key, "s": title, "plot": "short"}

    logger.info(f"Searching OMDB for movie/show: {title} (Year: {year}, Type: {type})")

    if year != "":
        params["y"] = year

    if type != "":
        params["type"] = type

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("Response") == "True":
            logger.success(f"OMDB returned the following movies {data}")

            return f"Found matches: {json.dumps(data)}"

        else:
            logger.error("Movie not found")
            return f"Movie '{title}' not found. Error: {data.get('Error', 'Unknown error')}"

    except Exception as e:
        logger.error(f"Error searching for movie: {str(e)}")
        return f"Error searching for movie: {str(e)}"
