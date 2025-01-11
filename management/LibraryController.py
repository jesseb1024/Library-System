from management.StatisticsManager import StatisticsManager

class LibraryController:
    def __init__(self, library):
        self.library = library
        self.stats_manager = library.stat_manager
        self.current_user = None  # Store the currently authenticated librarian

    def authenticate_librarian(self, username, password, librarian_manager):
        """Authenticate the librarian before accessing the system."""
        librarian = librarian_manager.authenticate(username, password)
        if librarian:
            print(f"Access granted to {librarian.username}")
            self.current_user = librarian
        else:
            raise PermissionError("Invalid username or password")

    def require_authentication(func):
        """Decorator to ensure operations are done by authenticated librarians."""

        def wrapper(self, *args, **kwargs):
            if not self.current_user:
                raise PermissionError("You must be logged in as a librarian to perform this action")
            return func(self, *args, **kwargs)

        return wrapper

    @require_authentication
    def add_book(self, title, author, copies, genre, year):
        """Add a new book (requires authentication)."""
        return self.library.add_book(title, author, copies, genre, year)

    @require_authentication
    def remove_book(self, title, author):
        """Remove a book (requires authentication)."""
        return self.library.remove_book(title, author)

    # Wrap the other methods with the @require_authentication decorator as needed


    def add_book(self, title, author, copies, genre, year):
        """Add a new book through the controller."""
        if not isinstance(copies, int) or copies < 0:
            raise ValueError("Copies must be a non-negative integer")
        if not isinstance(year, int):
            raise ValueError("Year must be an integer")
        return self.library.add_book(title, author, copies, genre, year)

    def remove_book(self, title, author):
        """Remove a book through the controller."""
        return self.library.remove_book(title, author)

    def borrow_book(self, title, author):
        """Borrow a book through the controller."""
        return self.library.borrow_book(title, author)

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

    def get_waitlist(self):
        """Get waitlist information - currently returns None as not implemented."""
        return None
