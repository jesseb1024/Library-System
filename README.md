# Library Management System

## Project Overview

This document provides an overview of the Library Management System (LMS), including instructions for running the project, a description of the system features, and the design patterns implemented to enhance the functionality and scalability of the system.

---

## Instructions for Running the Project

1. **Navigate to the Files Directory**  
   Go to the directory where the project files are located.

2. **Run the Main Program**  
   Execute the main program to start the system.

3. **Register as a Librarian**  
   - Ensure that you use your ID during the registration process to avoid any issues with account approval.
   - You will need to use the encrypted password storage for security purposes.

4. **Explore the GUI**  
   Once registered, you can start managing the library through the Graphical User Interface (GUI), where you can perform the following tasks:
   - **Add Books**: Add new books to the library catalog.
   - **Remove Books**: Remove outdated or unnecessary books from the library.
   - **Manage Library Operations**: Perform other administrative tasks for efficient library management.

---

## System Features

### 1. **Librarian Management**  
   - Enables librarian registration.
   - Passwords are securely stored using encryption to ensure user data protection.

### 2. **Book Waitlist Notifications**  
   - Allows librarians to manage waitlists for popular books.
   - Automatically notifies users when a book they are waiting for becomes available.

### 3. **Internal-Only System**  
   - Designed solely for internal use by librarians, which means there is no direct interaction with customers through the system interface.

---

## Design Patterns Implemented

### 1. **Observer Pattern**  
   - **Purpose**: Used for the waitlist notification system. When a book becomes available, all users on the waitlist are automatically notified.
   - **Implemented in**: `StatisticsManager`

### 2. **Decorator Pattern**  
   - **Purpose**: Enhances search functionalities by allowing flexible and extensible search methods.
   - **Implemented in**: `SearchStrategy` 

### 3. **Iterator Pattern**  
   - **Purpose**: Simplifies iteration over observer lists and ensures efficient handling of notifications.
   - **Implemented in**: `StatisticsManager`

### 4. **Strategy Pattern**  
   - **Purpose**: Provides multiple search strategies to meet different librarian needs, allowing them to choose the most appropriate method.
   - **Implemented in**: `SearchStrategy` 

---

## Additional Notes

- You can see all your actions in the log file. I would also appreciate it if you tried to return a book whose number of copies is not available. Then you will be able to see messages informing librarians about the book you returned and that they should update the user.
---

**Enjoy managing your library with ease!**