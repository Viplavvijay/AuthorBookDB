
import tkinter as tk
import mysql.connector
from tkinter import messagebox

# Connect to a MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="VIPLAV",
    password="your",
    database="world"
)
cursor = conn.cursor()

# Create a table to store book information
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_name VARCHAR(255),
    author_name VARCHAR(255)
)
''')
conn.commit()

# Merge Sort Algorithm
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    return merge(left_half, right_half)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][1].lower() < right[j][1].lower():
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Other functions
def add_book():
    book = book_entry.get().strip()
    author = author_entry.get().strip()

    if book and author:
        cursor.execute('INSERT INTO books (book_name, author_name) VALUES (%s, %s)', (book, author))
        conn.commit()
        book_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        view_library()
        messagebox.showinfo("Library", "Book added successfully!")
    else:
        messagebox.showerror("Error", "Both Book name and Author name must be filled!")

def delete_book():
    index = delete_entry.get().strip()
    if index.isdigit():
        index = int(index)
        cursor.execute('SELECT id FROM books LIMIT 1 OFFSET %s', (index - 1,))
        data = cursor.fetchone()
        if data:
            book_id = data[0]
            cursor.execute('DELETE FROM books WHERE id = %s', (book_id,))
            conn.commit()
            view_library()
            delete_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid index!")
    else:
        messagebox.showerror("Error", "Invalid index!")

def view_library():
    cursor.execute('SELECT book_name, author_name FROM books')
    data = cursor.fetchall()
    if not data:
        messagebox.showinfo("Library", "The list is empty")
    else:
        books_info = ""
        for index, book in enumerate(data, start=1):
            books_info += f"{index}. The name of the Book: {book[0]}\n    The author of the book: {book[1]}\n\n"
        messagebox.showinfo("Current Books", books_info)

def exit_library():
    conn.close()
    root.destroy()

# Create the main window and run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Library Management System")

    # Set the background color and padding
    root.configure(bg="#f0f0f0")
    root.geometry("400x400")

    # Create a custom font
    custom_font = ("Arial", 12)

    # Create labels and entry fields
    book_label = tk.Label(root, text="Book Name:", font=custom_font, bg="#f0f0f0")
    book_label.pack(pady=10)

    book_entry = tk.Entry(root, font=custom_font)
    book_entry.pack(pady=5)

    author_label = tk.Label(root, text="Author Name:", font=custom_font, bg="#f0f0f0")
    author_label.pack(pady=10)

    author_entry = tk.Entry(root, font=custom_font)
    author_entry.pack(pady=5)

    # Create buttons with colors and padding
    add_button = tk.Button(root, text="Add Book", font=custom_font, bg="#4CAF50", fg="white", command=add_book)
    add_button.pack(pady=10)

    view_button = tk.Button(root, text="View Library", font=custom_font, bg="#008CBA", fg="white", command=view_library)
    view_button.pack(pady=5)

    delete_label = tk.Label(root, text="Enter index to delete:", font=custom_font, bg="#f0f0f0")
    delete_label.pack(pady=10)

    delete_entry = tk.Entry(root, font=custom_font)
    delete_entry.pack(pady=5)

    delete_button = tk.Button(root, text="Delete Book", font=custom_font, bg="#f44336", fg="white", command=delete_book)
    delete_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", font=custom_font, bg="#555", fg="white", command=exit_library)
    exit_button.pack(pady=10)

    root.mainloop()
