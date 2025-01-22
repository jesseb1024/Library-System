from management.StatisticsManager import StatisticsManager
from management.LibraryController import LibraryController
from management.library import Library
from users.librarian import LibrarianManager
from management.gui import LibraryGUI
import logging
import os


# Initialize system components
def main():
    logging.info("Initializing Library System...")

    # File paths
    books_file_path = "files/books.csv"
    statistics_file = "../statistics.csv"
    librarian_file = "librarians.csv"
    log_file_path = os.path.abspath("../library_log.txt")

    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    logging.basicConfig(
        filename=log_file_path,
        level=logging.DEBUG,  # Change to INFO or WARNING in production
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Logging setup complete. Application starting.")

    # Initialize components
    library = Library(books_file_path)  # Manage books
    statistics_manager = StatisticsManager()  # Manage waitlists and request counts
    librarian_manager = LibrarianManager(librarian_file)  # Manage librarians

    # Load books into the library from CSV
    library.load_books_from_file()
    logging.info("Books loaded successfully from file.")


    # Create the controller and GUI
    controller = LibraryController(library, statistics_manager, file_path=books_file_path)
    gui = LibraryGUI(controller)

    # Run the GUI
    logging.info("Starting the Library Management GUI...")
    gui.run()


if __name__ == "__main__":
    main()
