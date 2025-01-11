import os
import pandas as pd
import logging
from management.BookFactory import BookFactory
from management.StatisticsManager import StatisticsManager

class LibraryFileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.stat_manager = StatisticsManager()



    def load_books(self):
        """Load book data from a CSV file."""
        if not os.path.exists(self.file_path):
            # Return empty dictionaries if the file does not exist
            return {}, {}

        try:
            logging.info("Loading books from file...")
            df = pd.read_csv(self.file_path)
            # Convert the CSV data into books and request counts
            books = {
                StatisticsManager.generate_key(row["title"], row["author"]): BookFactory.create_book(
                    title=row["title"],
                    author=row["author"],
                    is_loaned=row["is_loaned"].strip().lower() in ("true", "yes"),
                    copies=int(row["copies"]),
                    genre=row["genre"],
                    year=int(row["year"]),
                    available=int(row["available"]),
                )

                for _, row in df.iterrows()
            }
            request_counts = {
                StatisticsManager.generate_key(row["title"], row["author"]): int(row["request_counter"])
                for _, row in df.iterrows()

            }

            self.stat_manager.load_statistics(request_counts)
            return books, request_counts
        except Exception as e:
            raise RuntimeError(f"Error loading books from file: {e}")

    def save_books(self, books, request_counts):
        """Save book data to a CSV file."""
        df = pd.DataFrame([
            {
                "title": book.title,
                "author": book.author,
                "is_loaned": "yes" if book.is_loaned else "no",
                "copies": book.copies,
                "genre": book.genre,
                "year": book.year,
                "available": book.available,
                "request_counter": request_counts.get(StatisticsManager.generate_key(book.title, book.author),0)
            }
            for book in books.values()
        ])
        df.to_csv(self.file_path, index=False, encoding="utf-8")
