import logging
from management.book import Book
from management.LibraryFileManager import LibraryFileManager
from management.StatisticsManager import StatisticsManager


class Library:
    def __init__(self, file_path=None, statistics_manager=None):
        self.file_path = file_path
        self.stat_manager = statistics_manager or StatisticsManager()
        self.file_manager = LibraryFileManager(file_path) if file_path else None
        self.books = {}
        if file_path:
            self.load_books()

    def add_book(self, title, author, copies, genre, year, is_loaned=False, available=None):
        """Add or update a book in the library."""
        if not title or not author:
            raise ValueError("Title and author are required")

        book_key = StatisticsManager.generate_key(title, author)
        if book_key in self.books:
            self.books[book_key].copies += copies
            self.books[book_key].available += (available if available is not None else copies)
        else:
            self.books[book_key] = Book(
                title=title,
                author=author,
                copies=copies,
                genre=genre,
                year=year,
                is_loaned=is_loaned,
                available=available,
                stat_manager=self.stat_manager
            )

        if self.file_manager:
            self.save_books_to_csv()
        return self.books[book_key]

    def remove_book(self, title, author):
        """Remove a book from the library."""
        book_key = StatisticsManager.generate_key(title, author)
        if book_key not in self.books:
            raise ValueError(f"Book '{title}' by {author}' not found")

        del self.books[book_key]
        if self.file_manager:
            self.save_books_to_csv()
        return True

    def borrow_book(self, title, author):
        """Borrow a book if available."""
        book_key = StatisticsManager.generate_key(title, author)

        if book_key not in self.books:
            raise ValueError(f"Book '{title}' by {author} not found")

        book = self.books[book_key]
        if book.borrow():
            if self.file_manager:
                self.save_books_to_csv()
            return True

        # Update request count even if borrow fails
        self.stat_manager.update_request_count(book_key)
        raise ValueError(f"No available copies of '{title}' by {author}")

    def return_book(self, title, author):
        """Return a borrowed book."""
        book_key = StatisticsManager.generate_key(title, author)
        if book_key not in self.books:
            raise ValueError(f"Book '{title}' by {author} not found")

        book = self.books[book_key]
        if book.return_book():
            if self.file_manager:
                self.save_books_to_csv()
            return True

        raise ValueError(f"Cannot return more copies than exist for '{title}' by {author}")

    def load_books(self):
        """Load books from file if file_manager exists."""
        if not self.file_manager:
            return

        try:
            books, request_counts = self.file_manager.load_books()
            self.books = books
            self.stat_manager.load_statistics(request_counts)
        except Exception as e:
            raise RuntimeError(f"Error loading books: {e}")

    def save_books_to_csv(self):
        """Save books to file if file_manager exists."""
        if not self.file_manager:
            return

        try:
            self.file_manager.save_books(self.books, self.stat_manager.export_statistics())
        except Exception as e:
            raise RuntimeError(f"Error saving books: {e}")

    def add_user_to_waitlist(self, title, author, username):
        """Add a user to the waitlist for a specific book."""
        book_key = StatisticsManager.generate_key(title, author)
        if book_key not in self.books:
            raise ValueError(f"Book '{title}' by {author} not found")
        if username in self.stat_manager.get_waitlist(book_key):
            raise ValueError(f"User '{username}' is already on the waitlist for '{title}' by {author}")
        self.stat_manager.add_user_to_waitlist(book_key, username)
        if self.file_manager:
            self.save_books_to_csv()
        return True

    def remove_user_from_waitlist(self, title, author, username):
        """Remove a user from the waitlist for a specific book."""
        book_key = StatisticsManager.generate_key(title, author)
        if book_key not in self.books:
            raise ValueError(f"Book '{title}' by {author} not found")
        self.stat_manager.remove_user_from_waitlist(book_key, username)
        if self.file_manager:
            self.save_books_to_csv()
        return True

    def get_waitlist(self, book_key):
        """Get the waiting list for a specific book."""
        return self.stat_manager.get_waitlist(book_key)