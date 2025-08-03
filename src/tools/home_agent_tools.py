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
    title: str, rating: Optional[int] = None, notes: Optional[str] = None
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
def get_book_lists() -> str:
    """
    Get the complete book reading list and reading history.
    The agent will analyze this data to make personalized recommendations.

    Returns:
        str: JSON string containing full book data
    """
    book_paths = "/home/petar/Documents/project-charon/data/book_list.json"
    try:
        with open(book_paths) as f:
            books = json.load(f)

        total_to_read = len(books.get("to_read", []))
        total_read = len(books.get("read", []))

        result = f"BOOK DATA (To Read: {total_to_read}, Read: {total_read})\n"
        result += "=" * 50 + "\n\n"
        result += json.dumps(books, indent=2)

        return result
    except Exception as e:
        return f"Error reading book data: {str(e)}"


@tool
def add_book_to_reading_list(
    title: str,
    author: str,
    genre: Optional[str] = None,
    pages: Optional[int] = None,
    notes: Optional[str] = None,
) -> str:
    """
    Add a book to the reading list.

    Args:
        title: Book title
        author: Book author
        genre: Book genre/category
        pages: Number of pages
        notes: Any additional notes or why the user wants to read it

    Returns:
        str: Confirmation message
    """
    book_paths = "/home/petar/Documents/project-charon/data/book_list.json"

    try:
        with open(book_paths) as f:
            books = json.load(f)

        # Check if book already exists
        existing = next(
            (
                b
                for b in books["to_read"]
                if b["title"].lower() == title.lower()
                and b["author"].lower() == author.lower()
            ),
            None,
        )
        if existing:
            return f"'{title}' by {author} is already in your reading list!"

        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages,
            "notes": notes,
            "added_date": datetime.now().isoformat()[:10],
        }

        books["to_read"].append(new_book)

        with open(book_paths, "w") as f:
            json.dump(books, f, indent=2)

        logger.success(f"Added '{title}' by {author} to your reading list!")

        return f"Added '{title}' by {author} to your reading list!"
    except Exception as e:
        logger.error(f"Error adding book: {str(e)}")

        return f"Error adding book: {str(e)}"


@tool
def mark_book_read(
    title: str, author: str, rating: Optional[int] = None, notes: Optional[str] = None
) -> str:
    """
    Mark a book as read and move it to the read list.

    Args:
        title: Book title (must match existing title)
        author: Book author (must match existing author)
        rating: Your rating out of 10
        notes: Your thoughts about the book

    Returns:
        str: Confirmation message
    """
    book_paths = "/home/petar/Documents/project-charon/data/book_list.json"

    try:
        with open(book_paths) as f:
            books = json.load(f)

        # Find book in to_read list
        book_index = None
        for i, book in enumerate(books["to_read"]):
            if (
                book["title"].lower() == title.lower()
                and book["author"].lower() == author.lower()
            ):
                book_index = i
                break

        if book_index is None:
            return f"'{title}' by {author} not found in your reading list. Make sure both title and author match exactly."

        # Move book to read list
        read_book = books["to_read"].pop(book_index)
        read_book["read_date"] = datetime.now().isoformat()[:10]

        if rating is not None:
            read_book["rating"] = rating
        if notes:
            read_book["notes"] = notes

        books["read"].append(read_book)

        with open(book_paths, "w") as f:
            json.dump(books, f, indent=2)

        logger.success(
            f"Marked '{title}' by {author} as read! {f'Rated {rating}/10. ' if rating else ''}Nice work!"
        )
        return f"Marked '{title}' by {author} as read! {f'Rated {rating}/10. ' if rating else ''}Nice work!"

    except Exception as e:
        logger.error(f"Error marking book as read: {str(e)}")
        return f"Error marking book as read: {str(e)}"


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


@tool
def search_book(title: str, author: str = "") -> str:
    """
    Search for book information using the Open Library API.

    Args:
        title: Book title to search by
        author: Book author to search by (optional)

    Returns:
        str: A string of JSONs that the API matched to the search
    """
    api_url = "https://openlibrary.org/search.json"
    params = {"title": title}
    logger.info(f"Searching Open Library for book: {title} (Author: {author})")
    if author:
        params["author"] = author

    try:
        response = requests.get(api_url, params=params)
        data = response.json()

        if data.get("numFound", 0) > 0:
            logger.success(f"Open Library returned the following books {data}")

            return f"Found matches: {json.dumps(data)}"
        else:
            logger.error("Book not found")
            return (
                f"Book '{title}' not found. Error: {data.get('Error', 'Unknown error')}"
            )

    except Exception as e:
        logger.error(f"Error searching for book: {str(e)}")
        return f"Error searching for book: {str(e)}"
