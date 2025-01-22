from abc import ABC, abstractmethod
import pandas as pd
from tkinter import messagebox
import tkinter as tk



df = pd.read_csv(r"C:\Users\97253\PycharmProjects\Library-System2\files\books.csv")

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, query, books,controller):
        pass

    @staticmethod
    def update_book_list(books,matching_books):
        if not matching_books:
            messagebox.showinfo("Search", "No books found.")
        else:

            books.delete(*books.get_children())
            for book in matching_books:
                books.insert(
                    "", tk.END,
                    values=(book.title, book.author, "yes" if book.is_loaned else "no", book.copies,
                            book.genre, book.year, book.available, book.request_counter)
                )

class SearchByBookName (SearchStrategy):
    def search(self, query, books,books_in_lib):
        if not query or query == "Enter book name..." or query == "Enter book author...":
            messagebox.showinfo("Search", "Please enter a search term.")
            return

        matching_books = [book for book in books_in_lib if query in book.title.lower()]
        SearchStrategy.update_book_list(books, matching_books)

class SearchByAuthorName(SearchStrategy):
    def search(self, query, books,books_in_lib):
        if not query or query == "Enter book name..." or query == "Enter book author...":
            messagebox.showinfo("Search", "Please enter a search term.")
            return

        matching_books = [book for book in books_in_lib if query in book.author.lower()]
        SearchStrategy.update_book_list(books, matching_books)

class SearchAllBooks(SearchStrategy):
    def search(self, query, books,books_in_lib):
        matching_books = [book for book in books_in_lib]
        SearchStrategy.update_book_list(books, matching_books)

class SearchAvailableBooks(SearchStrategy):
    def search(self, query, books,books_in_lib):
        matching_books = [book for book in books_in_lib if book.available>0]
        SearchStrategy.update_book_list(books, matching_books)

class SearchBorrowedBooks(SearchStrategy):
    def search(self, query, books,books_in_lib):
        matching_books = [book for book in books_in_lib if book.is_loaned]
        SearchStrategy.update_book_list(books, matching_books)

class SearchCategory(SearchStrategy):
    def search(self, query, books,books_in_lib):
        matching_books = [book for book in books_in_lib if query in book.genre]
        SearchStrategy.update_book_list(books, matching_books)

class Search:
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def search(self, query,books,controller):
        self.strategy.search(query,books,controller)
#