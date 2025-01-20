import csv
from books.book import Book
from Library_Controls.StatisticsManager import StatisticsManager
import logging
from users.librarian import LibrarianManager

logging.basicConfig(filename='files/library_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')


class LibraryController:
    def __init__(self, library, statistics_manager, librarian_manager, file_path="books.csv"):
        self.library = library  # Reference to the Library object
        self.stat_manager = statistics_manager  # Reference to StatisticsManager
        self.librarian_manager = LibrarianManager()  # Properly assign instance
        self.file_path = file_path

    def add_book(self, title, author, copies, category, year):
        """Add a new book to the library."""
        try:
            book_identifier = self._generate_book_key(title, author)
            if self.library.has_book(book_identifier):
                raise ValueError(f"Book '{title}' by {author} already exists.")
            book = Book(title, author, category, year, copies)
            self.library.add_book(book_identifier, book)
            self._sync_books()
            logging.info(f"Book '{title}' added successfully.")
        except Exception as e:
            logging.error(f"Failed to add book '{title}': {e}")

    def remove_book(self, title, author):
        """Remove a book from the library."""
        book_identifier = self._generate_book_key(title, author)
        if not self.library.has_book(book_identifier):
            raise ValueError(f"Book '{title}' by {author} not found in the library.")
        self.library.remove_book(book_identifier)
        self._sync_books()

    def update_book(self, title, author, updates):
        """Update details of an existing book."""
        book_identifier = self._generate_book_key(title, author)
        if not self.library.has_book(book_identifier):
            raise ValueError(f"Book '{title}' by {author} not found in the library.")
        book = self.library.get_book(book_identifier)
        for key, value in updates.items():
            setattr(book, key, value)
        self._sync_books()

    def _generate_book_key(self, title, author):
        """Generate a unique key for the book."""
        return StatisticsManager.generate_key(title, author)

    def borrow_book(self, title, author, user):
        """Borrow a book or add the user to the waitlist if no copies are available."""
        book_key = self._generate_book_key(title, author)
        if not self.library.has_book(book_key):
            raise ValueError(f"Book '{title}' by '{author}' not found in the library.")

        book = self.library.books[book_key]

        # Check if there are available copies to borrow
        if book.available_copies > 0:
            # Borrow the book
            book.available_copies -= 1
            if book.available_copies == 0:
                book.is_loaned = True

            # Update StatisticsManager
            self.stat_manager.increment_request_count(book_key)
            logging.info(f"'{user}' borrowed the book '{title}' by '{author}'.")
        else:
            # Add the user to the waitlist
            self.stat_manager.add_user_to_waitlist(book_key, user)
            logging.info(f"'{title}' by '{author}' is unavailable. '{user}' has been added to the waitlist.")
            raise ValueError(f"No available copies of '{title}' by '{author}'. You have been added to the waitlist.")

    def return_book(self, title, author):
        """Return a borrowed book and notify the next user in the waitlist if applicable."""
        book_key = self._generate_book_key(title, author)
        if not self.library.has_book(book_key):
            raise ValueError(f"Book '{title}' by '{author}' not found in the library.")

        book = self.library.books[book_key]

        # Check if the book is actually loaned out
        if book.available_copies >= book.copies:  # All copies are already returned
            raise ValueError(f"All copies of '{title}' by '{author}' have already been returned.")

        # Increment the available copies
        book.available_copies += 1
        if book.available_copies > 0:
            book.is_loaned = False

        # Notify the next user on the waitlist, if any
        next_user = self.stat_manager.notify_waitlist(book_key)
        if next_user:
            logging.info(f"'{title}' by '{author}' is now available. Notifying '{next_user}'.")
        else:
            logging.info(f"'{title}' by '{author}' was returned. No users are on the waitlist.")

    def _sync_books(self):
        """Write library data to CSV."""
        books = self.library.get_all_books()
        with open(self.file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "author", "category", "year", "copies", "available_copies", "is_loaned"])
            writer.writeheader()
            for book in books.values():
                writer.writerow(book.to_dict())

    def load_books(self):
        """Load books from CSV into the library."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book = Book.from_dict(row)
                    book_identifier = self._generate_book_key(book.title, book.author)
                    self.library.add_book(book_identifier, book)
        except FileNotFoundError:
            pass  # No books to load if the file doesn't exist

    def authenticate_librarian(self, username, librarian_id, password):
        """Authenticate a librarian."""
        try:
            if not self.librarian_manager.authenticate(username, librarian_id, password):
                raise PermissionError("Invalid username, ID, or password.")
            logging.info(f"Librarian '{username}' with ID '{librarian_id}' authenticated successfully.")
        except Exception as e:
            logging.error(f"Failed to authenticate librarian '{username}' with ID '{librarian_id}': {e}")
            raise

    def register_librarian(self, username, id, password):
        """Register a new librarian."""
        if self.librarian_manager.is_librarian_registered(id):
            raise ValueError("Librarian with this id already exists.")
        self.librarian_manager.add_librarian(username, id, password)
        logging.info(f"Librarian '{username}' registered successfully.")
