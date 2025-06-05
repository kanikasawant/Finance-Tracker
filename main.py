import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from login import LoginPage  # Import the login page

def open_finance_tracker(username):
    """This function starts the finance tracker after login."""
    global LOGGED_IN_USER
    LOGGED_IN_USER = username  # Store the logged-in username
    root.withdraw()  # Hide the login window
    new_root = tk.Tk()
    FinanceTracker(new_root, username)  # Open finance tracker
    new_root.mainloop()

def restart_app():
    """Restarts the application by reopening the login window."""
    new_root = tk.Tk()
    LoginPage(new_root, open_finance_tracker)
    new_root.mainloop()

class FinanceTracker:
    def __init__(self, root, username):
        self.root = root    
        self.root.title(f"{username}'s Personal Finance Tracker")
        self.root.geometry("900x700")
        self.root.configure(bg="#0A192F")  

        self.username = username  # Store the username

        # Database connection
        self.conn = sqlite3.connect("finance.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # UI Components
        self.setup_ui()
    def create_table(self):
     """Drops and recreates the transactions table."""
     self.cursor.execute("DROP TABLE IF EXISTS transactions")  
     self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        category TEXT,
        amount REAL,
        type TEXT,
        payment_mode TEXT,
        date TEXT
    )
    """)
     self.conn.commit()

    
    def setup_ui(self):
        # Set overall style
        style = ttk.Style(self.root)
        
        # Title Label
        ttk.Label(self.root, text="BudgetMate", font=("Montserrat", 24, "bold"), background="lightblue", foreground="black").pack(pady=15)
        
        """Sets up the user interface components."""
        # Use tk.Frame instead of ttk.Frame to allow background color
        self.input_frame = tk.Frame(self.root, bg="lightblue", padx=20, pady=20)
        self.input_frame.pack(pady=20)

        # Date Input using Calendar
        ttk.Label(self.input_frame, text="Date:", font=("Arial", 10), background="#0A192F", foreground="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = DateEntry(self.input_frame, width=12, background='#0A192F', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        # Type Selection
        ttk.Label(self.input_frame, text="Type:", font=("Arial", 10), background="#0A192F", foreground="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.type_combobox = ttk.Combobox(self.input_frame, values=["Income", "Expense"], state="readonly", font=("Arial", 10))
        self.type_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.type_combobox.bind("<<ComboboxSelected>>", self.toggle_category_field)

        # Amount Input
        ttk.Label(self.input_frame, text="Amount:", font=("Arial", 10), background="#0A192F", foreground="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(self.input_frame, font=("Arial", 10))
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        # Category Input with Dropdown
        self.category_label = ttk.Label(self.input_frame, text="Category:", font=("Arial", 10), background="#0A192F", foreground="white")
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(self.input_frame, textvariable=self.category_var, values=["Food", "Transport", "Shopping", "Bills", "Other"], state="normal", font=("Arial", 10))

        # Payment Mode Selection
        ttk.Label(self.input_frame, text="Payment Mode:", font=("Arial", 10), background="#0A192F", foreground="white").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.payment_mode_combobox = ttk.Combobox(self.input_frame, values=["Cash", "Credit Card", "Debit Card", "UPI", "Bank Transfer"], state="readonly", font=("Arial", 10))
        self.payment_mode_combobox.grid(row=4, column=1, padx=5, pady=5)

        # Treeview for displaying transactions
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(pady=10)

        self.tree = ttk.Treeview(self.tree_frame, columns=("id", "category", "amount", "type", "payment_mode", "date"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("type", text="Type")
        self.tree.heading("payment_mode", text="Payment Mode")
        self.tree.heading("date", text="Date")

        self.tree.column("id", width=30)
        self.tree.pack(pady=10)
        self.load_transactions()

        # Buttons
        self.add_button = tk.Button(self.input_frame, text="Add Transaction", command=self.add_transaction, width=20, bg="green", fg="white")
        self.add_button.grid(row=5, column=0, columnspan=3, pady=15)

        # Buttons for Analysis
        self.analysis_button = tk.Button(self.root, text="Show Analysis", command=self.show_analysis, width=20, bg="green", fg="white")
        self.analysis_button.pack(pady=10)

        # Button for deleting transactions
        self.delete_button = tk.Button(self.root, text="Delete Transactions", command=self.delete_selected_record, width=20, bg="green", fg="white")
        self.delete_button.pack(pady=10)

        # Button for Logout
        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout, width=20, bg="red", fg="white")
        self.logout_button.pack(pady=10)
        

    def apply_styles(self):
        """Apply the custom styles to the widgets."""
        style = ttk.Style()
        
        # General widget style
        style.configure("TLabel", font=("Arial", 10), background="#f4f4f9", foreground="black")
        style.configure("TButton", font=("Arial", 10), background="#4CAF50", foreground="white", padding=10)
        style.configure("TButton:hover", background="#45a049")

        # Accent buttons (Add, Show Analysis, etc.)
        style.configure("AccentButton.TButton", font=("Arial", 10, "bold"), background="#2196F3", foreground="white", padding=10)
        style.map("AccentButton.TButton", background=[('active', '#1976D2')])

        # Treeview styling
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#333", foreground="white")
        style.configure("Treeview", font=("Arial", 10), background="#f9f9f9", foreground="black", rowheight=25)
        style.map("Treeview", background=[('selected', '#4CAF50')])

        # Input frame styling
        style.configure("InputFrame.TFrame", background="#ffffff")

    def toggle_category_field(self, event=None):
        """Shows or hides the category field based on type selection."""
        selected_type = self.type_combobox.get()

        if selected_type == "Expense":
            self.category_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
            self.category_combobox.grid(row=3, column=1, padx=5, pady=5)
        else:
            self.category_label.grid_remove()
            self.category_combobox.grid_remove()

    def add_transaction(self):
        """Handles adding a new transaction to the database."""
        type_ = self.type_combobox.get()
        category = self.category_combobox.get() if type_ == "Expense" else "N/A"
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        payment_mode = self.payment_mode_combobox.get()

        if not (amount and type_ and date and payment_mode):
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        try:
            amount = float(amount)
            self.cursor.execute(
                "INSERT INTO transactions (username, category, amount, type, payment_mode, date) VALUES (?, ?, ?, ?, ?, ?)",
                (self.username, category, amount, type_, payment_mode, date)
            )
            self.conn.commit()
            self.load_transactions()  # Refresh transactions immediately
            messagebox.showinfo("Success", "Transaction added successfully!")

            # Clear inputs properly
            self.category_combobox.set("")  
            self.amount_entry.delete(0, tk.END)
            self.type_combobox.set("")
            self.payment_mode_combobox.set("")
            self.date_entry.set_date(datetime.today())  

        except ValueError:
            messagebox.showwarning("Input Error", "Amount must be a number!")

    def load_transactions(self):
        """Loads transactions for the logged-in user and displays them in the GUI."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.cursor.execute("SELECT id, category, amount, type, payment_mode, date FROM transactions WHERE username = ?", (self.username,))
        
        for row in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

    def delete_selected_record(self):
        """Deletes the selected transaction from the Treeview and database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")
            return

        # Get the selected record's ID
        record_id = self.tree.item(selected_item)["values"][0]

        # Confirm the deletion with the user
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete record {record_id}?"):
            try:
                self.cursor.execute("DELETE FROM transactions WHERE id = ?", (record_id,))
                self.conn.commit()
                self.load_transactions()  # Refresh the Treeview after deletion
                messagebox.showinfo("Success", f"Record {record_id} deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete record: {str(e)}")

    def show_analysis(self):
        self.cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
        data = self.cursor.fetchall()

        if not data:
            messagebox.showinfo("No Data", "No expense data available for analysis.")
            return

        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        # Create a pie chart
        fig, ax = plt.subplots()
        ax.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.
        ax.set_title("Expense Distribution")

        # Display the chart in a new window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Expense Analysis")
        chart_window.geometry("400x400")

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    def logout(self):
        """Logs out the user and returns to the login screen."""
        self.root.destroy()  # Close the finance tracker window
        restart_app()  # Call restart_app() correctly

if __name__ == "__main__":
        root = tk.Tk()

        # Start the login page first
        login = LoginPage(root, open_finance_tracker)
        root.mainloop()
