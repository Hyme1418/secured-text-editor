import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from cryptography.fernet import Fernet
import json


class SecuredTextEditor(tk.Tk):
    def __init__(self):
        """Initialize the application"""
        super().__init__()
        self.title("Secured Text Editor")
        self.geometry("800x600")
        self.text = tk.Text(self, font=("Courier New", 12))
        self.text.pack(fill=tk.BOTH, expand=True)
        self.create_menu()
        self.bind_shortcuts()

        self.key_file = "keys.json"
        self.filename_to_key = {}
        self.load_keys()

    def create_menu(self):
        """Create a menu with file operations"""
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=False)
        # add file menu
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # add about us menu
        aboutus_menu = tk.Menu(menubar, tearoff=False)
        aboutus_menu.add_command(label="About us", command=self.show_aboutus_popup)

        # add help menu
        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="Help", command=self.show_help_popup)

        # add cascade menu
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="About us", menu=aboutus_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

        # set config to use this menubar
        self.config(menu=menubar)

    def show_help_popup(self):
        """Show a popup with information about the application"""
        about_text = """This is a secured text editor application that allows you to encrypt and decrypt text data."""
        messagebox.showinfo("Help", about_text)

    def show_aboutus_popup(self):
        """Show a popup with information about the team members"""
        about_text = (
            "Team members\n\n"
            "Sirasit Puangpathanachai 6488133\n"
            "Thanawat Jarusuthirug 6488178\n"
        )
        messagebox.showinfo("About us", about_text)

    def load_keys(self):
        """Load filename-key pairs from the JSON file."""
        try:
            with open(self.key_file, "r") as f:
                self.filename_to_key = json.load(f)
        except FileNotFoundError:
            pass  # Ignore if the file doesn't exist yet

    def save_keys(self):
        """Save filename-key pairs to the JSON file."""
        with open(self.key_file, "w") as f:
            json.dump(self.filename_to_key, f, indent=4)

    def generate_key_for_file(self, filename):
        """Generates a new key for a given filename and stores it."""
        key = Fernet.generate_key()
        self.filename_to_key[filename] = key.decode()  # Store as string
        self.save_keys()
        return key

    def get_key_for_file(self, filename):
        """Retrieves the key associated with a filename."""
        if filename in self.filename_to_key:
            return self.filename_to_key[filename].encode()  # Convert back to bytes
        else:
            return None  # No key found for this file

    def new_file(self):
        """Clear the text widget."""
        self.text.delete(1.0, tk.END)

    def open_file(self):
        """Open a file, retrieve its key, and decrypt the content."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            key = self.get_key_for_file(file_path)
            if key:
                fernet = Fernet(key)
                with open(file_path, "rb") as file:
                    encrypted_data = file.read()
                try:
                    decrypted_data = fernet.decrypt(encrypted_data).decode()
                    self.text.delete(1.0, tk.END)
                    self.text.insert(tk.END, decrypted_data)
                except Exception as e:
                    messagebox.showerror("Error", "Failed to open file: " + str(e))
            else:
                messagebox.showerror("Error", "No key found for this file.")

    def save_file(self):
        """Encrypt the text content using the associated key and save the file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            key = self.get_key_for_file(file_path)
            if not key:  # Generate a new key if none exists
                key = self.generate_key_for_file(file_path)
            fernet = Fernet(key)
            text_data = self.text.get(1.0, tk.END)
            encrypted_data = fernet.encrypt(text_data.encode())
            with open(file_path, "wb") as file:
                file.write(encrypted_data)

    def bind_shortcuts(self):
        """Bind keyboard shortcuts to functions"""

        # Ctrl+s to save file
        self.bind("<Control-s>", lambda event: self.save_file())
        # Ctrl+o to open file
        self.bind("<Control-o>", lambda event: self.open_file())
        # Ctrl+n to create new file
        self.bind("<Control-n>", lambda event: self.new_file())


if __name__ == "__main__":
    app = SecuredTextEditor()
    app.mainloop()
