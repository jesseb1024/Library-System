import logging
from Library_Controls.StatisticsManager import StatisticsManager
from books.book import Book
import csv

class Library:
    FILE_PATH_NOT_PROVIDED_ERROR = "File path is not provided."

    def __init__(self, file_path=None):
        self.books_file_path = file_path
        self.books = {}  # Dictionary keyed by book_key

    def load_books_from_file(self):
        if not self.books_file_path:
            raise ValueError(self.FILE_PATH_NOT_PROVIDED_ERROR)
        try:
            with open(self.books_file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for line in reader:
                    book = self._parse_book_line(line)
                    if book:
                        self.add_book(book)
                    else:
                        print(f"Invalid book data: {line}")
        except Exception as e:
            raise RuntimeError(f"Failed to load books: {str(e)}")

    def add_book(self, book, book_key=None):
        if not isinstance(book, Book):
            raise TypeError(f"Expected a Book object, but got {type(book).__name__}")
        if book_key is None:
            book_key = StatisticsManager.generate_key(book.title, book.author)
        self.books[book_key] = book

    def has_book(self, book_key):
        return book_key in self.books

    def get_books(self):
        # Return the books as a list
        return list(self.books.values())

    @staticmethod
    def _parse_book_line(line):
        try:
            # Extract and sanitize fields
            title = line.get("title", "").strip()
            author = line.get("author", "").strip()
            is_loaned = line.get("is_loaned", "no").strip().lower() == "yes"
            copies = int(line.get("copies", 1))  # Default to 1 copy if not provided
            genre = line.get("genre", "Unknown").strip()
            year = int(line.get("year", 2000))  # Default to 2000 if not provided

            # Handle 'available' field
            if "available" in line and line["available"]:  # Use provided value if available
                available_copies = int(line["available"])
            else:  # Default logic for missing or empty 'available'
                available_copies = 0 if is_loaned else copies

            # Handle 'request_counter' field
            if "request_counter" in line and line["request_counter"]:  # Use provided value if available
                request_counter = int(line["request_counter"])
            else:  # Default logic for missing or empty 'request_counter'
                request_counter = copies if is_loaned else 0

            # Create and return a Book object
            return Book(
                title=title,
                author=author,
                is_loaned=is_loaned,
                copies=copies,
                genre=genre,
                year=year,
                available=available_copies,
                request_counter=request_counter,
            )
        except (ValueError, KeyError):
            # Return None if data is invalid
            return None