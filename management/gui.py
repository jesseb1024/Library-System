from tkinter import ttk, messagebox
import tkinter as tk
from tkinter.font import Font

from management.LibraryFileManager import LibraryFileManager
from management.StatisticsManager import StatisticsManager
from management.librarian import LibrarianManager


class LibraryGUI:
    def __init__(self, controller):
        self.controller = controller

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Library Management System")

        # Initialize GUI components
        self.book_list = None  # TreeView for book details

        # Display login screen initially
        self.librarian_manager = LibrarianManager()
        self.librarian = None
        self.login_screen()

    def login_screen(self):
        """Create a login screen for librarian authentication."""
        login_frame = tk.Frame(self.root)
        login_frame.pack(expand=True)

        tk.Label(login_frame, text="Librarian Login", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(login_frame, text="Username").pack(pady=5)
        username_entry = tk.Entry(login_frame)
        username_entry.pack()

        tk.Label(login_frame, text="Password").pack(pady=5)
        password_entry = tk.Entry(login_frame, show="*")
        password_entry.pack()

        error_label = tk.Label(login_frame, text="", fg="red")
        error_label.pack()

        def on_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            try:
                self.controller.authenticate_librarian(username, password, self.librarian_manager)
                login_frame.destroy()
                self.create_dashboard()
            except PermissionError as e:
                error_label.config(text=str(e))

        login_button = tk.Button(login_frame, text="Login", command=on_login)
        login_button.pack(pady=10)

    def create_dashboard(self):
        """Create the main library dashboard after login."""
        self.create_widgets()
        self.create_action_buttons()
        self.create_book_list_table()
        self.update_book_list()

    def create_widgets(self):
        """Create essential widgets for the dashboard."""
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
        self.search_entry.bind("<FocusOut>", lambda event: self.restore_placeholder())
        self.search_entry.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Search Button
        search_button = ttk.Button(search_frame, text="Search", command=self.search_books)
        search_button.grid(row=0, column=1, padx=10, sticky="w")

    def create_action_buttons(self):
        """Create action buttons for the main dashboard."""
        button_frame = tk.Frame(self.root, pady=10, padx=30)
        button_frame.pack(fill=tk.X)

        actions = [
            ("Add Book", self.add_book),
            ("All Books", self.update_book_list),
            ("Borrow Book", self.borrow_book),
            ("Return Book", self.return_book),
            ("Remove Book", self.remove_book),
            ("Available Books", self.display_available_books),
            ("Popular Books", self.display_popular_books),
            ("Waitlist", self.display_waitlist),
            ("Logout", self.root.destroy)
        ]

        for i, (text, command) in enumerate(actions):
            button = ttk.Button(button_frame, text=text, command=command)
            button.grid(row=0, column=i, padx=5, pady=5)

    def create_book_list_table(self):
        """Set up the TreeView for displaying book data."""
        tree_frame = tk.Frame(self.root, pady=10, padx=10)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Title", "Author", "Loaned", "Copies", "Genre", "Year", "Available")
        self.book_list = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        for column in columns:
            self.book_list.heading(column, text=column)

        self.book_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.book_list.yview)
        self.book_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def clear_placeholder(self):
        """Clear the placeholder in the search field."""
        if self.search_entry.get() == "Search by title or author...":
            self.search_entry.delete(0, tk.END)

    def restore_placeholder(self, event=None):
        """Restore the placeholder text if the search bar is empty."""
        if not self.search_entry.get().strip():
            self.search_entry.insert(0, "Search by title or author...")

    def update_book_list(self):
        """Update the TreeView with books from the library."""
        # Clear current list
        for row in self.book_list.get_children():
            self.book_list.delete(row)

        # Populate the list with books
        for book in self.controller.get_books():
            loan_status = "yes" if book.is_loaned else "no"
            self.book_list.insert(
                "", tk.END,
                values=(book.title, book.author, loan_status, book.copies, book.genre, book.year, book.available)
            )

    def add_book(self):
        """GUI dialog for adding a new book to the library."""

        def save_book():
            try:
                # Retrieve user input
                title = title_entry.get().strip()
                author = author_entry.get().strip()
                genre = genre_entry.get().strip()
                year = int(year_entry.get().strip())
                copies = int(copies_entry.get().strip())

                # Add book via controller
                self.controller.add_book(title, author, copies, genre, year)
                self.update_book_list()
                messagebox.showinfo("Success", f"Book '{title}' added successfully!")
                add_book_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        # Create popup window
        add_book_window = tk.Toplevel(self.root)
        add_book_window.title("Add Book")

        # Form fields
        book_fields = [("Title", ""), ("Author", ""), ("Genre", ""), ("Year", ""), ("Copies", "")]
        entries = []

        for i, (label, value) in enumerate(book_fields):
            tk.Label(add_book_window, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(add_book_window)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)

        # Assign entries for reuse in save_book
        title_entry, author_entry, genre_entry, year_entry, copies_entry = entries

        ttk.Button(add_book_window, text="Save", command=save_book).grid(row=len(book_fields), columnspan=2, pady=10)

    def borrow_book(self):
        """Borrow a selected book."""
        selected_item = self.book_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to borrow.")
            return

        book_data = self.book_list.item(selected_item)['values']
        title, author = book_data[0], book_data[1]

        try:
            self.controller.borrow_book(title, author)
            self.update_book_list()
            messagebox.showinfo("Success", f"Borrowed '{title}' successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def return_book(self):
        """Return a selected book."""
        selected_item = self.book_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to return.")
            return

        book_data = self.book_list.item(selected_item)['values']
        title, author = book_data[0], book_data[1]

        try:
            self.controller.return_book(title, author)
            self.update_book_list()
            messagebox.showinfo("Success", "Book returned successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_book(self):
        """Remove a selected book."""
        selected_item = self.book_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to remove.")
            return

        book_data = self.book_list.item(selected_item)['values']
        title, author = book_data[0], book_data[1]

        try:
            self.controller.remove_book(title, author)
            self.update_book_list()
            messagebox.showinfo("Success", f"Removed book '{title}'.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def search_books(self):
        """Search books by title or author."""
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showinfo("Search", "Please enter a search term.")
            return

        # Clear book list
        for row in self.book_list.get_children():
            self.book_list.delete(row)

        # Display search results
        matching_books = [
            book for book in self.controller.get_books()
            if query in book.title.lower() or query in book.author.lower()
        ]

        if not matching_books:
            messagebox.showinfo("Search", "No books found.")
        else:
            for book in matching_books:
                loan_status = "yes" if book.is_loaned else "no"
                self.book_list.insert(
                    "", tk.END,
                    values=(book.title, book.author, loan_status, book.copies, book.genre, book.year, book.available)
                )

    def display_available_books(self):
        """Display books with available copies."""
        available_books = self.controller.get_available_books()
        self.display_books_popup("Available Books", available_books)

    def display_popular_books(self):
        """Display popular books sorted by request count."""
        popular_books = self.controller.get_popular_books()
        self.display_books_popup("Popular Books", popular_books)

    def display_waitlist(self):
        """Display books on the waitlist."""
        waitlist = self.controller.get_waitlist()
        self.waitlist_popup("Waitlist", waitlist)

    def waitlist_popup(self, title, members):
        """Show a list of members in a popup window."""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("800x400")

    def display_books_popup(self, title, books):
        """Show a list of books in a popup window."""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("800x400")

        columns = ("Title", "Author", "Copies", "Genre", "Year", "Available", "Requests")
        book_list = ttk.Treeview(popup, columns=columns, show='headings')

        for column in columns:
            book_list.heading(column, text=column)

        for book in books:
            # Safeguard against missing stat_manager
            if hasattr(book, 'stat_manager') and book.stat_manager:
                request_count = book.stat_manager.get_request_count(
                    StatisticsManager.generate_key(book.title, book.author)
                )
            else:
                request_count = book.copies-book.available

            book_list.insert(
                "", tk.END,
                values=(book.title, book.author, book.copies, book.genre, book.year, book.available, request_count)
            )

        book_list.pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()
