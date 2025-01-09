import csv
import os
from management.BookFactory import BookFactory
from management.book import Book as Book
import logging
from collections import defaultdict


class Library:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, 'initialized', False):
            return

        # Configure logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

        # File path setup
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_dir, "data/books.csv")
        self.books = {}  # Dictionary to hold Book objects, indexed by (title, author)
        self.loan_counter = defaultdict(int)  # Tracks borrow requests for each book

        self.initialized = True
        self.load_books_from_csv()

    # ==================== BOOK MANAGEMENT ====================
    def add_book(self, title, author, copies, genre, year):
        """
        Adds a book to the library. If it already exists, increases the number of copies.
        """
        key = Book.generate_key(title, author)
        if not title or not author:
            raise ValueError("Title and Author cannot be empty.")
        if copies <= 0:
            raise ValueError("Copies must be greater than zero.")
        if year <= 0:
            raise ValueError("Year must be a positive integer.")

        if key in self.books:
            self.books[key].copies += copies
            self.books[key].available += copies
            logging.info(f"Copies of '{title}' by {author} updated to {self.books[key].copies}.")
        else:
            new_book = BookFactory.create_book(
                title=title,
                author=author,
                is_loaned=False,
                copies=copies,
                genre=genre,
                year=year,
                available=copies
            )
            self.books[key] = new_book
            logging.info(f"Book '{title}' by {author} added to the library.")

        self.save_books_to_csv()

    def remove_book(self, title, author):
        """
        Removes a book from the library if it's not currently on loan.
        """
        key = Book.generate_key(title, author)
        if key in self.books:
            if self.books[key].available < self.books[key].copies:
                raise ValueError("Cannot remove a book with outstanding loans.")
            del self.books[key]
            logging.info(f"Book '{title}' by {author} removed from the library.")
            self.save_books_to_csv()
        else:
            raise ValueError(f"The book '{title}' by {author} does not exist.")

    def search_books(self, title=None, author=None):
        """
        Searches books based on the title and/or author.
        """
        results = [
            book for book in self.books.values()
            if (not title or title.lower() in book.title.lower()) and
               (not author or author.lower() in book.author.lower())
        ]
        return results

    def borrow_book(self, title, author):
        """
        Borrows a book if available. It decreases the 'available' count
        and increments the loan counter.
        """
        key = Book.generate_key(title, author)
        if key not in self.books:
            raise ValueError(f"The book '{title}' by {author} does not exist.")

        book = self.books[key]
        if book.available <= 0:
            raise ValueError(f"No copies of '{title}' by {author} are available for borrowing.")

        book.borrow()
        self.loan_counter[key] += 1
        logging.info(f"Book '{title}' by {author} borrowed successfully.")
        self.save_books_to_csv()

    def return_book(self, title, author):
        """
        Returns a borrowed book, increasing the 'available' count.
        """
        key = Book.generate_key(title, author)
        if key not in self.books:
            raise ValueError(f"The book '{title}' by {author} does not exist.")

        book = self.books[key]
        if not book.return_book():
            raise ValueError(f"All copies of '{title}' by {author} are already returned.")

        logging.info(f"Book '{title}' by {author} returned successfully.")
        self.save_books_to_csv()

    def get_loan_count(self, title, author):
        """
        Fetches the loan request count for a specific book.
        """
        key = Book.generate_key(title, author)
        return self.loan_counter.get(key, 0)

    # ==================== FILE HANDLING ====================
    def load_books_from_csv(self):
        """
        Loads books from a CSV file into the library. Creates Book objects from rows.
        """
        if not os.path.exists(self.file_path):
            logging.warning(f"File not found: {self.file_path}. Starting with an empty library.")
            return

        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.books = {
                    Book.generate_key(row['title'].strip(), row['author'].strip()):
                        BookFactory.create_book(
                            title=row['title'].strip(),
                            author=row['author'].strip(),
                            is_loaned=row['is_loaned'].strip().lower() in ('true', 'yes'),
                            copies=int(row['copies']),
                            genre=row['genre'].strip(),
                            year=int(row['year']),
                            available=int(row['available']),
                        )
                    for row in reader
                }
            logging.info(f"Books loaded successfully from '{self.file_path}'.")
        except Exception as e:
            logging.error(f"Failed to load books: {e}")

    def save_books_to_csv(self):
        """
        Saves the current state of the library to a CSV file.
        """
        try:
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["title", "author", "is_loaned", "copies", "genre", "year", "available"])
                for book in self.books.values():
                    writer.writerow([
                        book.title,
                        book.author,
                        "yes" if book.is_loaned else "no",
                        book.copies,
                        book.genre,
                        book.year,
                        book.available
                    ])
            logging.info("Books saved to CSV file successfully.")
        except Exception as e:
            logging.error(f"Failed to save books: {e}")

    # ==================== UTILITIES ====================
    def get_available_books(self):
        """
        Returns a list of books with at least one available copy.
        """
        return [book for book in self.books.values() if book.is_loaned==False]

    def get_popular_books(self):
        """
        Returns the books sorted by the number of times they were borrowed.
        """

        sorted_books = sorted(self.books.values(),
                              key=lambda book: self.loan_counter[Book.generate_key(book.title, book.author)],
                              reverse=True)
        return sorted_books
