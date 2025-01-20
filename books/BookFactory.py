import logging
from books.book import Book

logging.basicConfig(filename="../files/library_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")


class BookFactory:
    @staticmethod
    def create_book(title, author, is_loaned=False, copies=0, genre="", year=0, available=None):
        """
        Factory method to create a new book instance.
        Validates inputs and ensures consistent object creation.
        """
        try:
            # Validation for mandatory fields
            if not title or not author:
                raise ValueError("Title and Author cannot be empty")
            if copies < 0:
                raise ValueError("Copies cannot be negative")
            if year < 0:
                raise ValueError("Year cannot be negative")

            # Default for available copies
            if available is None:
                available = copies

            # Create and return the Book instance
            book = Book(
                title=title.strip(),
                author=author.strip(),
                is_loaned=is_loaned,
                copies=copies,
                genre=genre.strip(),
                year=year,
                available=available
            )
            logging.info(f"Book '{title}' by {author} created successfully.")
            return book

        except Exception as e:
            logging.error(f"Failed to create book '{title}' by {author}: {e}")
            raise