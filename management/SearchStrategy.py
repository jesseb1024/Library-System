import logging
from abc import ABC, abstractmethod
import pandas as pd
from tkinter import messagebox
import tkinter as tk
import os

df = pd.read_csv(os.path.abspath("../files/books.csv"))

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, query, books,controller):
        pass


    @staticmethod
    def update_book_list(fanc):
        def wrapper(self,query,books,matching_books):
            matching_books= fanc(self,query,books,matching_books)

            if matching_books is None:
                return

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
        return wrapper



class SearchByBookName (SearchStrategy):
    @SearchStrategy.update_book_list
    def search(self, query, books,books_in_lib):
        if not query or query == "Enter book name..." or query == "Enter book author...":
            messagebox.showinfo("Search", "Please enter a search term.")
            return

        return [book for book in books_in_lib if query in book.title.lower()]


class SearchByAuthorName(SearchStrategy):
    @SearchStrategy.update_book_list
    def search(self, query, books,books_in_lib):
        if not query or query == "Enter book name..." or query == "Enter book author...":
            messagebox.showinfo("Search", "Please enter a search term.")
            return

        return [book for book in books_in_lib if query in book.author.lower()]


class SearchAllBooks(SearchStrategy):
    @SearchStrategy.update_book_list
    def search(self, query, books,books_in_lib):
        return [book for book in books_in_lib]


class SearchAvailableBooks(SearchStrategy):
    @SearchStrategy.update_book_list
    def search(self, query, books,books_in_lib):
        return [book for book in books_in_lib if book.available>0]


class SearchBorrowedBooks(SearchStrategy):
    @SearchStrategy.update_book_list
    def search(self, query, books,books_in_lib):
        return [book for book in books_in_lib if book.is_loaned]

class SearchCategory(SearchStrategy):
    @SearchStrategy.update_book_list
    def search(self, query, books,books_in_lib):
        if query == "Categories":
            return
        else:
            return [book for book in books_in_lib if query == book.genre]

class Search:
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def search(self, query,books,controller):
        self.strategy.search(query,books,controller)
