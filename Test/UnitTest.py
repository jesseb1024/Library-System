import os
import unittest
from unittest.mock import patch, MagicMock
from management.LibraryController import LibraryController
from management.StatisticsManager import StatisticsManager
from management.LibraryFileManager import LibraryFileManager
from users.librarian import LibrarianManager
from books.book import Book
from management.library import Library
import pandas as pd

class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        """Set up a clean state before each test."""
        self.library = Library()
        self.stats_manager = StatisticsManager(storage_file=os.path.abspath("../Test/TestStat.csv"))
        self.file_manager = LibraryFileManager(file_path=os.path.abspath("../files/books.csv"))
        self.controller = LibraryController(
            library=self.library,
            statistics_manager=self.stats_manager,
            file_path=os.path.abspath("../Test/TestBooks.csv")
        )

    def tearDown(self):
        """Clear the contents of CSV files after tests."""
        # Clear the contents of TestBooks.csv
        if os.path.exists("../Test/TestBooks.csv"):
            with open("../Test/TestBooks.csv", "w") as file:
                file.truncate(0)  # Clears the file content

        # Clear the contents of TestStats.csv
        if os.path.exists("../Test/TestStat.csv"):
            with open("../Test/TestStat.csv", "w") as file:
                file.truncate(0)  # Clears the file content

        df=pd.read_csv("../files/librarians.csv")
        last_row=df.index[-1]


        if df.loc[last_row, "username"] == "tester":
            df.drop(last_row,inplace=True)
            df.to_csv("../files/librarians.csv",index=False)


    def test_add_book(self):
        """Test adding a new book."""
        self.controller.add_book("Test Title", "Test Author", 5, "Fiction", 2021)
        books = self.library.get_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Test Title")
        self.assertEqual(books[0].request_counter, 0)


    def test_borrow_book_success(self):
        """Test borrowing a book with available copies."""
        self.controller.add_book("Test Title", "Test Author", 5, "Fiction", 2021)
        user = {"name": "Lidor", "email": "lidor@gmail.com", "phone": "111111"}
        success = self.controller.borrow_book("Test Title", "Test Author", user)
        self.assertTrue(success)
        book = self.library.books["test title:test author"]
        self.assertEqual(book.available, 4)
        self.assertEqual(book.request_counter, 1)

    def test_borrow_book_waitlist(self):
        """Test adding a user to the waitlist when no copies are available."""
        self.controller.add_book("Test Title", "Test Author", 1, "Fiction", 2021)
        user1 = {"name": "Lidor", "email": "lidor@gmail.com", "phone": "111111"}
        user2 = {"name": "Jessy", "email": "Jessy@gmail.com", "phone": "222222"}
        self.controller.borrow_book("Test Title", "Test Author", user1)  # First user borrows the book
        success = self.controller.borrow_book("Test Title", "Test Author", user2)
        self.assertFalse(success)
        waitlist = self.stats_manager.get_waitlist("test title:test author")
        self.assertEqual(len(waitlist), 1)
        self.assertEqual(waitlist[0]["name"], "Jane Doe")

    def test_return_book(self):
        """Test returning a borrowed book."""
        self.controller.add_book("Test Title", "Test Author", 1, "Fiction", 2021)
        user = {"name": "Jessy", "email": "Jessy@gmail.com", "phone": "222222"}
        self.controller.borrow_book("Test Title", "Test Author", user)
        self.controller.return_book("Test Title", "Test Author")
        book = self.library.books["test title:test author"]
        self.assertEqual(book.available, 1)
        self.assertFalse(book.is_loaned)


    def test_register_librarian(self):
        """Test registering a new librarian."""
        self.controller.register_librarian("tester", "tester123", "password")
        df=pd.read_csv("../files/librarians.csv")
        last_row=df.iloc[-1]
        self.assertTrue(last_row["username"]=="tester" and last_row["id"]=="tester123" and last_row["password_hash"] != "password")


    def test_authenticate_librarian(self):
        """Test authenticating a librarian."""
        self.controller.register_librarian("tester", "tester123", "password")
        librarian = self.controller.authenticate_librarian("tester", "tester123", "password")
        self.assertIsNone(librarian)

        with self.assertRaises(PermissionError):
            self.controller.authenticate_librarian("Admin", "admin123", "wrongpassword")

if __name__ == "_main_":
    unittest.main()