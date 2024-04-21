import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from cryptography.fernet import Fernet


class SecuredTextEditor(tk.Tk):

    def __init__(self):
        """Initialize the application"""
        super().__init__()
        self.title("Secured Text Editor")
        self.geometry("800x600")
        self.key = None
        self.text = tk.Text(self, font=("Courier New", 12))
        self.text.pack(fill=tk.BOTH, expand=True)
        # self.iconbitmap('icon.ico')
        self.create_menu()
        self.bind_shortcuts()
        # Load or generate the encryption key when the application starts
        self.load_or_generate_key()

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

    def load_or_generate_key(self):
        """Load the encryption key from a file or generate a new key if the file doesn't exist"""
        try:
            with open("encryption_key.txt", "rb") as key_file:
                self.encryption_key = key_file.read()
        except FileNotFoundError:
            self.encryption_key = Fernet.generate_key()
            with open("encryption_key.txt", "wb") as key_file:
                key_file.write(self.encryption_key)

        self.fernet = Fernet(self.encryption_key)

    def new_file(self):
        """Clear the text widget and reset the key"""
        self.text.delete(1.0, tk.END)

    def open_file(self):
        """Open a file and display its content in the text widget"""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "rb") as file:
                encrypted_data = file.read()
            try:
                decrypted_data = self.fernet.decrypt(encrypted_data).decode()
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, decrypted_data)
            except Exception as e:
                messagebox.showerror("Error", "Failed to open file: " + str(e))

    def save_file(self):
        text_data = self.text.get(1.0, tk.END)
        encrypted_data = self.fernet.encrypt(text_data.encode())
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt")]
        )
        if file_path:
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
