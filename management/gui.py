from management.BookFactory import BookFactory
from management.book import Book
from management.library import Library
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font


class LibraryGUI:
    def __init__(self, library):

        self.available_books_window = None
        self.book_list = None
        self.library = library
        self.available_books_list = None

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Library System")
        self.root.geometry("800x600")  # Set window size

        # Apply a theme
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")  # Modern theme
        self.style.configure("Treeview", rowheight=30)

        # Create a custom font
        self.header_font = Font(family="Helvetica", size=14, weight="bold")
        self.button_font = Font(family="Arial", size=12)

        # Initialize the GUI components
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(
            self.root,
            text="Library Management System",
            font=("Helvetica", 18, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=10
        )
        title_label.pack(fill=tk.X)

        # Search Frame
        search_frame = tk.Frame(self.root, pady=10, padx=10)
        search_frame.pack(fill=tk.X)

        # Search Entry
        self.search_entry = ttk.Entry(search_frame, width=50, font=("Arial", 12))
        self.search_entry.insert(0, "Search by title or author...")
        self.search_entry.bind("<FocusIn>", lambda event: self.clear_placeholder())
        self.search_entry.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Search Button
        search_button = ttk.Button(search_frame, text="Search", command=self.search_books)
        search_button.grid(row=0, column=1, padx=10, sticky="e")

        # Action Buttons Frame
        button_frame = tk.Frame(self.root, pady=10, padx=10)
        button_frame.pack(fill=tk.X)

        actions = [
            ("Add Book", self.add_book),
            ("All Books", self.load_books),
            ("Borrow Book", self.borrow_book),
            ("Return Book", self.return_book),
            ("Remove Book", self.remove_book),
            ("Available Books", self.display_available_books),
        ]

        for i, (text, command) in enumerate(actions):
            button = ttk.Button(button_frame, text=text, command=command)
            button.grid(row=0, column=i, padx=5, pady=5)

        # TreeView for Books
        tree_frame = tk.Frame(self.root, pady=10, padx=10)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.book_list = ttk.Treeview(
            tree_frame,
            columns=("Title", "Author", "Loaned", "Copies", "Genre", "Year", "Available"),
            show="headings",
            selectmode="browse",
        )

        self.book_list.heading("Title", text="Title"),
        self.book_list.heading("Author", text="Author"),
        self.book_list.heading("Loaned", text="Loaned"),
        self.book_list.heading("Copies", text="Copies"),
        self.book_list.heading("Genre", text="Genre"),
        self.book_list.heading("Year", text="Year"),
        self.book_list.heading("Available", text="Available copies", anchor="w"),
        self.book_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT),

        # Alternating Row Colors
        self.style.map("Treeview", background=[("selected", "#DDEBF7")])

        # Scrollbars for TreeView
        y_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.book_list.yview)
        self.book_list.configure(yscrollcommand=y_scrollbar.set)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load Initial Data
        self.update_book_list()

    def clear_placeholder(self):
        if self.search_entry.get() == "Search by title or author...":
            self.search_entry.delete(0, tk.END)

    def search_books(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showinfo("Search", "Please enter a search term.")
            return

        # Clear existing data
        for row in self.book_list.get_children():
            self.book_list.delete(row)

        # Find matching books
        matching_books = [
            book for book in self.library.books.values()
            if query in book.title.lower() or query in book.author.lower()
        ]

        if not matching_books:
            messagebox.showinfo("Search", "No books found.")
        else:
            for book in matching_books:
                self.book_list.insert(
                    "", tk.END,
                    values=(book.title, book.author, book.is_loaned, book.copies, book.genre, book.year)
                )

    def update_book_list(self):
        # Clear the current list
        for row in self.book_list.get_children():
            self.book_list.delete(row)

        # Populate the list with books
        for book in self.library.books.values():
            # Convert is_loaned boolean to "yes" or "no"
            is_loaned_display = "yes" if book.is_loaned else "no"
            self.book_list.insert(
                "", tk.END,
                values=(book.title, book.author, is_loaned_display, book.copies, book.genre, book.year, book.available)
            )

    def add_book(self):
        def save_book():
            try:
                # Get values from the entry fields
                title = title_entry.get().strip()
                author = author_entry.get().strip()
                genre = genre_entry.get().strip()
                year = int(year_entry.get().strip())
                copies = int(copies_entry.get().strip())

                # Use the factory to create a Book instance
                new_book = BookFactory.create_book(
                    title=title,
                    author=author,
                    is_loaned=False,  # New books are not loaned initially
                    copies=copies,
                    genre=genre,
                    year=year
                )

                # Add the book to the library
                self.library.add_book(new_book.title, new_book.author, new_book.copies, new_book.genre, new_book.year)

                # Refresh the book list in the GUI
                self.update_book_list()
                messagebox.showinfo("Success", f"Book '{title}' added successfully!")
                add_book_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        # Create the Add Book window
        add_book_window = tk.Toplevel(self.root)
        add_book_window.title("Add Book")

        # Define the entry fields within the scope of the outer function
        tk.Label(add_book_window, text="Title").grid(row=0, column=0, padx=5, pady=5)
        title_entry = tk.Entry(add_book_window)
        title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_book_window, text="Author").grid(row=1, column=0, padx=5, pady=5)
        author_entry = tk.Entry(add_book_window)
        author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_book_window, text="Genre").grid(row=2, column=0, padx=5, pady=5)
        genre_entry = tk.Entry(add_book_window)
        genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_book_window, text="Year").grid(row=3, column=0, padx=5, pady=5)
        year_entry = tk.Entry(add_book_window)
        year_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(add_book_window, text="Copies").grid(row=4, column=0, padx=5, pady=5)
        copies_entry = tk.Entry(add_book_window)
        copies_entry.grid(row=4, column=1, padx=5, pady=5)

        # Save button
        tk.Button(add_book_window, text="Save", command=save_book).grid(row=5, column=0, columnspan=2, pady=10)

    def load_books(self):
        try:
            self.library.load_books_from_csv("books.csv")
            self.update_book_list()
            messagebox.showinfo("Success", "Books loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load books: {e}")

    def borrow_book(self):
        selected_item = self.book_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to borrow.")
            return

        book_title = self.book_list.item(selected_item)["values"][0]
        book_author = self.book_list.item(selected_item)["values"][1]

        try:
            self.library.borrow_book(book_title, book_author)
            self.update_book_list()
            messagebox.showinfo("Success", f"Successfully borrowed '{book_title}'.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def return_book(self):
        selected_item = self.book_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to return.")
            return

        book_title = self.book_list.item(selected_item)["values"][0]
        book_author = self.book_list.item(selected_item)["values"][1]

        try:
            self.library.return_book(book_title, book_author)
            self.update_book_list()
            messagebox.showinfo("Success", f"Successfully returned '{book_title}'.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_book(self):
        selected_item = self.book_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to remove.")
            return

        # Get book details
        book_values = self.book_list.item(selected_item)["values"]
        title = book_values[0]
        author = book_values[1]

        # Remove book and update list
        self.library.remove_book(title, author)
        self.update_book_list()

    def display_available_books(self):
        """Displays only available books in a new window with a functional Borrow button."""
        available_books = self.library.get_available_books()

        # Create a new popup window for available books
        self.available_books_window = tk.Toplevel(self.root)
        self.available_books_window.title("Available Books")
        self.available_books_window.geometry("600x400")

        # TreeView to list available books
        self.available_books_list = ttk.Treeview(
            self.available_books_window,
            columns=("Title", "Author", "Copies", "Genre", "Year", "Available Copies"),
            show="headings",
            selectmode="browse"
        )
        self.available_books_list.heading("Title", text="Title")
        self.available_books_list.heading("Author", text="Author")
        self.available_books_list.heading("Copies", text="Copies")
        self.available_books_list.heading("Genre", text="Genre")
        self.available_books_list.heading("Year", text="Year")
        self.available_books_list.heading("Available Copies", text="Available Copies")
        self.available_books_list.pack(fill=tk.BOTH, expand=True)

        # Populate the TreeView with available books
        for book in available_books:
            self.available_books_list.insert(
                "",
                tk.END,
                values=(book.title, book.author, book.copies, book.genre, book.year, book.available)
            )

        # Add Borrow Button below the TreeView
        borrow_button = ttk.Button(
            self.available_books_window,
            text="Borrow",
            command=self.borrow_available_button
        )
        # Place the Borrow button in the popup window
        borrow_button.pack(pady=10)

    def borrow_available_button(self):
        """Handles borrowing a book from the Available Books popup."""
        # Ensure a book is selected in the Available Books TreeView
        selected_item = self.available_books_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to borrow.")
            return

        # Fetch selected book details
        book_values = self.available_books_list.item(selected_item)["values"]
        title = book_values[0]
        author = book_values[1]

        try:
            # Attempt to borrow the selected book
            self.library.borrow_book(title, author)

            # Update the main list of books in the main window
            self.update_book_list()

            # Refresh the Available Books popup window to update the list
            self.available_books_window.destroy()  # Close the current popup
            self.display_available_books()  # Reopen the popup with updated data

            # Notify the user of the successful borrow operation
            messagebox.showinfo("Success", f"Successfully borrowed '{title}'.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def display_popular_books(self):
        """Displays only popular books in a new window with specific headers."""
        popular_books = self.library.get_popular_books()

        # Create a new window for popular books
        popular_books_window = tk.Toplevel(self.root)
        popular_books_window.title("Popular Books")
        popular_books_window.geometry("600x400")

        # TreeView for Popular Books
        popular_books_list = ttk.Treeview(
            popular_books_window,
            columns=("Title", "Author", "Loaned Count", "Copies", "Available Copies", "Genre", "Year"),
            show="headings",
            selectmode="browse"
        )
        popular_books_list.heading("Title", text="Title")
        popular_books_list.heading("Author", text="Author")
        popular_books_list.heading("Loaned Count", text="Loaned Count")
        popular_books_list.heading("Copies", text="Copies")
        popular_books_list.heading("Available Copies", text="Available")
        popular_books_list.heading("Genre", text="Genre")
        popular_books_list.heading("Year", text="Year")
        popular_books_list.pack(fill=tk.BOTH, expand=True)

        for book in popular_books:
            loan_count = self.library.get_loan_count(book.title, book.author)
            popular_books_list.insert("", tk.END,
                                      values=(
                                      book.title, book.author, loan_count, book.copies, book.available, book.genre,
                                      book.year))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    library = Library()  # Create the library instance
    gui = LibraryGUI(library)  # Pass the library instance to the GUI
    gui.run()  # Start the GUI main loop
