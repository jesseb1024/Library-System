from management.book import Book

class BookFactory:
    @staticmethod
    def create_book(title, author, is_loaned=False, copies=0, genre="", year=0, available=None):
        """Factory method to create a new book instance."""
        if not title or not author:
            raise ValueError("Title and Author cannot be empty")
        if copies < 0:
            raise ValueError("Copies cannot be negative")

        return Book(
            title=title.strip(),
            author=author.strip(),
            is_loaned=is_loaned,
            copies=copies,
            genre=genre.strip(),
            year=year,
            available=available
        )

