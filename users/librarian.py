import csv
import hashlib
import logging
import os

# Ensure the log directory exists
log_dir = os.path.dirname("../library_log.txt")
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(filename=os.path.abspath("../library_log.txt"), level=logging.INFO, format="%(asctime)s - %(message)s")


class Librarian:
    """Represents a single librarian with encrypted password storage."""

    def __init__(self, username, id, password):
        self.username = username
        self.id = id
        self.password_hash = self._hash_password(password)

    def get_password(self):
        return self.password_hash

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    @staticmethod
    def _hash_password(password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        """Verify if the entered password matches the stored hash."""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def to_dict(self):
        """Convert librarian details to a dictionary for CSV storage."""
        return {"username": self.username, "id": self.id, "password_hash": self.password_hash}

    @staticmethod
    def from_dict(data):
        """Create a Librarian object from a dictionary."""
        librarian = Librarian(data["username"], data["id"], "")
        librarian.password_hash = data["password_hash"]
        return librarian


class LibrarianManager:
    """Manages librarian registration and authentication."""

    def __init__(self, file_path=os.path.abspath("../files/librarians.csv")):
        self.file_path = file_path
        self.librarians = {}  # Dictionary to store librarians by ID
        self._load_librarians()

    def _load_librarians(self):
        """Load librarians from the CSV file."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    librarian = Librarian.from_dict(row)
                    self.librarians[librarian.id] = librarian
        except FileNotFoundError:
            logging.warning("Users file not found. Starting with an empty database.")

    def _save_librarians(self):
        """Save librarians to the CSV file."""
        with open(self.file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "id", "password_hash"])
            writer.writeheader()
            for librarian in self.librarians.values():
                writer.writerow(librarian.to_dict())

    def add_librarian(self, username, id, password):
        """Register a new librarian."""
        if id in self.librarians:
            logging.error(f"Registration failed: ID '{id}' already exists.")
            raise ValueError(f"Librarian with ID '{id}' already exists.")
        self.librarians[id] = Librarian(username, id, password)
        self._save_librarians()
        logging.info(f"Librarian '{username}' registered successfully.")

    def is_librarian_registered(self, id):
        """Check if a librarian with the given username is already registered."""
        return id in self.librarians

    def authenticate(self, username, id, password):
        """Authenticate a librarian by username, ID, and password."""
        librarian = self.librarians.get(id)
        if librarian and librarian.username == username and librarian.verify_password(password):
            logging.info(f"Librarian '{username}' logged in successfully.")
            return librarian
        logging.error(f"Authentication failed for username '{username}' and ID '{id}'.")
        return None
