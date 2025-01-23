from management.StatisticsManager import StatisticsManager
from management.LibraryController import LibraryController
from management.library import Library
from users.librarian import LibrarianManager
from management.gui import LibraryGUI
import logging
import os
from files.Log import add_log


# Initialize system components
def main():
    add_log("Initializing Library System...","info")

    # File paths
    books_file_path = os.path.abspath("../files/books.csv")
    statistics_file = os.path.abspath("../files/statistics.csv")
    librarian_file = os.path.abspath("../files/librarian.csv")
    log_file_path = os.path.abspath("../library_log.txt")

    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    logging.basicConfig(
        filename=log_file_path,
        level=logging.DEBUG,  # Change to INFO or WARNING in production
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    add_log("Logging setup complete. Application starting.","info")

    # Initialize components
    library = Library(books_file_path)  # Manage books
    statistics_manager = StatisticsManager()  # Manage waitlists and request counts
    librarian_manager = LibrarianManager(librarian_file)  # Manage librarians

    # Load books into the library from CSV
    library.load_books_from_file()
    add_log("Books loaded successfully from file.", "info")


    # Create the controller and GUI
    controller = LibraryController(library, statistics_manager, file_path=books_file_path)
    gui = LibraryGUI(controller)

    # Run the GUI
    add_log("Starting the Library Management GUI...", "info")
    gui.run()


if __name__ == "__main__":
    main()
