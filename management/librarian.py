import hashlib


class Librarian:
    """Class representing a Librarian with authentication capabilities."""

    def __init__(self, username, password):
        self.username = username
        self.password_hash = self._hash_password(password)

    @staticmethod
    def _hash_password(password):
        """Hash a password using SHA-256 for secure storage."""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        """Verify if the entered password matches the stored hash."""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()


class LibrarianManager:
    """Handles librarian authentication and management."""

    def __init__(self):
        # Simulating a database of users
        self.librarians = {
            "jesse": Librarian("jesse", "12345"),
            "lidor": Librarian("lidor", "12345")
        }

    def authenticate(self, username, password):
        """Authenticate a librarian by username and password."""
        librarian = self.librarians.get(username)
        if librarian and librarian.verify_password(password):
            return librarian
        return None
