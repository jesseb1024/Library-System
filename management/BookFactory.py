from management.book import Book


class BookFactory:
    """Factory class to create Book instances."""

    @staticmethod
    def create_book(title, author, is_loaned=False, copies=0, genre="", year=0, available=0):
        """
        Factory method to create a new book instance.

        Args:
            title (str): The book title.
            author (str): The book's author.
            is_loaned (bool): Whether the book is currently loaned out (default: False).
            copies (int): The total number of copies available in the library.
            genre (str): The book's genre/category.
            year (int): The publication year (default: 0).

        Returns:
            Book: A new `Book` object.
        """
        # Validation (can be extended)
        if not title or not author:
            raise ValueError("Title and Author cannot be empty.")

        if copies < 0:
            raise ValueError("Copies cannot be a negative number.")

        return Book(
            title=title.strip(),
            author=author.strip(),
            is_loaned=is_loaned,
            copies=copies,
            genre=genre.strip(),
            year=year,
            available=available
        )


