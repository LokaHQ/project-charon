from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from agents.books_agent import BookAgent


def main():
    books_agent = BookAgent()
    books_agent.query(
        "I need to add a book to my reading list. The book is 'The Way of Kings' by Brandon Sanderson. Can you add it?"
    )


if __name__ == "__main__":
    main()
