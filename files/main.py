from Library_Controls.StatisticsManager import StatisticsManager
from Library_Controls.LibraryController import LibraryController
from Library_Controls.library import Library
from users.librarian import LibrarianManager
from Library_Controls.gui import LibraryGUI
import logging
logging.basicConfig(
    filename="library_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    filemode="w",
)

# Initialize system components
def main():
    logging.info("Initializing Library System...")

    # File paths
    books_file_path = "files/books.csv"
    statistics_file = "statistics.csv"
    librarian_file = "librarians.csv"



    # Initialize components
    library = Library(books_file_path)  # Manage books
    statistics_manager = StatisticsManager(statistics_file)  # Manage waitlists and request counts
    librarian_manager = LibrarianManager(librarian_file)  # Manage librarians

    # Load books into the library from CSV
    library.load_books_from_file()
    logging.info("Books loaded successfully from file.")


    # Create the controller and GUI
    controller = LibraryController(library, statistics_manager, librarian_manager)
    gui = LibraryGUI(controller)

    # Run the GUI
    logging.info("Starting the Library Management GUI...")
    gui.run()


if __name__ == "__main__":
    main()
