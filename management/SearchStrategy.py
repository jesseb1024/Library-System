from abc import ABC, abstractmethod
import pandas as pd
from tkinter import messagebox
import tkinter as tk
import os

from files.Log import add_log


df = pd.read_csv(os.path.abspath("../files/books.csv"))

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, query, books, controller):
        pass

    @staticmethod
    def add_logs(caller, flag):
        if caller == "BookName" and flag == "successfully":
            add_log('Search for book by name completed successfully.', "info")
        elif caller == "BookName" and flag == "fail":
            add_log('Search for book by name failed.', "info")
        elif caller == "AuthorName" and flag == "successfully":
            add_log('Search for book by author completed successfully.', "info")
        elif caller == "AuthorName" and flag == "fail":
            add_log('Search for book by author failed.', "info")
        elif caller == "AllBooks" and flag == "successfully":
            add_log('Displayed all books successfully.', "info")
        elif caller == "AllBooks" and flag == "fail":
            add_log('Failed to display all books.', "info")
        elif caller == "AvailableBooks" and flag == "successfully":
            add_log('Displayed available books successfully.', "info")
        elif caller == "AvailableBooks" and flag == "fail":
            add_log('Failed to display available books.', "info")
        elif caller == "BorrowedBooks" and flag == "successfully":
            add_log('Displayed borrowed books successfully.', "info")
        elif caller == "BorrowedBooks" and flag == "fail":
            add_log('Failed to display borrowed books.', "info")
        elif caller == "Category" and flag == "successfully":
            add_log('Displayed books by category successfully.', "info")
        elif caller == "Category" and flag == "fail":
            add_log('Failed to display books by category.', "info")

    @staticmethod
    def update_book_list(func):
        def wrapper(self, query, books, books_in_lib):
            result = func(self, query, books, books_in_lib)

            matching_books ,caller = result

            if matching_books is None:
                return

            if not matching_books :
                SearchStrategy.add_logs(caller, "fail")
                messagebox.showinfo("Search", "No books found.")
            else:
                SearchStrategy.add_logs(caller, "successfully")
                books.delete(*books.get_children())
                for book in matching_books:
                    books.insert(
                        "", tk.END,
                        values=(book.title,book.author,"yes" if book.is_loaned else "no",book.copies,book.genre, book.year,book.available,book.request_counter))

        return wrapper


class SearchBookName(SearchStrategy):
    @SearchStrategy.update_book_list
    def search(self, query, books, books_in_lib):
        if not query or query == "Enter book name..." or query == "Enter book author...":
            messagebox.showinfo("Search", "Please enter a search term.")
            return
        return [book for book in books_in_lib if query.lower() in book.title.lower()],"BookName"


class SearchAuthorName(SearchStrategy):
    @SearchStrategy.update_book_list
    def search(self, query, books, books_in_lib):
        if not query or query == "Enter book name..." or query == "Enter book author...":
            messagebox.showinfo("Search", "Please enter a search term.")
            return
        return [book for book in books_in_lib if query.lower() in book.author.lower()],"AuthorName"


class SearchAllBooks(SearchStrategy):
    @SearchStrategy.update_book_list
    def search(self, query, books, books_in_lib):
        return [book for book in books_in_lib],"AllBooks"


class SearchAvailableBooks(SearchStrategy):
    @SearchStrategy.update_book_list
    def search(self, query, books, books_in_lib):
        return [book for book in books_in_lib if book.available > 0],"AvailableBooks"


class SearchBorrowedBooks(SearchStrategy):
    @SearchStrategy.update_book_list
    def search(self, query, books, books_in_lib):
        return [book for book in books_in_lib if book.is_loaned],"BorrowedBooks"


class SearchCategory(SearchStrategy):
    @SearchStrategy.update_book_list
    def search(self, query, books, books_in_lib):
        if query == "Categories":
            return [],"category"
        return [book for book in books_in_lib if query == book.genre],"Category"


class Search:
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def search(self, query, books, controller):
        self.strategy.search(query, books, controller)