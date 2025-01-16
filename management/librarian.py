import hashlib


class Librarian:
    """Class representing a Librarian with authentication capabilities."""

    def __init__(self, username, id, password):
        self.username = username
        self.id = id
        self.password_hash = self._hash_password(password)

    @staticmethod
    def _hash_password(password):
        """Hash a password using SHA-256 for secure storage."""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        """Verify if the entered password matches the stored hash."""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def is_id_valid(self, id_to_verify):
        """Verify if the entered ID matches the stored ID."""
        return self.id == id_to_verify


class LibrarianManager:
    """Handles librarian authentication and management."""

    def __init__(self):
        # Simulating a database of users
        self.librarians = {
            "admin": Librarian("admin", "1223", "admin"),
        }

    def add_librarian(self, username, id, password):
        """Add a new librarian to the database."""
        if id in self.librarians:
            raise ValueError("Librarian already exists.")
        self.librarians[id] = Librarian(username, id, password)


    def authenticate(self, username, id, password):
        """Authenticate a librarian by username, id and password."""
        librarian = self.librarians.get(username, id)
        if librarian and librarian.verify_password(password) and librarian.is_id_valid(id):
            return librarian
        return None
