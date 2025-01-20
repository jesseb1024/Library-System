import csv

import pandas as pd
import os
import logging
from Library_Controls.StatisticsManager import StatisticsManager
from books.book import Book

logging.basicConfig(filename="../files/library_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")


class LibraryFileManager:
    def __init__(self, file_path="data/books.csv", available_file="available_books.csv", loaned_file="loaned_books.csv"):
        self.file_path = file_path
        self.available_file = available_file
        self.loaned_file = loaned_file

    def save_books(self, library, statistics_manager):
        """Save all book data to CSV files."""
        try:
            books = library.get_all_books()

            # Save all books to books.csv
            self._save_to_csv(
                self.file_path,
                [
                    {
                        "title": book.title,
                        "author": book.author,
                        "is_loaned": "yes" if book.is_loaned else "no",
                        "copies": book.copies,
                        "genre": book.genre,
                        "year": book.year,
                        "available": book.available_copies,
                        "request_counter": statistics_manager.get_request_count(
                            StatisticsManager.generate_key(book.title, book.author)
                        ),
                        "waitlist": ";".join(statistics_manager.get_waitlist(
                            StatisticsManager.generate_key(book.title, book.author)
                        ))
                    }
                    for book in books.values()
                ]
            )

            # Save available books to available_books.csv
            self._save_to_csv(
                self.available_file,
                [
                    {
                        "title": book.title,
                        "author": book.author,
                        "copies": book.available_copies
                    }
                    for book in books.values() if not book.is_loaned
                ]
            )

            # Save loaned books to loaned_books.csv
            self._save_to_csv(
                self.loaned_file,
                [
                    {
                        "title": book.title,
                        "author": book.author,
                        "copies": book.copies - book.available_copies
                    }
                    for book in books.values() if book.is_loaned
                ]
            )

            logging.info("Books saved successfully to all CSV files.")
        except Exception as e:
            logging.error(f"Failed to save books: {e}")
            raise

    def load_books(self, library, statistics_manager):
        """Load book data from books.csv into the library."""
        try:
            if not os.path.exists(self.file_path):
                logging.warning(f"File {self.file_path} not found. No books loaded.")
                return

            with open(self.file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book = Book.from_dict(row)
                    if book is None:  # Ensure invalid rows are skipped
                        continue
                    book_key = StatisticsManager.generate_key(book.title, book.author)
                    library.add_book(book, book_key)  # Pass both the book and book_key
                    statistics_manager.request_counts[book_key] = book.request_counter
                    statistics_manager.waiting_list[book_key] = book.waitlist

            logging.info("Books loaded successfully from CSV.")
        except Exception as e:
            logging.error(f"Failed to load books: {e}")
            raise

    def _save_to_csv(self, file_path, data):
        """Helper function to save data to a CSV file."""
        try:
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False, encoding="utf-8")
            logging.info(f"Data saved successfully to {file_path}.")
        except Exception as e:
            logging.error(f"Failed to save data to {file_path}: {e}")
            raise