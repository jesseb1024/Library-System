from management.library import Library
from management.gui import LibraryGUI

if __name__ == "__main__":
    # Initialize the Library system
    library_system = Library()

    # Load books from CSV if available
    try:
        library_system.load_books_from_csv()
    except Exception as e:
        print(f"An error occurred while loading the library: {e}")
        print("Starting fresh...")

    # Run the GUI
    gui = LibraryGUI(library_system)
    gui.run()