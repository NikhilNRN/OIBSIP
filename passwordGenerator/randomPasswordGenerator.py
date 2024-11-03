import random
import string
import tkinter as tk
from tkinter import messagebox

def generate_password(length, use_letters, use_numbers, use_symbols):
    # Define possible characters based on user preferences
    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    # Check if any character set is selected
    if not characters:
        messagebox.showerror("Error", "Please select at least one character set.")
        return ""

    # Generate random password
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def generate():
    try:
        length = int(length_entry.get())
        use_letters = letters_var.get()
        use_numbers = numbers_var.get()
        use_symbols = symbols_var.get()

        password = generate_password(length, use_letters, use_numbers, use_symbols)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid length.")


def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(password_entry.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")


# Set up GUI
root = tk.Tk()
root.title("Password Generator")

tk.Label(root, text="Password Length:").grid(row=0, column=0, sticky="w")
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, pady=5)

letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Letters", variable=letters_var).grid(row=1, column=0, sticky="w")
tk.Checkbutton(root, text="Include Numbers", variable=numbers_var).grid(row=1, column=1, sticky="w")
tk.Checkbutton(root, text="Include Symbols", variable=symbols_var).grid(row=1, column=2, sticky="w")

tk.Button(root, text="Generate Password", command=generate).grid(row=2, column=0, columnspan=3, pady=10)

password_entry = tk.Entry(root, width=40)
password_entry.grid(row=3, column=0, columnspan=2, pady=5)

tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).grid(row=3, column=2)

root.mainloop()
