from tkinter import ttk, simpledialog
from management import StatisticsManager
from management.SearchStrategy import *

class LibraryGUI:
    def __init__(self, controller):
        self.controller = controller
        self.stat_manager = StatisticsManager

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Library Management System")

        # Initialize GUI components
        self.book_list = None  # TreeView for book details
        self.search_entry = None

        # Display login screen initially
        self.librarian = None
        self.login_screen()

    def create_dashboard(self):
        """Create the main library dashboard after login."""
        self.create_widgets()
        self.create_action_buttons()

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

    def create_action_buttons(self):
        """Create action buttons for the main dashboard."""
        button_frame = tk.Frame(self.root, pady=10, padx=40)
        button_frame.pack(fill=tk.X)

        actions = [
            ("Add Book", self.add_book_screen),
            ("Remove Book", self.remove_book_screen),
            ("Search Book", self.search_screen),
            ("View Books", self.view_books_screen),
            ("Lend Book", self.lend_book_screen),
            ("Return Book", self.return_book_screen),
            ("Popular Books", self.display_popular_books),
            ("Logout", self.logout)
        ]

        for i, (text, command) in enumerate(actions):
            button = ttk.Button(button_frame, text=text, command=command)
            button.grid(row=0, column=i, padx=5, pady=5)

    def clear_all_books(self):
        """Clear the books display, including the TreeView and its data."""
        if hasattr(self, "book_list") and self.book_list:
            for row in self.book_list.get_children():
                self.book_list.delete(row)

            if self.book_list.master:
                self.book_list.master.destroy()

            self.book_list = None

    def create_book_list_table(self):
        """Set up the TreeView for displaying book data."""
        tree_frame = tk.Frame(self.root, pady=10, padx=10)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("title", "author", "is_loaned", "copies", "genre", "year", "available", "request_counter")
        self.book_list = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        for column in columns:
            self.book_list.heading(column, text=column.capitalize())

        self.book_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.book_list.yview)
        self.book_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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
                        book.genre, book.year, book.available, book.request_counter)
            )

    def all_books(self):
        self.create_book_list_table()
        self.update_book_list()

    def login_screen(self):
        """Create a login screen for librarian authentication."""
        login_frame = tk.Frame(self.root)
        login_frame.pack(expand=True)

        # Add a title to the login page
        title_label = tk.Label(
            login_frame,
            text="Welcome to Jesse & Lidor's Library",
            font=("Helvetica", 24, "bold"),
            fg="blue"
        )
        title_label.pack(pady=20)

        # Add login fields
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
                add_log("logged in successfully","info")
            except PermissionError as e:
                add_log("logged in fail", "info")
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
                add_log("registered fail", "info")
                return

            try:
                self.controller.register_librarian(username, librarian_id, password)
                messagebox.showinfo("Success", "Librarian registered successfully!")
                add_log("registered successfully", "info")
                register_frame.destroy()
                self.login_screen()
            except ValueError as e:
                error_label.config(text=str(e))

        tk.Button(register_frame, text="Register", command=on_register).pack(pady=10)
        tk.Button(register_frame, text="Back to Login",
                  command=lambda: [register_frame.destroy(), self.login_screen()]).pack(pady=5)

    # DONE
    def search_screen(self, event=None):
        """Create the search screen for finding books."""
        for widget in self.root.winfo_children():
            widget.destroy()
        search_frame = tk.Frame(self.root, pady=10, padx=10)
        search_frame.pack(fill=tk.X)

        tk.Label(search_frame, text="Search By:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        options = ["Search By Book Name", "Search By Author Name"]
        self.combo = ttk.Combobox(search_frame, values=options, state="readonly")
        self.combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.combo.set("Search By Book Name")

        def update_placeholder(event=None):
            selected_option = self.combo.get()
            if selected_option == "Search By Book Name":
                self.search_entry.delete(0, tk.END)
                self.search_entry.insert(0, "Enter book name...")
            elif selected_option == "Search By Author Name":
                self.search_entry.delete(0, tk.END)
                self.search_entry.insert(0, "Enter author name...")

        self.combo.bind("<<ComboboxSelected>>", update_placeholder)

        tk.Label(search_frame, text="Search Query:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = ttk.Entry(search_frame, width=50, font=("Arial", 12))
        self.search_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.search_entry.insert(0, "Enter book name...")

        def clear_placeholder(event=None):
            if self.search_entry.get() in ["Enter book name...", "Enter author name..."]:
                self.search_entry.delete(0, tk.END)

        self.search_entry.bind("<FocusIn>", clear_placeholder)

        search_button = ttk.Button(search_frame, text="Search", command=lambda: self.search_books(self.combo.get()))
        search_button.grid(row=1, column=2, padx=10, sticky="w")

        self.all_books()

        back_button = ttk.Button(search_frame, text="Back",
                                 command=lambda: [self.clear_all_books(), search_frame.destroy(),
                                                  self.create_dashboard()])
        back_button.grid(row=1, column=3, padx=10, sticky="w")

    # DONE
    def view_books_screen(self):
        """Create the search screen for finding books."""
        for widget in self.root.winfo_children():
            widget.destroy()

        view_books_frame = tk.Frame(self.root, pady=10, padx=10)
        view_books_frame.pack(fill=tk.BOTH, expand=True)

        # Filter selection
        tk.Label(view_books_frame, text="Filter By:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        options = ["All Books", "Available Books", "Borrowed Books", "Category"]
        self.combo = ttk.Combobox(view_books_frame, values=options, state="readonly")
        self.combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.combo.set("All Books")

        def get_all_categories():
            categories = []
            for book in self.controller.library.get_books():
                if book.genre not in categories:
                    categories.append(book.genre)
            return categories

        self.category_combo = ttk.Combobox(view_books_frame, values=get_all_categories(), state="readonly")
        self.category_combo.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.category_combo.set(f"{get_all_categories()[0]}")
        self.category_combo.grid_forget()

        # Function to update the books list based on selected filter
        def update_books_list(event=None):
            selected_filter = self.combo.get()
            if selected_filter == "Category":
                self.category_combo.grid(row=0, column=2, padx=5, pady=5, sticky="w")
                search = Search(SearchCategory())
                search.search(self.category_combo.get(), self.book_list, self.controller.library.get_books())
            else:
                self.category_combo.grid_forget()
                self.search_books(selected_filter)

        self.combo.bind("<<ComboboxSelected>>", update_books_list)
        self.category_combo.bind("<<ComboboxSelected>>", update_books_list)

        self.all_books()

        # Back button
        back_button = ttk.Button(view_books_frame, text="Back",
                                 command=lambda: [self.clear_all_books(), view_books_frame.destroy(),
                                                  self.create_dashboard()])
        back_button.grid(row=0, column=6, padx=10, sticky="w")

    # DONE
    def add_book_screen(self):
        """Display a screen to add a new book."""
        for widget in self.root.winfo_children():
            widget.destroy()

        add_book_frame = tk.Frame(self.root, pady=10, padx=10)
        add_book_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(add_book_frame, text="Add New Book", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Fields for book information
        fields = [("Title", "Enter book title..."),
                  ("Author", "Enter book author..."),
                  ("Genre", "Enter book genre..."),
                  ("Year", "Enter publication year..."),
                  ("Copies", "Enter number of copies...")]

        entries = {}
        initial_values = {}  # Dictionary to store initial values for comparison
        for label_text, placeholder in fields:
            field_frame = tk.Frame(add_book_frame)
            field_frame.pack(fill=tk.X, pady=5)

            tk.Label(field_frame, text=label_text, width=15, anchor="w").pack(side=tk.LEFT, padx=5)
            entry = ttk.Entry(field_frame)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            entry.insert(0, placeholder)
            entry.bind("<FocusIn>",
                       lambda e, ent=entry, ph=placeholder: ent.delete(0, tk.END) if ent.get() == ph else None)
            entries[label_text] = entry
            initial_values[label_text] = placeholder  # Store initial value

        # Error message label
        error_label = tk.Label(add_book_frame, text="", fg="red")
        error_label.pack(pady=10)

        # Submit button
        def on_submit():
            changed = 0
            for label, entry in entries.items():
                if entry.get().strip() != initial_values[label]:
                    changed += 1

            if changed != 5:
                error_label.config(text="All fields are required.")
                return

            title = entries["Title"].get().strip()
            author = entries["Author"].get().strip()
            genre = entries["Genre"].get().strip()
            try:
                year = int(entries["Year"].get().strip())
                copies = int(entries["Copies"].get().strip())
            except ValueError:
                error_label.config(text="Year and Copies must be valid integers.")
                add_log("book added fail", "info")
                return

            try:
                self.controller.add_book(title, author, copies, genre, year)
                messagebox.showinfo("Success", f"Book '{title}' added successfully.")
                add_log("book added successfully", "info")
                add_book_frame.destroy()
                self.create_dashboard()
            except Exception as e:
                error_label.config(text=str(e))

        # Buttons
        button_frame = tk.Frame(add_book_frame)
        button_frame.pack(fill=tk.X, pady=10)

        tk.Button(button_frame, text="Submit", command=on_submit).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Back", command=lambda: [add_book_frame.destroy(), self.create_dashboard()]).pack(
            side=tk.RIGHT, padx=10)

    # DONE
    def remove_book_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        remove_book_frame = tk.Frame(self.root, pady=10, padx=10)
        remove_book_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(remove_book_frame, text="Remove Book", font=("Helvetica", 16, "bold")).pack(pady=10)

        self.all_books()

        button_frame = tk.Frame(remove_book_frame)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        def remove():
            selected_item = self.book_list.focus()
            if not selected_item:
                messagebox.showerror("Error", "No book selected!")
                add_log("book removed fail", "info")
                return
            values = self.book_list.item(selected_item, "values")
            try:
                self.controller.remove_book(values[0], values[1])
                self.update_book_list()
                messagebox.showinfo("Success", "Book removed successfully.")
                add_log("book removed successfully", "info")
            except Exception as e:
                messagebox.showinfo("Error", str(e))

        tk.Button(button_frame, text="Remove", command=remove, width=10).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Back",
                  command=lambda: [self.clear_all_books(), remove_book_frame.destroy(), self.create_dashboard()],
                  width=10).pack(side=tk.RIGHT, padx=5)

    def lend_book_screen(self):
        """Borrow a selected book or add the user to the waitlist if unavailable."""
        for widget in self.root.winfo_children():
            widget.destroy()

        lend_book_frame = tk.Frame(self.root, pady=10, padx=10)
        lend_book_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(lend_book_frame, text="Lend Book", font=("Helvetica", 16, "bold")).pack(pady=10)

        self.all_books()

        button_frame = tk.Frame(lend_book_frame)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        def lend_book():
            # Check if a book is selected
            selected_item = self.book_list.focus()
            if not selected_item:
                messagebox.showerror("Error", "No book selected!")
                add_log("book borrowed fail", "info")
                return

            # Get the selected book's title and author
            values = self.book_list.item(selected_item, "values")
            title, author = values[0], values[1]

            # Create a popup for user information
            user_popup = tk.Toplevel(self.root)
            user_popup.title("User Information")
            user_popup.geometry("400x300")
            user_popup.grab_set()  # Prevent interaction with the main window

            tk.Label(user_popup, text="Enter User Information", font=("Helvetica", 14, "bold")).pack(pady=10)

            # Fields for user information
            fields = [("Full Name", "Enter your full name..."),
                      ("Email", "Enter your email (e.g., user@example.com)..."),
                      ("Phone Number", "Enter your phone number...")]

            entries = {}
            for label_text, placeholder in fields:
                field_frame = tk.Frame(user_popup)
                field_frame.pack(fill=tk.X, pady=5)

                tk.Label(field_frame, text=label_text, width=15, anchor="w").pack(side=tk.LEFT, padx=5)
                entry = ttk.Entry(field_frame)
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
                entry.insert(0, placeholder)
                entry.bind("<FocusIn>",
                           lambda e, ent=entry, ph=placeholder: ent.delete(0, tk.END) if ent.get() == ph else None)
                entries[label_text] = entry

            error_label = tk.Label(user_popup, text="", fg="red")
            error_label.pack(pady=5)

            def submit_user_info():
                user_name = entries["Full Name"].get().strip()
                user_email = entries["Email"].get().strip()
                user_phone = entries["Phone Number"].get().strip()

                if not user_name or user_name == "Enter your full name...":
                    error_label.config(text="Name is required to borrow a book.")
                    return

                if not user_email or "@" not in user_email or user_email == "Enter your email (e.g., user@example.com)...":
                    error_label.config(text="A valid email address is required to borrow a book.")
                    return

                if not user_phone or not user_phone.isnumeric() or user_phone == "Enter your phone number...":
                    error_label.config(text="A valid phone number is required to borrow a book.")
                    return

                # Create a user dictionary to represent the borrower
                user = {"name": user_name, "email": user_email, "phone": user_phone}

                try:
                    if self.controller.borrow_book(title, author, user) : # Pass user info to the controller
                        messagebox.showinfo("Success", f"'{user_name}' borrowed '{title}' successfully.")
                        add_log("book borrowed successfully", "info")
                    else:
                        messagebox.showinfo("Failed",f"Book '{title}' is unavailable. {user['name']} added to the waitlist.")
                        add_log("book borrowed fail", "info")
                    self.update_book_list()
                    user_popup.destroy()
                except ValueError as e:
                    error_label.config(text=str(e))

            tk.Button(user_popup, text="Submit", command=submit_user_info).pack(pady=10)
            tk.Button(user_popup, text="Cancel", command=user_popup.destroy).pack()

        tk.Button(button_frame, text="Lend", command=lend_book, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back",
                  command=lambda: [self.clear_all_books(), lend_book_frame.destroy(), self.create_dashboard()],
                  width=10).pack(side=tk.RIGHT, padx=5)

    def return_book_screen(self):
        """Return a selected book."""
        for widget in self.root.winfo_children():
            widget.destroy()

        return_book_frame = tk.Frame(self.root, pady=10, padx=10)
        return_book_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(return_book_frame, text="Return Book", font=("Helvetica", 16, "bold")).pack(pady=10)

        self.all_books()

        button_frame = tk.Frame(return_book_frame)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        def return_book():
            selected_item = self.book_list.focus()
            if not selected_item:
                messagebox.showerror("Error", "No book selected!")
                add_log("book returned fail", "info")
                return
            values = self.book_list.item(selected_item, "values")
            try:
                self.controller.return_book(values[0], values[1])
                self.update_book_list()
                messagebox.showinfo("Success", "Book returned successfully.")
                add_log("book returned successfully", "info")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(button_frame, text="Return", command=return_book, width=10).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Back",
                  command=lambda: [self.clear_all_books(), return_book_frame.destroy(), self.create_dashboard()],
                  width=10).pack(side=tk.RIGHT, padx=5)

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

    def display_popular_books(self):
        """Display popular books sorted by request count."""
        popular_books = self.controller.get_popular_books()
        self.display_books_popup("Popular Books", popular_books, "Popular Books")
        add_log("displayed successfully", "info")

    def display_available_books(self):
        """Display books with available copies."""
        available_books = self.controller.get_available_books()
        self.display_books_popup("Available Books", available_books, "Available Books")

    def display_books_popup(self, title, books, case):
        """Show a list of books in a popup window with dynamic columns based on the case."""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("800x400")

        # Define columns based on the case
        if case == "Popular Books":
            columns = ("Title", "Author", "Copies", "Genre", "Year", "Available", "Request Counter")
            data_rows = [
                (book.title, book.author, book.copies, book.genre, book.year, book.available, book.request_counter)
                for book in books
            ]
        elif case == "Available Books":
            columns = ("Title", "Author", "Copies", "Genre", "Year", "Available")
            data_rows = [
                (book.title, book.author, book.copies, book.genre, book.year, book.available)
                for book in books
            ]
        else:
            raise ValueError("Unknown case provided.")

        # Create TreeView for dynamic columns
        book_list = ttk.Treeview(popup, columns=columns, show='headings')

        for column in columns:
            book_list.heading(column, text=column)

        # Insert the data rows into the TreeView
        for row in data_rows:
            book_list.insert("", tk.END, values=row)

        book_list.pack(fill=tk.BOTH, expand=True)

        # Scrollbar configuration
        scrollbar = ttk.Scrollbar(popup, orient=tk.VERTICAL, command=book_list.yview)
        book_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def search_books(self, strategy):
        if strategy == "Search By Book Name":
            search = Search(SearchBookName())
            search.search(self.search_entry.get().strip().lower(), self.book_list, self.controller.library.get_books())
        elif strategy == "Search By Author Name":
            search = Search(SearchAuthorName())
            search.search(self.search_entry.get().strip().lower(), self.book_list, self.controller.library.get_books())
        elif strategy == "All Books":
            search = Search(SearchAllBooks())
            search.search("All Books", self.book_list, self.controller.library.get_books())
        elif strategy == "Available Books":
            search = Search(SearchAvailableBooks())
            search.search("available", self.book_list, self.controller.library.get_books())
        elif strategy == "Borrowed Books":
            search = Search(SearchBorrowedBooks())
            search.search("is_loaned", self.book_list, self.controller.library.get_books())

    def logout(self):
        """Logout the current librarian and return to the login screen."""
        add_log("log out successful", "info")
        self.root.destroy()
        self.__init__(self.controller)

    def run(self):
        """Run the main application loop."""
        self.root.mainloop()
