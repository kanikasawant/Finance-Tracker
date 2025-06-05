import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import bcrypt

# Function to hash passwords
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

# Function to authenticate user
def authenticate_user(username, password):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return bcrypt.checkpw(password.encode(), result[0].encode())
    return False  

# Function to register user
def register_user(username, password):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE, 
            password TEXT
        )
    """)

    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    conn.close()

# Styled Login Page
class LoginPage:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success  # ✅ Fix: Store the function
        self.root.title("Personal Finance - Login")
        self.root.geometry("500x550")  
        self.root.configure(bg="#0A192F")  

        self.on_success = on_success  

        login_label = tk.Label(root, text="BudgetMate", font=("Montserrat", 40, "bold"), fg="white", bg="#0A192F")
        login_label.pack(pady=30)

        frame = tk.Frame(root, bg="#0A192F", padx=20, pady=20)
        frame.pack(pady=20)
        frame.configure(relief="raised", bd=5)

        inner_frame = tk.Frame(frame, bg="#1976D2", padx=30, pady=30)
        inner_frame.pack()

        ttk.Label(inner_frame, text="Username:", font=("Arial", 14), background="#1976D2", foreground="white").pack(pady=5)
        self.username_entry = ttk.Entry(inner_frame, font=("Arial", 14), width=25)
        self.username_entry.pack(pady=5)

        ttk.Label(inner_frame, text="Password:", font=("Arial", 14), background="#1976D2", foreground="white").pack(pady=5)
        self.password_entry = ttk.Entry(inner_frame, font=("Arial", 14), width=25, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(inner_frame, text="Login", command=self.check_login, style="TButton")
        self.login_button.pack(pady=10)

        self.register_button = ttk.Button(inner_frame, text="Register", command=self.show_register_window, style="TButton")
        self.register_button.pack(pady=10)

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 14, "bold"), padding=10, background="#FFFFFF", foreground="black")

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if authenticate_user(username, password):
            messagebox.showinfo("Login Success", "Welcome!")
            self.root.withdraw()  
            self.on_success(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_register_window(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Register")
        register_window.geometry("500x550")  
        register_window.configure(bg="#0A192F")  

        reg_label = tk.Label(register_window, text="BudgetMate", font=("Montserrat", 40, "bold"), fg="white", bg="#0A192F")
        reg_label.pack(pady=30)

        frame = tk.Frame(register_window, bg="#0A192F", padx=20, pady=20)
        frame.pack(pady=20)
        frame.configure(relief="raised", bd=5)

        inner_frame = tk.Frame(frame, bg="#1976D2", padx=30, pady=30)
        inner_frame.pack()

        ttk.Label(inner_frame, text="Username:", font=("Arial", 14), background="#1976D2", foreground="white").pack(pady=5)
        username_entry = ttk.Entry(inner_frame, font=("Arial", 14), width=25)
        username_entry.pack(pady=5)

        ttk.Label(inner_frame, text="Password:", font=("Arial", 14), background="#1976D2", foreground="white").pack(pady=5)
        password_entry = ttk.Entry(inner_frame, font=("Arial", 14), width=25, show="*")
        password_entry.pack(pady=5)

        def register():
            username = username_entry.get()
            password = password_entry.get()
            if not username or not password:
                messagebox.showwarning("Input Error", "All fields are required!")
                return
            register_user(username, password)
            register_window.destroy()

        ttk.Button(inner_frame, text="Register", command=register, style="TButton").pack(pady=10)