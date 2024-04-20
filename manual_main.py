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

        # use menubar as the menu
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

    def create_key(self):
        """Generate a new key"""
        self.key = Fernet.generate_key()

    def encrypt_text(self):
        """Encrypt the text in the text widget"""
        if self.key is None:
            self.create_key()
        fernet = Fernet(self.key)
        text_to_encrypt = self.text.get(1.0, tk.END).encode()
        encrypted_text = fernet.encrypt(text_to_encrypt).decode()
        self.text.delete(1.0, tk.END)
        self.text.insert(1.0, encrypted_text)

    def decrypt_text(self):
        """Decrypt the text in the text widget"""
        try:
            fernet = Fernet(self.key)
            text_to_decrypt = self.text.get(1.0, tk.END).encode()
            decrypted_text = fernet.decrypt(text_to_decrypt).decode()
            self.text.delete(1.0, tk.END)
            self.text.insert(1.0, decrypted_text)
        except:
            messagebox.showerror(
                "Decryption Error", "Failed to decrypt! Check your key and try again."
            )
            return False
        return True

    def new_file(self):
        """Clear the text widget and reset the key"""
        self.text.delete(1.0, tk.END)
        self.key = None

    def open_file(self):
        """Open a file and display its content in the text widget"""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.text.delete(1.0, tk.END)
                    self.text.insert(1.0, file.read())
            except Exception as e:
                messagebox.showerror("Error", "Failed to read file: " + str(e))
                return

            key = simpledialog.askstring("Encryption Key", "Enter the encryption key:")
            if key:
                self.key = key.encode()
                if not self.decrypt_text():
                    self.new_file()
                # messagebox.showinfo("Decrypted", "File decrypted successfully.")
            else:
                messagebox.showinfo(
                    "Cancelled", "Operation cancelled! File is not decrypted."
                )

    def save_file(self):
        """Save the text to a file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            try:
                self.encrypt_text()
                with open(file_path, "w") as file:
                    file.write(self.text.get(1.0, tk.END))
                self.show_key_dialog(self.key.decode())
            except Exception as e:
                messagebox.showerror("Error", "Failed to save file: " + str(e))

    def show_key_dialog(self, key):
        """Show a dialog with the encryption key"""
        dialog = tk.Toplevel(self)
        dialog.title("Encryption Key")
        tk.Label(dialog, text="Copy your encryption key:").pack(pady=5)
        tk.Label(dialog, text=key).pack(pady=5)
        tk.Button(
            dialog,
            text="Copy to Clipboard",
            command=lambda: self.copy_to_clipboard(key),
        ).pack(pady=5)
        tk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=5)

    def copy_to_clipboard(self, key):
        """Copy the key to clipboard when the button is clicked"""
        self.clipboard_clear()
        self.clipboard_append(key)
        # messagebox.showinfo("Copied", "Key copied to clipboard!")

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
