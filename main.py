import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import base64

# Import the necessary modules

class SecuredTextEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Secured Text Editor")
        self.geometry("800x600")
        self.key = None  # Initialize the encryption key to None
        self.text_area = tk.Text(self, font=("Courier", 12))
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu_bar)

    def new_file(self):
        self.text_area.delete("1.0", tk.END)  # Clear the text area
        self.key = None  # Reset the encryption key

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt")
        if file_path:
            try:
                with open(file_path, "r") as file:
                    encrypted_data = file.read()  # Read the encrypted data from the file
                self.text_area.delete("1.0", tk.END)  # Clear the text area
                decrypted_data = self.decrypt_data(encrypted_data)  # Decrypt the data
                self.text_area.insert("1.0", decrypted_data)  # Insert the decrypted data into the text area
            except Exception as e:
                messagebox.showerror("Error", str(e))  # Show an error message if an exception occurs

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            try:
                text_content = self.text_area.get("1.0", tk.END)  # Get the text content from the text area
                encrypted_data = self.encrypt_data(text_content)  # Encrypt the text content
                with open(file_path, "w") as file:
                    file.write(encrypted_data)  # Write the encrypted data to the file
            except Exception as e:
                messagebox.showerror("Error", str(e))  # Show an error message if an exception occurs

    def encrypt_data(self, data):
        if not self.key:
            self.key = Fernet.generate_key()  # Generate a new encryption key if it doesn't exist
        fernet = Fernet(self.key)
        encrypted_data = fernet.encrypt(data.encode())  # Encrypt the data
        return base64.urlsafe_b64encode(encrypted_data).decode()  # Encode the encrypted data using base64

    def decrypt_data(self, encrypted_data):
        if not self.key:
            return ""  # Return an empty string if there is no encryption key
        fernet = Fernet(self.key)
        encrypted_data = base64.urlsafe_b64decode(encrypted_data.encode())  # Decode the base64-encoded data
        decrypted_data = fernet.decrypt(encrypted_data)  # Decrypt the data
        return decrypted_data.decode()  # Decode the decrypted data to a string

if __name__ == "__main__":
    app = SecuredTextEditor()
    app.mainloop()