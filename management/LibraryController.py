import csv

from management.LibraryFileManager import LibraryFileManager
from books.book import *
from management.StatisticsManager import StatisticsManager

from users.librarian import LibrarianManager
import os
from files.Log import add_log

class LibraryController:
    DEFAULT_FILE_PATH = os.path.abspath("../files/books.csv")
    def __init__(self, library, statistics_manager, file_path=DEFAULT_FILE_PATH):
        self.library = library
        self.stat_manager = statistics_manager
        self.librarian_manager = LibrarianManager()
        self.file_path = file_path
        if not isinstance(file_path, (str, os.PathLike)):
            raise TypeError("file_path must be a string or PathLike object.")

    def add_book(self, title, author, copies, genre, year):
        """Add a new book to the library."""
        try:
            # Generate book key
            book_key = self._generate_book_key(title, author)
            if self.library.has_book(book_key):
                raise ValueError(f"The book '{title}' by {author} already exists in the library.")

            # Create a new book object with request_counter set to 0
            new_book = Book(
                title=title,
                author=author,
                genre=genre,
                year=year,
                copies=copies,
                available=copies,
                request_counter=0  # Initialize request counter to 0 for new books
            )

            # Add book to the internal library
            self.library.add_book(new_book, book_key)

            # Synchronize the library data with books.csv
            self._sync_books()
            add_log(f"Book '{title}' by '{author}' successfully added to the library.","info")

        except Exception as e:
            add_log(f"Error while adding book '{title}' by '{author}': {str(e)}","info")
            raise

    def remove_book(self, title, author):
        """Remove a book from the library."""
        book_identifier = self._generate_book_key(title, author)
        book = self.library.books[book_identifier]
        if not self.library.has_book(book_identifier):
            raise ValueError(f"Book '{title}' by {author} not found in the library.")
        if book.available != book.copies:
            raise ValueError(f"The book '{title}' by {author} cannot be removed from the library because the book is lend.")
        else:
            self.library.remove_book(book_identifier)
            self._sync_books()

    @staticmethod
    def _generate_book_key(title, author):
        """Generate a unique key for the book."""
        return StatisticsManager.generate_key(title, author)

    def borrow_book(self, title, author, user):
        """Borrow a book or add the user to the waitlist if unavailable."""
        book_key = self._generate_book_key(title, author)

        if not self.library.has_book(book_key):
            raise ValueError(f"The book '{title}' by '{author}' does not exist in the library.")

        book = self.library.books[book_key]

        # Increment the request counter
        book.request_counter += 1

        if book.available > 0:
            # Decrease the available copies and mark the book as loaned
            book.available -= 1
            book.is_loaned = book.available == 0
            add_log(f"Book '{title}' successfully borrowed by {user['name']}.",'info')
            self._sync_books()
            return True  # Book successfully borrowed

        # If no copies are available, add the user to the waitlist
        self.stat_manager.add_user_to_waitlist(book_key, user)
        add_log(f"Book '{title}' is unavailable. {user['name']} added to the waitlist.","info")
        self._sync_books()
        return False  # User added to waitlist

    def return_book(self, title, author):
        """Return a borrowed book and notify the next user in the waitlist if applicable."""
        book_key = self._generate_book_key(title, author)
        if not self.library.has_book(book_key):
            raise ValueError(f"Book '{title}' by '{author}' not found in the library.")

        book = self.library.books[book_key]

        # Check if the book is actually loaned out
        if book.available >= book.copies:  # All copies are already returned
            raise ValueError(f"All copies of '{title}' by '{author}' have already been returned.")

        # Increment the available copies
        book.available += 1
        if book.available > 0:
            book.is_loaned = False

        if self.stat_manager.get_waitlist_count()>0:
            self.stat_manager.notify_waitlist(book_key,title)

    def get_popular_books(self):
        """Get the top 10 most popular books."""
        books = sorted(self.library.get_books(), key=lambda book: book.request_counter, reverse=True)
        return books[:10]

    def get_available_books(self):
        """Get all available books."""
        available_books = [book for book in self.library.get_books() if not book.is_loaned]
        return available_books

    def _sync_books(self):
        """Save library data to CSV using LibraryFileManager."""
        file_manager = LibraryFileManager(file_path=self.file_path)
        file_manager.save_books(self.library, self.stat_manager)

    def load_books(self):
        """Load books from CSV into the library."""
        file_manager = LibraryFileManager(file_path=self.file_path)
        file_manager.load_books(self.library, self.stat_manager)

    def authenticate_librarian(self, username, librarian_id, password):
        """Authenticate a librarian."""
        try:
            if not self.librarian_manager.authenticate(username, librarian_id, password):
                raise PermissionError("Invalid username, ID, or password.")
            add_log(f"Librarian '{username}' with ID '{librarian_id}' authenticated successfully.","info")
        except Exception as e:
            add_log(f"Failed to authenticate librarian '{username}' with ID '{librarian_id}': {e}", "info")
            raise

    def register_librarian(self, username, librarian_id, password):
        """Register a new librarian."""
        if self.librarian_manager.is_librarian_registered(librarian_id):
            raise ValueError("Librarian with this id already exists.")
        self.librarian_manager.add_librarian(username, librarian_id, password)
        add_log(f"Librarian '{username}' registered successfully.","info")
