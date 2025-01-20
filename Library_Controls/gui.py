from tkinter import ttk, messagebox, simpledialog
import tkinter as tk
from tkinter.font import Font


class LibraryGUI:
    def __init__(self, controller):
        self.controller = controller

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Library Management System")

        # Initialize GUI components
        self.book_list = None  # TreeView for book details
        self.search_entry = None

        # Display login screen initially
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

        tk.Label(login_frame, text="ID").pack(pady=5)
        id_entry = tk.Entry(login_frame)
        id_entry.pack()

        tk.Label(login_frame, text="Password").pack(pady=5)
        password_entry = tk.Entry(login_frame, show="*")
        password_entry.pack()

        error_label = tk.Label(login_frame, text="", fg="red")
        error_label.pack()

        def on_login():
            username = username_entry.get().strip()
            librarian_id = id_entry.get().strip()
            password = password_entry.get().strip()
            try:
                self.controller.authenticate_librarian(username, librarian_id, password)
                login_frame.destroy()
                self.create_dashboard()
            except PermissionError as e:
                error_label.config(text=str(e))

        tk.Button(login_frame, text="Login", command=on_login).pack(pady=10)
        tk.Button(login_frame, text="Register New Librarian",
                  command=lambda: [login_frame.destroy(), self.register_screen()]).pack(pady=5)

    def register_screen(self):
        """Create a registration screen for librarian registration."""
        register_frame = tk.Frame(self.root)
        register_frame.pack(expand=True)

        tk.Label(register_frame, text="Librarian Registration", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(register_frame, text="Username").pack(pady=5)
        username_entry = tk.Entry(register_frame)
        username_entry.pack()

        tk.Label(register_frame, text="ID").pack(pady=5)
        id_entry = tk.Entry(register_frame)
        id_entry.pack()

        tk.Label(register_frame, text="Password").pack(pady=5)
        password_entry = tk.Entry(register_frame, show="*")
        password_entry.pack()

        error_label = tk.Label(register_frame, text="", fg="red")
        error_label.pack()

        def on_register():
            username = username_entry.get().strip()
            librarian_id = id_entry.get().strip()
            password = password_entry.get().strip()

            if not username or not librarian_id or not password:
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                self.controller.register_librarian(username, librarian_id, password)
                messagebox.showinfo("Success", "Librarian registered successfully!")
                register_frame.destroy()
                self.login_screen()
            except ValueError as e:
                error_label.config(text=str(e))

        tk.Button(register_frame, text="Register", command=on_register).pack(pady=10)
        tk.Button(register_frame, text="Back to Login",
                  command=lambda: [register_frame.destroy(), self.login_screen()]).pack(pady=5)

    def create_dashboard(self):
        """Create the main library dashboard after login."""
        self.create_widgets()
        self.create_action_buttons()
        self.create_book_list_table()
        self.update_book_list()

    def create_widgets(self):
        """Create the header and search bar."""
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
        self.search_entry.insert(0, "Search by title, author, or genre...")
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
            ("Remove Book", self.remove_book),
            ("View All Books", self.update_book_list),
            ("Borrow Book", self.borrow_book),
            ("Return Book", self.return_book),
            ("View Waitlist", self.display_waitlist),
            ("Logout", self.logout)
        ]

        for i, (text, command) in enumerate(actions):
            button = ttk.Button(button_frame, text=text, command=command)
            button.grid(row=0, column=i, padx=5, pady=5)

    def create_book_list_table(self):
        """Set up the TreeView for displaying book data."""
        tree_frame = tk.Frame(self.root, pady=10, padx=10)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Columns match the books.csv order
        columns = ("title", "author", "is_loaned", "copies", "genre", "year", "available", "request_counter", "waitlist")
        self.book_list = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        for column in columns:
            self.book_list.heading(column, text=column.capitalize())

        self.book_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.book_list.yview)
        self.book_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def clear_placeholder(self):
        """Clear the placeholder in the search field."""
        if self.search_entry.get() == "Search by title, author, or genre...":
            self.search_entry.delete(0, tk.END)

    def restore_placeholder(self, event=None):
        """Restore the placeholder text if the search bar is empty."""
        if not self.search_entry.get().strip():
            self.search_entry.insert(0, "Search by title, author, or genre...")

    def update_book_list(self):
        """Update the TreeView with books from the library."""
        # Clear the current list
        for row in self.book_list.get_children():
            self.book_list.delete(row)

        # Populate the list with books
        books = self.controller.library.get_books()

        # Assuming books is a list of objects where each object has attributes title, author, etc.
        for book in books:
            self.book_list.insert(
                "", tk.END,
                values=(book.title, book.author, "yes" if book.is_loaned else "no", book.copies,
                        book.genre, book.year, book.available_copies, book.request_counter, ";".join(book.waitlist))
            )

    def search_books(self):
        """Search books by title, author, or genre."""
        query = self.search_entry.get().strip().lower()
        if not query or query == "search by title, author, or genre...":
            messagebox.showinfo("Search", "Please enter a search term.")
            return

        matching_books = [
            book
            for book in self.controller.library.get_books()  # Directly iterate over the list of Book objects
            if query in book.title.lower() or query in book.author.lower() or query in book.genre.lower()
        ]

        if not matching_books:
            messagebox.showinfo("Search", "No books found.")
        else:
            # Update the TreeView with matching books
            self.book_list.delete(*self.book_list.get_children())  # Clear existing rows
            for book in matching_books:
                self.book_list.insert(
                    "", tk.END,
                    values=(book.title, book.author, "yes" if book.is_loaned else "no", book.copies,
                            book.genre, book.year, book.available_copies, book.request_counter, ";".join(book.waitlist))
                )

    def add_book(self):
        """Add a new book via the controller."""
        title = simpledialog.askstring("Add Book", "Enter book title:")
        author = simpledialog.askstring("Add Book", "Enter book author:")
        genre = simpledialog.askstring("Add Book", "Enter book genre:")
        year = simpledialog.askinteger("Add Book", "Enter publication year:")
        copies = simpledialog.askinteger("Add Book", "Enter number of copies:")
        if not all([title, author, genre, year, copies]):
            messagebox.showerror("Error", "All fields must be filled!")
            return
        try:
            self.controller.add_book(title, author, copies, genre, year)
            self.update_book_list()
            messagebox.showinfo("Success", f"Book '{title}' added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_book(self):
        """Remove a selected book."""
        selected_item = self.book_list.focus()
        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            return
        values = self.book_list.item(selected_item, "values")
        try:
            self.controller.remove_book(values[0], values[1])
            self.update_book_list()
            messagebox.showinfo("Success", "Book removed successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def borrow_book(self):
        """Borrow a selected book or add the user to the waitlist if unavailable."""
        selected_item = self.book_list.focus()
        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            return

        # Get the selected book's title and author
        values = self.book_list.item(selected_item, "values")
        title, author = values[0], values[1]

        # Prompt for user information
        user_name = simpledialog.askstring("Borrow Book", "Enter your full name:")
        if not user_name:
            messagebox.showerror("Error", "Name is required to borrow a book.")
            return

        user_email = simpledialog.askstring("Borrow Book", "Enter your email (e.g., user@example.com):")
        if not user_email or "@" not in user_email:  # Basic email validation
            messagebox.showerror("Error", "A valid email address is required to borrow a book.")
            return

        user_phone = simpledialog.askstring("Borrow Book", "Enter your phone number:")
        if not user_phone or not user_phone.isnumeric():
            messagebox.showerror("Error", "A valid phone number is required to borrow a book.")
            return

        # Create a user dictionary to represent the borrower
        user = {"name": user_name, "email": user_email, "phone": user_phone}

        try:
            self.controller.borrow_book(title, author, user)  # Pass user info to the controller
            self.update_book_list()
            messagebox.showinfo("Success", f"'{user_name}' borrowed '{title}' successfully.")
        except ValueError as e:
            messagebox.showerror("Waitlist Information", str(e))

    def return_book(self):
        """Return a selected book."""
        selected_item = self.book_list.focus()
        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            return
        values = self.book_list.item(selected_item, "values")
        try:
            self.controller.return_book(values[0], values[1])
            self.update_book_list()
            messagebox.showinfo("Success", "Book returned successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_waitlist(self):
        """Display the waitlist for the selected book."""
        selected_item = self.book_list.focus()
        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            return

        # Retrieve the title and author of the selected book
        values = self.book_list.item(selected_item, "values")
        title, author = values[0], values[1]
        book_key = self.controller._generate_book_key(title, author)

        # Get the waitlist for the book
        waitlist = self.controller.stat_manager.get_waitlist(book_key)

        if not waitlist:
            messagebox.showinfo("Waitlist", f"No users are currently on the waitlist for '{title}' by '{author}'.")
        else:
            # Safely handle cases where some entries in the waitlist might not be dictionaries
            valid_entries = []
            for user in waitlist:
                if isinstance(user, dict) and {"name", "email", "phone"}.issubset(user.keys()):
                    valid_entries.append(f"{user['name']} - {user['email']} - {user['phone']}")
                else:
                    print(f"Invalid waitlist entry: {user}")  # Log bad entries for debugging

            if valid_entries:
                waitlist_str = "\n".join(valid_entries)
                messagebox.showinfo("Waitlist", f"Users on the waitlist for '{title}' by '{author}':\n\n{waitlist_str}")
            else:
                messagebox.showinfo("Waitlist", f"All waitlist entries for '{title}' by '{author}' are invalid.")

    def logout(self):
        """Logout the current librarian and return to the login screen."""
        self.root.destroy()
        self.__init__(self.controller)

    def run(self):
        """Run the main application loop."""
        self.root.mainloop()