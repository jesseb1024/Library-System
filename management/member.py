class Member:
    def __init__(self, name, member_id):
        """
        Initialize a member with their details.
        :param name: Name of the member.
        :param member_id: Unique membership ID.
        """
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []  # Stores a list of borrowed books (by book ID)

    def borrow_book(self, book):
        """
        Adds a borrowed book to the member's list.
        :param book: The book object being borrowed.
        """
        self.borrowed_books.append(book.book_id)

    def return_book(self, book):
        """
        Removes a returned book from the member's list.
        :param book: The book object being returned.
        """
        if book.book_id in self.borrowed_books:
            self.borrowed_books.remove(book.book_id)

    def __str__(self):
        """
        Returns a user-friendly string representation of the member.
        """
        return f"Member ID: {self.member_id}, Name: {self.name}, Borrowed: {self.borrowed_books}"
