from management.library import Library
from management.LibraryController import LibraryController
from management.gui import LibraryGUI
import os

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "management/data/books.csv")
    library_system = Library(file_path=file_path)

    # Load books from CSV
    try:
        library_system.load_books()
    except Exception as e:
        print(f"An error occurred while loading the library: {e}")
        print("Starting fresh...")

    # Initialize the LibraryController
    library_controller = LibraryController(library_system)

    # Run the GUI with the LibraryController
    gui = LibraryGUI(library_controller)
    gui.run()