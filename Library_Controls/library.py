from Library_Controls.StatisticsManager import StatisticsManager
from books.book import Book


class Library:
    FILE_PATH_NOT_PROVIDED_ERROR = "File path is not provided."

    def __init__(self, file_path=None):
        self.books_file_path = file_path
        self.books = {}  # Dictionary keyed by book_key

    def load_books_from_file(self):
        if not self.books_file_path:
            raise ValueError(self.FILE_PATH_NOT_PROVIDED_ERROR)
        try:
            with open(self.books_file_path, 'r') as file:
                for line in file:
                    book = self._parse_book_line(line)
                    if book:
                        self.add_book(book)
        except FileNotFoundError:
            print(f"File not found: {self.books_file_path}")
        except Exception as e:
            print(f"Error loading books: {type(e).__name__} - {e}")

    def add_book(self, book, book_key=None):
        if not isinstance(book, Book):
            raise TypeError(f"Expected a Book object, but got {type(book).__name__}")
        if book_key is None:
            book_key = StatisticsManager.generate_key(book.title, book.author)
        self.books[book_key] = book

    def has_book(self, book_key):
        return book_key in self.books

    def get_books(self):
        # Return the books as a list
        return list(self.books.values())

    @staticmethod
    def _parse_book_line(line):
        try:
            title,author,is_loaned,copies,genre,year,available,request_counter,waitlist = line.strip().split(',')
            return Book(title=title, author=author, is_loaned=is_loaned == 'yes', copies=int(copies), genre=genre, year=int(year), available=int(available), request_counter=int(request_counter), waitlist=waitlist.split(';'))
        except ValueError:
            print(f"Invalid book data: {line.strip()}")
            return None