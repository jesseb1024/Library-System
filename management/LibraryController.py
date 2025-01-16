from functools import wraps
from management.log import add_logger
from management.StatisticsManager import StatisticsManager

class LibraryController:
    def __init__(self, library):
        self.library = library
        self.stats_manager = library.stat_manager
        self.current_user = None  # Store the currently authenticated librarian

    def authenticate_librarian(self, username, id, password, librarian_manager):
        """Authenticate the librarian before accessing the system."""
        librarian = librarian_manager.authenticate(username, id, password)
        if librarian:
            print(f"Access granted to {librarian.username}")
            self.current_user = librarian
        else:
            raise PermissionError("Invalid username, id or password")

    def notify(action):
        """Decorator to notify of librarian actions."""

        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if not self.current_user:
                    raise PermissionError("You must be logged in as a librarian to perform this action")

                # Perform the action
                result = func(self, *args, **kwargs)

                # Notify other librarians
                message = f"Librarian '{self.current_user.username}' performed action '{action}' with details: {args}, {kwargs}."
                add_logger(message, level="info")

                return result

            return wrapper

        return decorator




    @notify("remove_book")
    def remove_book(self, title, author):
        """Remove a book (requires authentication)."""
        return self.library.remove_book(title, author)

    @notify("add_book")
    def add_book(self, title, author, copies, genre, year):
        """Add a new book through the controller."""
        if not isinstance(copies, int) or copies < 0:
            raise ValueError("Copies must be a non-negative integer")
        if not isinstance(year, int):
            raise ValueError("Year must be an integer")
        return self.library.add_book(title, author, copies, genre, year)

    @notify("borrow_book")
    def borrow_book(self, title, author):
        """Borrow a book through the controller."""
        return self.library.borrow_book(title, author)

    @notify("return_book")
    def return_book(self, title, author):
        """Return a book through the controller."""
        return self.library.return_book(title, author)


    def get_books(self):
        """Get all books with statistics manager properly set."""
        books = self.library.books.values()
        for book in books:
            if not hasattr(book, 'stat_manager') or book.stat_manager is None:
                book.stat_manager = self.stats_manager
        return books

    def get_available_books(self):
        """Get all books with available copies."""
        return [book for book in self.library.books.values() if book.available > 0]

    def get_popular_books(self):
        """Get top 10 most requested books."""
        return sorted(
            self.library.books.values(),
            key=lambda book: self.stats_manager.get_request_count(book.key),
            reverse=True
        )[:10]

    @notify("added_to_waitlist")
    def add_user_to_waitlist(self, title, author, name, phone, email):
        """Add a user to the waitlist for a specific book."""
        self.library.add_user_to_waitlist(title, author, name, phone, email)
        return True

    def get_waitlist(self, title, author):
        """Get the waitlist for a specific book."""
        book_key = StatisticsManager.generate_key(title, author)
        return self.library.get_waitlist(book_key)
