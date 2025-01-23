import csv
import os


class MyIterator:
    def __init__(self, collection):
        self.collection = collection
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.collection.items):
            item = self.collection.items[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration

class StatisticsManager:
    observers = []
    def __init__(self, storage_file=os.path.abspath("../files/statistics.csv")):
        """Initialize the StatisticsManager with CSV-based persistence."""
        self.storage_file = storage_file
        self.waiting_list = {}  # In-memory dictionary for waitlists
        self.request_counts = {}  # In-memory dictionary for request counts

        # Load data from the CSV file at initialization
        self.load_data()

    def register_observer(self, observer):
        StatisticsManager.observers.append(observer)

    def notify_observers(self,user_name, book_key):
        for observer in StatisticsManager.observers:
            observer.update(observer,user_name,book_key)

    def add_user_to_waitlist(self, book_key, user):
        """Add a user to the waitlist for a specific book."""
        if book_key not in self.waiting_list:
            self.waiting_list[book_key] = []
        if user not in self.waiting_list[book_key]:
            self.waiting_list[book_key].append(user)
        self.save_data()  # Save after modification

    def get_waitlist(self, book_key):
        """Retrieve the waiting list for a specific book."""
        return self.waiting_list.get(book_key, [])

    def get_waitlist_count(self):
        return len(self.waiting_list)

    def get_request_count(self, book_key):
        """Retrieve the request count for a specific book."""
        return self.request_counts.get(book_key, 0)

    def notify_waitlist(self, book_key,book_name):
        """Notify the next user on the waitlist when a book becomes available."""
        user = self.waiting_list[book_key].pop(0)
        self.notify_observers(user,book_name)
        self.save_data()

    def save_data(self):
        """Save the waiting list and request counts to a CSV file."""
        with open(self.storage_file, mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # Write the header
            writer.writerow(["title:author", "request_count", "waitlist"])
            # Write data rows: Combine title-author as the key
            for book_key, waitlist in self.waiting_list.items():
                waitlist_str = ";".join([f"{u['name']},{u['email']},{u['phone']}" for u in waitlist])
                request_count = self.request_counts.get(book_key, 0)
                writer.writerow([book_key, request_count, waitlist_str])

    def load_data(self):
        """Load the waiting list and request counts from a CSV file."""
        if not os.path.exists(self.storage_file):
            return

        with open(self.storage_file, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                book_key = row["title:author"]
                self.request_counts[book_key] = int(row["request_count"])
                # Parse the waitlist (semicolon-separated)
                waitlist_str = row["waitlist"]
                if waitlist_str:
                    self.waiting_list[book_key] = [
                        dict(zip(["name", "email", "phone"], user.split(",")))
                        for user in waitlist_str.split(";")
                    ]
                else:
                    self.waiting_list[book_key] = []

    @staticmethod
    def generate_key(title, author):
        """Generate a unique book key based on title and author."""
        return f"{title.lower()}:{author.lower()}"

    def __iter__(self):
        return MyIterator(StatisticsManager.observers)
