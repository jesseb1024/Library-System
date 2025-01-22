import csv
import pandas as pd
import os
import logging
from management.StatisticsManager import StatisticsManager
from books.book import Book



class LibraryFileManager:
    def __init__(self, file_path="books.csv"):
        self.file_path = file_path

    def save_books(self, library, statistics_manager):
        """Save all book data to CSV."""
        try:
            books = library.get_books()  # Returns a list of Book objects

            # Prepare data for saving
            data = [
                {
                    "title": book.title,
                    "author": book.author,
                    "is_loaned": "yes" if book.is_loaned else "no",
                    "copies": book.copies,
                    "genre": book.genre,
                    "year": book.year,
                    "available": book.available,
                    "request_counter": book.request_counter  # Save correct request counter
                }
                for book in books
            ]

            # Save to CSV
            self._save_to_csv(self.file_path, data)
            logging.info("Books saved successfully.")
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
                        if book:
                            book_key = StatisticsManager.generate_key(book.title, book.author)
                            library.add_book(book, book_key)
                            statistics_manager.request_counts[book_key] = book.request_counter  # Sync with stats
                    statistics_manager.waiting_list[book_key] = book.waitlist

            logging.info("Books loaded successfully from CSV.")
        except Exception as e:
            logging.error(f"Failed to load books: {e}")
            raise

    def _save_to_csv(self, file_path, data):
        """Helper function to save data to a CSV file."""
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            logging.info(f"Data saved successfully to {file_path}.")
        except Exception as e:
            logging.error(f"Failed to save data to {file_path}: {e}")
            raise