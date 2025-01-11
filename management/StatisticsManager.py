from collections import defaultdict


class StatisticsManager:
    def __init__(self):
        self.request_count = defaultdict(int)

    @staticmethod
    def generate_key(title, author):
        """Generates a normalized key for a book based on its title and author."""
        if not title or not author:
            raise ValueError("Both title and author are required to generate a key.")
        return f"{title.strip()}|{author.strip()}"

    def update_request_count(self, book_key):
        """Increment the borrow request count for a book."""
        self.request_count[book_key] += 1

    def get_request_count(self, book_key):
        """Retrieve the request count for a specific book."""
        return self.request_count.get(book_key, 0)

    def load_statistics(self, request_data):
        """Load request data from an external source."""
        self.request_count.update(request_data)

    def export_statistics(self):
        """Export the current request counts for saving."""
        return dict(self.request_count)
