import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import csv
from tkinter import filedialog
import threading
import websocket
import json
import requests

class EmployeeManagementApp:
    def __init__(self, root):
        self.cursor = None
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)

        self.db_connection = self.connect_db()
        self.apply_styles()

        # Sidebar
        self.sidebar = tk.Frame(self.root, bg="#2d3e50", width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        sidebar_buttons = [
            ("Home", self.show_home),
            ("Admin Login", self.admin_login),
            ("Employee Login", self.employee_login)
        ]

        for text, command in sidebar_buttons:
            ttk.Button(self.sidebar, text=text, command=command, style="Sidebar.TButton").pack(pady=10, fill="x")

        # Main Content Area
        self.content_frame = tk.Frame(self.root, bg="#f0f4fa")
        self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.show_home()

    def connect_db(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Add your database password
                database="employee_management"
            )
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")
            return None

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Sidebar.TButton", font=("Helvetica", 12, "bold"), foreground="#ffffff", background="#2d3e50", padding=10)
        style.map("Sidebar.TButton", background=[("active", "#3c78b4")], foreground=[("active", "#ffffff")])

    def show_home(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Welcome to Employee Management System", font=("Arial", 16, "bold"), bg="#f0f4fa").pack(pady=20)

    def admin_login(self):
        """Display the admin login form."""
        self.clear_content()
        # Header Frame
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)

        # Title Label
        title_label = tk.Label(header_frame, text="Admin Login", font=("Arial", 18, "bold"), bg="#4F6D7A", fg="white")
        title_label.pack()

        # Form Frame
        form_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        form_frame.pack(pady=20)

        # Email Input
        tk.Label(form_frame, text="Email:", font=("Arial", 12), bg="#f0f4fa", fg="#34495e").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.admin_email_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30)
        self.admin_email_entry.grid(row=0, column=1, padx=10, pady=10)

        # Password Input
        tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="#f0f4fa", fg="#34495e").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.admin_password_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30, show="*")
        self.admin_password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Login Button
        login_button = ttk.Button(form_frame, text="Login", style="Accent.TButton", command=self.authenticate_admin)
        login_button.grid(row=2, column=0, columnspan=2, pady=20)

    def authenticate_admin(self):
        """Authenticate the admin using the provided email and password."""
        email = self.admin_email_entry.get()
        password = self.admin_password_entry.get()

        if self.db_connection:
            cursor = self.db_connection.cursor()
            query = "SELECT * FROM admin WHERE email = %s AND password_hash = %s"
            cursor.execute(query, (email, password))
            result = cursor.fetchone()
            cursor.close()

            if result:
                messagebox.showinfo("Login Successful", "Welcome Admin!")
                self.admin_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid email or password")

    def admin_dashboard(self):
        self.clear_content()

        # Header frame with a modern background color
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)
        tk.Label(header_frame, text="Admin Dashboard", font=("Arial", 24, "bold"), fg="white", bg="#4F6D7A").pack()

        # Create a frame for the buttons
        button_frame = tk.Frame(self.content_frame, bg="#f0f4fa", padx=10, pady=10)
        button_frame.pack(fill="both", expand=True)

        # Function to apply consistent styling to buttons
        def style_button(btn):
            btn.config(relief="flat", font=("Arial", 12, "bold"), bg="#4F6D7A", fg="white", pady=10)
            btn.config(activebackground="#3a4d58", activeforeground="white", borderwidth=0)
            btn.grid(pady=10, padx=10, sticky="ew")

        # Button names and corresponding commands
        buttons = [
            ("Add Employee", self.add_employee),
            ("Edit Employee", self.edit_employee),
            ("Provide Performance Review", self.provide_review),
            ("View Employee Details", self.view_employees),
            ("View Salary History", self.adim_view_salary_history),
            ("View Progress", self.view_progress),
            ("View Feedback Review", self.view_feedback),
            ("View Attendance", self.view_attendance),
            ("Add Salary History", self.add_salary_history),
            ("Edit/Delete Salary History", self.edit_delete_salary_history),
            ("Edit/Delete Performance", self.manage_performance_reviews),
            ("Download Report", self.download_report),
            ("Send Notification", self.send_notification),
            ("View Notifications", self.view_admin_notifications)
        ]

        # Create and place the buttons in a 4-column grid layout
        row, col = 0, 0
        for idx, (text, command) in enumerate(buttons):
            btn = tk.Button(button_frame, text=text, command=command)
            style_button(btn)

            if row == 3:  # For row 4 (index 3), place buttons in columns 2 and 3 (index 1 and 2)
                if col == 0:  # First button in row 4, place it in column 2
                    btn.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
                    col += 1
                elif col == 1:  # Second button in row 4, place it in column 3
                    btn.grid(row=row, column=2, padx=10, pady=10, sticky="ew")
                    col += 1
            else:  # For other rows, use the regular grid system
                btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
                col += 1
                if col == 4:  # Once we reach the 4th column, move to the next row
                    col = 0
                    row += 1

        # Distinct logout button styling (placed at the center bottom)
        logout_btn = tk.Button(button_frame, text="Log Out", command=self.show_home)
        logout_btn.config(width=20, relief="flat", font=("Arial", 12, "bold"), bg="#d32f2f", fg="white", pady=12)
        logout_btn.config(activebackground="#b71c1c", activeforeground="white", borderwidth=0)
        logout_btn.grid(row=row + 1, column=1, padx=10, pady=20, sticky="ew", columnspan=2)

        # Optional: Hover effects for buttons
        def on_enter(event):
            event.widget.config(bg="#45a049", fg="white")

        def on_leave(event):
            event.widget.config(bg="#4F6D7A", fg="white")

        # Add hover effect to each button
        for btn in button_frame.winfo_children():
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

    def send_notification(self):
        """Admin sends a notification."""
        self.clear_content()

        # Header Frame
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)

        # Title Label
        title_label = tk.Label(header_frame, text="Send Notification", font=("Arial", 18, "bold"), bg="#4F6D7A", fg="white")
        title_label.pack()

        # Form Frame
        form_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        form_frame.pack(pady=10)

        # Employee ID Input (Optional)
        tk.Label(form_frame, text="Employee ID (Leave blank for all employees):", font=("Arial", 12), bg="#f0f4fa", fg="#34495e").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.employee_id_entry = ttk.Entry(form_frame, font=("Arial", 12), width=20)
        self.employee_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Message Input
        tk.Label(form_frame, text="Message:", font=("Arial", 12), bg="#f0f4fa", fg="#34495e").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.message_entry = tk.Text(form_frame, height=4, width=40, font=("Arial", 12), wrap=tk.WORD, bd=2, relief=tk.GROOVE)
        self.message_entry.grid(row=1, column=1, padx=10, pady=10)

        # Submit Button
        submit_button = ttk.Button(self.content_frame, text="Send", style="Accent.TButton", command=self.submit_notification)
        submit_button.pack(pady=10)

        # Back Button
        back_button = ttk.Button(self.content_frame, text="Back", style="Accent.TButton", command=self.admin_dashboard)
        back_button.pack(pady=10)

    def submit_notification(self):
        """Submit the notification."""
        employee_id = self.employee_id_entry.get().strip()
        message = self.message_entry.get("1.0", "end").strip()

        if not message:
            messagebox.showerror("Error", "Message cannot be empty!")
            return

        # If employee ID is left blank, set it to None (send to all employees)
        if not employee_id:
            employee_id = None
        else:
            try:
                employee_id = int(employee_id)  # Convert to integer
            except ValueError:
                messagebox.showerror("Error", "Employee ID must be a number!")
                return

        # Prepare payload
        payload = {"employee_id": employee_id, "message": message}

        # Send notification
        response = requests.post("http://localhost:5000/send_notification", json=payload)

        if response.status_code == 200:
            messagebox.showinfo("Success", "Notification sent!")
            self.admin_dashboard()
        else:
            messagebox.showerror("Error", "Failed to send notification.")


    def view_notifications(self):
        """View and delete notifications"""
        self.clear_content()
        tk.Label(self.content_frame, text="All Notifications", font=("Arial", 14, "bold"), bg="#f0f4fa").pack(pady=10)
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)

        response = requests.get("http://localhost:5000/get_notifications/0")  # 0 for all notifications
        notifications = response.json()

        for n in notifications:
            frame = tk.Frame(self.content_frame, bg="white", relief="solid", bd=1)
            frame.pack(pady=5, fill="x")

            tk.Label(frame, text=n["message"], bg="white", wraplength=400, justify="left").pack(side="left", padx=10)
            ttk.Button(frame, text="Delete", command=lambda id=n["id"]: self.delete_notification(id)).pack(side="right",
                                                                                                           padx=10)
            ttk.Button(self.content_frame, text="Back", command=self.admin_dashboard()).pack(pady=10)

    def delete_notification(self, notification_id):
        """Delete a notification"""
        requests.delete(f"http://localhost:5000/delete_notification/{notification_id}")
        messagebox.showinfo("Success", "Notification deleted!")
        self.view_notifications()


    def download_report(self):
        # Ask where to save the file
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("All Files", "*.*")],
                                                 title="Save Report As")
        if not file_path:
            return  # User canceled the save operation

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                # Write Employee Data
                cursor = self.db_connection.cursor()
                cursor.execute("SELECT * FROM employees")
                employees = cursor.fetchall()
                writer.writerow(["Employee Report"])
                writer.writerow(
                    ["Employee ID", "Name", "Email", "Position", "Department", "Phone", "Address", "Created At"])
                writer.writerows(employees)
                writer.writerow([])  # Blank line for separation

                # Write Salary History
                cursor.execute("SELECT * FROM salary")
                salary_data = cursor.fetchall()
                writer.writerow(["Salary History"])
                writer.writerow(["Salary ID", "Employee ID", "Salary Amount", "Payment Date"])
                writer.writerows(salary_data)
                writer.writerow([])

                # Write Performance Reviews
                cursor.execute("SELECT * FROM performance_reviews")
                reviews = cursor.fetchall()
                writer.writerow(["Performance Reviews"])
                writer.writerow(["Review ID", "Employee ID", "Review Text", "Review Date"])
                writer.writerows(reviews)
                writer.writerow([])

                # Write Attendance Records
                cursor.execute("SELECT * FROM attendance")
                attendance = cursor.fetchall()
                writer.writerow(["Attendance Records"])
                writer.writerow(
                    ["Attendance ID", "Employee ID", "Date", "Check-in Time", "Check-out Time", "Created At"])
                writer.writerows(attendance)
                writer.writerow([])

                # Write Feedback
                cursor.execute("SELECT * FROM feedback")
                feedbacks = cursor.fetchall()
                writer.writerow(["Employee Feedback"])
                writer.writerow(["Feedback ID", "Employee ID", "Name", "Feedback Text", "Submitted At"])
                writer.writerows(feedbacks)

                # Write Feedback
                cursor.execute("SELECT * FROM notifications")
                feedbacks = cursor.fetchall()
                writer.writerow(["Employee Feedback"])
                writer.writerow(["Feedback ID", "Notifications ID", "Employee ID", "Message", "Is Read", "Time Stamp"])
                writer.writerows(feedbacks)

                cursor.close()

            messagebox.showinfo("Success", "Report downloaded successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to download report: {e}")

    def manage_performance_reviews(self):
        self.clear_content()
        # Header Frame
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)

        # Title Label
        title_label = tk.Label(header_frame, text="Manage Performance Reviews", font=("Arial", 18, "bold"), bg="#4F6D7A", fg="white")
        title_label.pack()

        # Create a frame for the Treeview with scrollbars
        tree_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Create Treeview widget
        columns = ("Review ID", "Employee ID", "Employee Name", "Review Text", "Review Date")
        self.performance_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # Define column headings
        for col in columns:
            self.performance_tree.heading(col, text=col, anchor=tk.CENTER)
            self.performance_tree.column(col, width=150, anchor=tk.CENTER)  # Adjust width as needed

        # Add vertical and horizontal scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.performance_tree.yview)
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.performance_tree.xview)
        tree_scroll_x.pack(side="bottom", fill="x")

        self.performance_tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        self.performance_tree.pack(fill="both", expand=True)

        # Load Data
        self.load_performance_reviews()

        # Input Fields for Editing
        edit_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        edit_frame.pack(pady=10)

        # Review Text
        tk.Label(edit_frame, text="Review Text:", font=("Arial", 12), bg="#f0f4fa", fg="#34495e").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.review_text_entry = tk.Text(edit_frame, font=("Arial", 12), wrap=tk.WORD, height=5, width=50, bd=2, relief=tk.GROOVE)
        self.review_text_entry.grid(row=0, column=1, padx=5, pady=5)

        # Review Date
        tk.Label(edit_frame, text="Review Date (YYYY-MM-DD):", font=("Arial", 12), bg="#f0f4fa", fg="#34495e").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.review_date_entry = tk.Entry(edit_frame, font=("Arial", 12), width=30, bd=2, relief=tk.GROOVE)
        self.review_date_entry.grid(row=1, column=1, padx=5, pady=5)

        # Buttons for Editing and Deleting
        button_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        button_frame.pack(pady=10)

        # Styled Buttons
        ttk.Button(button_frame, text="Select", style="Accent.TButton", command=self.select_review).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Review", style="Accent.TButton", command=self.update_review).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Review", style="Accent.TButton", command=self.delete_review).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Back", style="Accent.TButton", command=self.admin_dashboard).grid(row=0, column=3, padx=5)

    def select_review(self):
        """Populate input fields with the selected review's data."""
        selected_item = self.performance_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a review to edit.")
            return

        # Get the selected review data
        review_data = self.performance_tree.item(selected_item, "values")

        # Populate input fields
        self.review_text_entry.delete(1.0, tk.END)
        self.review_text_entry.insert(tk.END, review_data[3])  # Review Text is the 4th column
        self.review_date_entry.delete(0, tk.END)
        self.review_date_entry.insert(0, review_data[4])  # Review Date is the 5th column

    def update_review(self):
        """Update the selected review with the new data."""
        selected_item = self.performance_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a review to update.")
            return

        # Get the selected review ID
        review_id = self.performance_tree.item(selected_item, "values")[0]

        # Get the updated data from input fields
        new_review_text = self.review_text_entry.get(1.0, tk.END).strip()
        new_review_date = self.review_date_entry.get()

        if not new_review_text or not new_review_date:
            messagebox.showwarning("Error", "All fields must be filled in!")
            return

        if self.db_connection:
            cursor = self.db_connection.cursor()
            try:
                cursor.execute("""
                    UPDATE performance_reviews
                    SET review_text=%s, review_date=%s
                    WHERE review_id=%s
                """, (new_review_text, new_review_date, review_id))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Review updated successfully!")
                self.load_performance_reviews()  # Refresh the list
            except Exception as e:
                self.db_connection.rollback()
                messagebox.showerror("Error", f"Error updating review: {e}")
            finally:
                cursor.close()

    def delete_review(self):
        """Delete the selected review."""
        selected_item = self.performance_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a review to delete.")
            return

        review_id = self.performance_tree.item(selected_item, "values")[0]

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this review?")
        if not confirm:
            return

        if self.db_connection:
            cursor = self.db_connection.cursor()
            try:
                cursor.execute("DELETE FROM performance_reviews WHERE review_id=%s", (review_id,))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Review deleted successfully.")
                self.load_performance_reviews()  # Refresh the list
            except Exception as e:
                self.db_connection.rollback()
                messagebox.showerror("Error", f"Error deleting review: {e}")
            finally:
                cursor.close()

    def load_performance_reviews(self):
        """Fetch and display performance reviews in the tree view."""
        if not hasattr(self, 'performance_tree'):
            messagebox.showerror("Error", "Performance tree view is not initialized.")
            return

        # Clear existing data from tree view
        for item in self.performance_tree.get_children():
            self.performance_tree.delete(item)

        if self.db_connection:
            cursor = self.db_connection.cursor()
            try:
                # Join performance_reviews with employee table to get employee names
                cursor.execute("""
                    SELECT p.review_id, p.employee_id, e.name, p.review_text, p.review_date
                    FROM performance_reviews p
                    JOIN employees e ON p.employee_id = e.employee_id
                """)
                rows = cursor.fetchall()
                for row in rows:
                    self.performance_tree.insert("", "end", values=row)
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading performance reviews: {e}")
            finally:
                cursor.close()

        def clear_content(self):
            for widget in self.content_frame.winfo_children():
                widget.destroy()

        def admin_dashboard(self):
            # Placeholder for the admin dashboard method
            print("Navigating to Admin Dashboard")

    def edit_delete_salary_history(self):
        self.clear_content()
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)
        tk.Label(self.content_frame, text="Edit/Delete Salary History", font=("Arial", 14, "bold"), bg="#f0f4fa").pack(
            pady=10)

        # Frame for TreeView and Scrollbars
        frame = tk.Frame(self.content_frame)
        frame.pack(fill=tk.BOTH, expand=True)

        tree_scroll_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        tree_scroll_y = ttk.Scrollbar(frame, orient=tk.VERTICAL)

        # Add "Employee Name" to the columns
        tree = ttk.Treeview(frame, columns=("Salary ID", "Employee ID", "Employee Name", "Salary Amount", "Payment Date"),
                            show="headings", yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        tree_scroll_x.config(command=tree.xview)
        tree_scroll_y.config(command=tree.yview)

        # Define column headings
        tree.heading("Salary ID", text="Salary ID")
        tree.heading("Employee ID", text="Employee ID")
        tree.heading("Employee Name", text="Employee Name")
        tree.heading("Salary Amount", text="Salary Amount")
        tree.heading("Payment Date", text="Payment Date")

        # Define column widths and alignment
        tree.column("Salary ID", width=100, anchor=tk.CENTER)
        tree.column("Employee ID", width=120, anchor=tk.CENTER)
        tree.column("Employee Name", width=200, anchor=tk.CENTER)
        tree.column("Salary Amount", width=150, anchor=tk.CENTER)
        tree.column("Payment Date", width=150, anchor=tk.CENTER)

        tree.pack(fill=tk.BOTH, expand=True)

        # Fetch and populate the treeview with salary data
        if self.db_connection:
            cursor = self.db_connection.cursor()
            # Join salary table with employee table to get employee names
            cursor.execute("""
                SELECT s.salary_id, s.employee_id, e.name, s.salary_amount, s.payment_date
                FROM salary s
                JOIN employees e ON s.employee_id = e.employee_id
            """)
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)
            cursor.close()

        # Create input fields for inline editing
        edit_frame = tk.Frame(self.content_frame)
        edit_frame.pack(pady=10)

        tk.Label(edit_frame, text="Salary Amount:").grid(row=0, column=0, padx=5)
        salary_amount_entry = tk.Entry(edit_frame)
        salary_amount_entry.grid(row=0, column=1, padx=5)

        tk.Label(edit_frame, text="Payment Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5)
        payment_date_entry = tk.Entry(edit_frame)
        payment_date_entry.grid(row=0, column=3, padx=5)

        # Function to handle selection and pre-fill input fields
        def select_record():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a salary record to edit.")
                return

            selected_values = tree.item(selected_item, "values")
            salary_amount_entry.delete(0, tk.END)
            payment_date_entry.delete(0, tk.END)

            salary_amount_entry.insert(0, selected_values[3])  # Salary Amount is the 4th column
            payment_date_entry.insert(0, selected_values[4])  # Payment Date is the 5th column

        # Function to Update Salary Record
        def update_salary():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a salary record to update.")
                return

            selected_values = tree.item(selected_item, "values")
            salary_id = selected_values[0]  # Salary ID is the 1st column

            new_salary_amount = salary_amount_entry.get()
            new_payment_date = payment_date_entry.get()

            if not new_salary_amount or not new_payment_date:
                messagebox.showerror("Error", "All fields must be filled in!")
                return

            if self.db_connection:
                cursor = self.db_connection.cursor()
                try:
                    cursor.execute("UPDATE salary SET salary_amount=%s, payment_date=%s WHERE salary_id=%s",
                                   (new_salary_amount, new_payment_date, salary_id))
                    self.db_connection.commit()
                    messagebox.showinfo("Success", "Salary record updated successfully!")
                    self.edit_delete_salary_history()  # Refresh the list
                except Exception as e:
                    self.db_connection.rollback()
                    messagebox.showerror("Error", f"Error updating record: {e}")
                finally:
                    cursor.close()

        # Function to Delete Selected Salary Record
        def delete_salary():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a salary record to delete.")
                return

            selected_values = tree.item(selected_item, "values")
            salary_id = selected_values[0]  # Salary ID is the 1st column

            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this salary record?")
            if confirm:
                if self.db_connection:
                    cursor = self.db_connection.cursor()
                    try:
                        cursor.execute("DELETE FROM salary WHERE salary_id=%s", (salary_id,))
                        self.db_connection.commit()
                        messagebox.showinfo("Success", "Salary record deleted successfully!")
                        self.edit_delete_salary_history()  # Refresh the list
                    except Exception as e:
                        self.db_connection.rollback()
                        messagebox.showerror("Error", f"Error deleting record: {e}")
                    finally:
                        cursor.close()

        # Buttons for Editing and Deleting
        button_frame = tk.Frame(self.content_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Select", command=select_record).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Salary", command=update_salary).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Salary", command=delete_salary).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Back", command=self.admin_dashboard).grid(row=0, column=3, padx=5)


    def add_salary_history(self):
        """Display the form to add salary history."""
        self.clear_content()
        # Title Label
        title_label = tk.Label(self.content_frame, text="Add Salary History", font=("Arial", 18, "bold"), bg="#f0f4fa",
                               fg="#2c3e50")
        title_label.pack(pady=20)

        # Form Frame
        form_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        form_frame.pack(pady=10)

        # Employee Name Dropdown
        tk.Label(form_frame, text="Select Employee:", font=("Arial", 12), bg="#f0f4fa", fg="#34495e").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.employee_var = tk.StringVar()
        self.employee_dropdown = ttk.Combobox(form_frame, textvariable=self.employee_var, font=("Arial", 12), state="readonly")
        self.employee_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Fetch employee names from the database
        self.load_employee_names()

        # Salary Amount input field
        tk.Label(form_frame, text="Salary Amount:", font=("Arial", 12), bg="#f0f4fa", fg="#34495e").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        salary_amount_entry = tk.Entry(form_frame, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        salary_amount_entry.grid(row=1, column=1, padx=10, pady=10)

        # Payment Date input field
        tk.Label(form_frame, text="Payment Date (YYYY-MM-DD):", font=("Arial", 12), bg="#f0f4fa", fg="#34495e").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        payment_date_entry = tk.Entry(form_frame, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        payment_date_entry.grid(row=2, column=1, padx=10, pady=10)

        # Submit button to add the salary history
        def submit_salary_history():
            selected_employee = self.employee_var.get()
            salary_amount = salary_amount_entry.get()
            payment_date = payment_date_entry.get()

            # Validation (you can add more validation as needed)
            if not selected_employee or not salary_amount or not payment_date:
                messagebox.showerror("Error", "All fields must be filled in!")
                return

            # Extract employee ID from the selected employee name
            employee_id = self.employee_name_to_id.get(selected_employee)

            # Insert data into the database
            if self.db_connection:
                cursor = self.db_connection.cursor()
                try:
                    cursor.execute("INSERT INTO salary (employee_id, salary_amount, payment_date) VALUES (%s, %s, %s)",
                                   (employee_id, salary_amount, payment_date))
                    self.db_connection.commit()
                    messagebox.showinfo("Success", "Salary History Added Successfully")
                    self.adim_view_salary_history()  # Refresh the salary history view
                except Exception as e:
                    self.db_connection.rollback()
                    messagebox.showerror("Error", f"Error adding salary history: {e}")
                finally:
                    cursor.close()

        # Styled Submit Button
        submit_button = tk.Button(self.content_frame, text="Add Salary", font=("Arial", 12, "bold"), bg="#34495e",
                                  fg="white",
                                  activebackground="#2ecc71", activeforeground="white", bd=0, padx=20, pady=10,
                                  command=submit_salary_history)
        submit_button.pack(pady=20)

        # Styled Back Button
        back_button = tk.Button(self.content_frame, text="Back", font=("Arial", 12, "bold"), bg="#34495e", fg="white",
                                activebackground="#2ecc71", activeforeground="white", bd=0, padx=20, pady=10,
                                command=self.admin_dashboard)
        back_button.pack(pady=10)

    def load_employee_names(self):
        """Fetch employee names from the database and populate the dropdown."""
        if self.db_connection:
            cursor = self.db_connection.cursor()
            try:
                cursor.execute("SELECT employee_id, name FROM employees")
                employees = cursor.fetchall()

                # Create a mapping of employee names to IDs
                self.employee_name_to_id = {f"{e[1]} (ID: {e[0]})": e[0] for e in employees}

                # Populate the dropdown with employee names
                self.employee_dropdown["values"] = list(self.employee_name_to_id.keys())
                self.employee_dropdown.current(0)  # Set default selection to the first employee
            except Exception as e:
                messagebox.showerror("Error", f"Error fetching employee data: {e}")
            finally:
                cursor.close()
    def view_attendance(self):
        self.clear_content()
        tk.Label(self.content_frame, text="View Attendance", font=("Arial", 14, "bold"), bg="#f0f4fa").pack(pady=10)

        # Treeview to show attendance records
        treeview_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        treeview_frame.pack(expand=True, fill=tk.BOTH)

        # Add "Employee Name" to the columns
        columns = ("Employee ID", "Employee Name", "Date", "Check-In Time", "Check-Out Time")
        self.attendance_tree = ttk.Treeview(treeview_frame, columns=columns, show="headings", selectmode="browse")

        # Define column headings
        for col in columns:
            self.attendance_tree.heading(col, text=col, anchor=tk.W)
            self.attendance_tree.column(col, width=150, anchor=tk.W)  # Adjust column width as needed

        # Scrollbars
        vertical_scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=self.attendance_tree.yview)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        horizontal_scrollbar = ttk.Scrollbar(treeview_frame, orient="horizontal", command=self.attendance_tree.xview)
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.attendance_tree.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        self.attendance_tree.pack(expand=True, fill=tk.BOTH)

        # Fetch attendance data from the database
        if self.db_connection:
            cursor = self.db_connection.cursor()
            # Join attendance table with employee table to get employee names
            cursor.execute("""
                SELECT a.employee_id, e.name, a.date, a.check_in_time, a.check_out_time
                FROM attendance a
                JOIN employees e ON a.employee_id = e.employee_id
            """)
            attendance_data = cursor.fetchall()
            cursor.close()

            # Insert data into the Treeview
            for record in attendance_data:
                self.attendance_tree.insert("", "end", values=record)

        # Back Button
        ttk.Button(self.content_frame, text="Back", command=self.admin_dashboard).pack(pady=10)

    def view_feedback(self):
        self.clear_content()
        tk.Label(self.content_frame, text="View Feedback Reviews", font=("Arial", 14, "bold"), bg="#f0f4fa").pack(
            pady=10)

        # Treeview to show feedback
        treeview_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        treeview_frame.pack(expand=True, fill=tk.BOTH)

        columns = ("Employee ID", "Name", "Feedback Text", "Submitted At")
        self.feedback_tree = ttk.Treeview(treeview_frame, columns=columns, show="headings", selectmode="browse")

        # Define column headings
        for col in columns:
            self.feedback_tree.heading(col, text=col, anchor=tk.W)
            self.feedback_tree.column(col, width=250, anchor=tk.W)

        # Scrollbars
        vertical_scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=self.feedback_tree.yview)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        horizontal_scrollbar = ttk.Scrollbar(treeview_frame, orient="horizontal", command=self.feedback_tree.xview)
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.feedback_tree.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        self.feedback_tree.pack(expand=True, fill=tk.BOTH)

        # Bind selection event to display full feedback
        self.feedback_tree.bind("<<TreeviewSelect>>", self.display_full_feedback)

        # Fetch feedback data from the database
        if self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT employee_id, name, feedback_text, submitted_at FROM feedback")
            feedback_data = cursor.fetchall()
            cursor.close()

            # Insert data into the Treeview
            for record in feedback_data:
                self.feedback_tree.insert("", "end", values=record)

        # Add a Text widget to display the full feedback
        self.feedback_text_widget = tk.Text(self.content_frame, wrap=tk.WORD, font=("Arial", 12), bg="white", fg="black", height=10)
        self.feedback_text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.feedback_text_widget.config(state=tk.DISABLED)  # Make the text widget read-only

        # Back Button
        ttk.Button(self.content_frame, text="Back", command=self.admin_dashboard).pack(pady=10)

    def display_full_feedback(self, event):
        # Get the selected item from the Treeview
        selected_item = self.feedback_tree.selection()
        if not selected_item:
            return

        # Retrieve the feedback text from the selected row
        item_values = self.feedback_tree.item(selected_item, "values")
        feedback_text = item_values[2]  # Feedback Text is the third column

        # Display the full feedback in the Text widget
        self.feedback_text_widget.config(state=tk.NORMAL)  # Enable editing temporarily
        self.feedback_text_widget.delete(1.0, tk.END)  # Clear previous content
        self.feedback_text_widget.insert(tk.END, feedback_text)  # Insert new content
        self.feedback_text_widget.config(state=tk.DISABLED)  # Make the text widget read-only again

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    def view_progress(self):
        self.clear_content()
        tk.Label(self.content_frame, text="View Progress (Performance Reviews)", font=("Arial", 14, "bold"),
                 bg="#f0f4fa").pack(pady=10)

        # Treeview to show performance reviews
        treeview_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        treeview_frame.pack(expand=True, fill=tk.BOTH)

        columns = ("Employee ID", "Review Text", "Review Date")
        self.progress_tree = ttk.Treeview(treeview_frame, columns=columns, show="headings", selectmode="browse")

        # Define column headings
        for col in columns:
            self.progress_tree.heading(col, text=col, anchor=tk.W)
            self.progress_tree.column(col, width=250, anchor=tk.W)

        # Scrollbars
        vertical_scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=self.progress_tree.yview)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        horizontal_scrollbar = ttk.Scrollbar(treeview_frame, orient="horizontal", command=self.progress_tree.xview)
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.progress_tree.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        self.progress_tree.pack(expand=True, fill=tk.BOTH)

        # Bind selection event to display full review
        self.progress_tree.bind("<<TreeviewSelect>>", self.display_full_message)

        # Fetch progress data from the database
        if self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT employee_id, review_text, review_date FROM performance_reviews")
            progress_data = cursor.fetchall()
            cursor.close()

            # Insert data into the Treeview
            for record in progress_data:
                self.progress_tree.insert("", "end", values=record)

        # Add a Text widget to display the full review
        self.review_text_widget = tk.Text(self.content_frame, wrap=tk.WORD, font=("Arial", 12), bg="white", fg="black",
                                          height=10)
        self.review_text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.review_text_widget.config(state=tk.DISABLED)  # Make the text widget read-only

        # Back Button
        ttk.Button(self.content_frame, text="Back", command=self.admin_dashboard).pack(pady=10)

    def view_feedback(self):
        """Display feedback reviews in a Treeview."""
        self.clear_content()
        tk.Label(self.content_frame, text="View Feedback Reviews", font=("Arial", 14, "bold"), bg="#f0f4fa").pack(
            pady=10)

        # Treeview to show feedback
        treeview_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        treeview_frame.pack(expand=True, fill=tk.BOTH)

        # Define columns for the Treeview
        columns = ("Feedback ID", "Employee ID", "Name", "Feedback Text", "Submitted At")
        self.feedback_tree = ttk.Treeview(treeview_frame, columns=columns, show="headings", selectmode="browse")

        # Define column headings
        for col in columns:
            self.feedback_tree.heading(col, text=col, anchor=tk.W)
            self.feedback_tree.column(col, width=150, anchor=tk.W)

        # Scrollbars
        vertical_scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=self.feedback_tree.yview)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        horizontal_scrollbar = ttk.Scrollbar(treeview_frame, orient="horizontal", command=self.feedback_tree.xview)
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.feedback_tree.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        self.feedback_tree.pack(expand=True, fill=tk.BOTH)

        # Bind selection event to display full feedback
        self.feedback_tree.bind("<<TreeviewSelect>>", self.display_full_feedback)

        # Fetch feedback data from the database
        if self.db_connection:
            cursor = self.db_connection.cursor()
            try:
                # Fetch feedback data sorted by most recent date
                query = """
                SELECT feedback_id, employee_id, name, feedback_text, submitted_at
                FROM feedback
                ORDER BY submitted_at DESC
                """
                cursor.execute(query)
                feedback_data = cursor.fetchall()

                # Insert data into the Treeview
                for record in feedback_data:
                    self.feedback_tree.insert("", "end", values=record)
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to fetch feedback data: {e}")
            finally:
                cursor.close()

        # Add a Text widget to display the full feedback
        self.feedback_text_widget = tk.Text(self.content_frame, wrap=tk.WORD, font=("Arial", 12), bg="white",
                                            fg="black", height=10)
        self.feedback_text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.feedback_text_widget.config(state=tk.DISABLED)  # Make the text widget read-only

        # Delete Feedback Button
        delete_button = ttk.Button(self.content_frame, text="Delete Selected Feedback", command=self.delete_feedback)
        delete_button.pack(pady=10)

        # Back Button
        ttk.Button(self.content_frame, text="Back", command=self.admin_dashboard).pack(pady=10)

    def display_full_feedback(self, event):
        """Display the full feedback text when a row is selected."""
        selected_item = self.feedback_tree.selection()
        if selected_item:
            # Get the selected record
            selected_record = self.feedback_tree.item(selected_item, "values")
            feedback_text = selected_record[3]  # Feedback Text is at index 3

            # Display the full feedback in the Text widget
            self.feedback_text_widget.config(state=tk.NORMAL)
            self.feedback_text_widget.delete(1.0, tk.END)
            self.feedback_text_widget.insert(tk.END, feedback_text)
            self.feedback_text_widget.config(state=tk.DISABLED)

    def delete_feedback(self):
        """Delete the selected feedback from the database."""
        selected_item = self.feedback_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a feedback entry to delete.")
            return

        # Get the feedback ID from the selected row
        selected_record = self.feedback_tree.item(selected_item, "values")
        feedback_id = selected_record[0]  # Feedback ID is at index 0

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this feedback?")
        if not confirm:
            return

        # Delete the feedback from the database
        if self.db_connection:
            cursor = self.db_connection.cursor()
            try:
                query = "DELETE FROM feedback WHERE feedback_id = %s"
                cursor.execute(query, (feedback_id,))
                self.db_connection.commit()

                # Remove the selected row from the Treeview
                self.feedback_tree.delete(selected_item)

                # Clear the feedback text widget
                self.feedback_text_widget.config(state=tk.NORMAL)
                self.feedback_text_widget.delete(1.0, tk.END)
                self.feedback_text_widget.config(state=tk.DISABLED)

                messagebox.showinfo("Success", "Feedback deleted successfully!")
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to delete feedback: {e}")
            finally:
                cursor.close()
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def adim_view_salary_history(self):
        """Display the salary history with employee names."""
        self.clear_content()
        # Title Label
        title_label = tk.Label(self.content_frame, text="View Salary History", font=("Arial", 18, "bold"), bg="#f0f4fa", fg="#2c3e50")
        title_label.pack(pady=20)

        # Treeview to show salary history
        treeview_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        treeview_frame.pack(expand=True, fill=tk.BOTH)

        # Define columns (including Employee Name)
        columns = ("Employee ID", "Employee Name", "Salary Amount", "Payment Date")
        self.salary_tree = ttk.Treeview(treeview_frame, columns=columns, show="headings", selectmode="browse")

        # Define column headings
        for col in columns:
            self.salary_tree.heading(col, text=col, anchor=tk.W)
            self.salary_tree.column(col, width=150, anchor=tk.W)

        # Scrollbars
        vertical_scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=self.salary_tree.yview)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        horizontal_scrollbar = ttk.Scrollbar(treeview_frame, orient="horizontal", command=self.salary_tree.xview)
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.salary_tree.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        self.salary_tree.pack(expand=True, fill=tk.BOTH)

        # Fetch salary history data from the database
        if self.db_connection:
            cursor = self.db_connection.cursor()
            # Join salary table with employees table to get employee names
            cursor.execute("""
                SELECT s.employee_id, e.name, s.salary_amount, s.payment_date
                FROM salary s
                JOIN employees e ON s.employee_id = e.employee_id
            """)
            salary_history = cursor.fetchall()
            cursor.close()

            # Insert data into the Treeview
            for record in salary_history:
                self.salary_tree.insert("", "end", values=record)

        # Back Button
        ttk.Button(self.content_frame, text="Back", style="Accent.TButton", command=self.admin_dashboard).pack(pady=20)
    def add_employee(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Add New Employee", font=("Arial", 16, "bold"), bg="#4F6D7A",
                 fg="white").pack(pady=20)

        # Define a frame for the form fields
        form_frame = tk.Frame(self.content_frame, bg="#f0f4fa", padx=20, pady=20)
        form_frame.pack(pady=20)  # This places the form below the label

        # Create labels and entry fields with styling
        labels = ["Name:", "Email:", "Password:", "Position:", "Department:", "Phone:", "Address:"]
        entries = []

        # Grid for better control over form field sizes
        for row, label_text in enumerate(labels):
            label = tk.Label(form_frame, text=label_text, bg="#f0f4fa", font=("Arial", 12))
            label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

            entry = ttk.Entry(form_frame, font=("Arial", 12), width=30)  # Reduced width
            entry.grid(row=row, column=1, padx=10, pady=5)
            entries.append(entry)

        # Unpack entries for better organization
        name_entry, email_entry, password_entry, position_entry, department_entry, phone_entry, address_entry = entries

        # Save button with styling
        def save_employee():
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()  # Should be hashed in a real-world scenario
            position = position_entry.get()
            department = department_entry.get()
            phone = phone_entry.get()
            address = address_entry.get()

            if not (name and email and password and position and department):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                cursor = self.db_connection.cursor()
                query = "INSERT INTO employees (name, email, password_hash, position, department, phone, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (name, email, password, position, department, phone, address))
                self.db_connection.commit()
                cursor.close()
                messagebox.showinfo("Success", "Employee added successfully!")
                self.admin_dashboard()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        # Buttons section with styling
        button_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        button_frame.pack(pady=10)  # Adjust padding to move buttons below the form

        # Place Save Employee and Back buttons side by side
        save_button = ttk.Button(button_frame, text="Save Employee", command=save_employee, width=20, style="TButton")
        save_button.grid(row=0, column=0, padx=10, pady=10)

        back_button = ttk.Button(button_frame, text="Back", command=self.admin_dashboard, width=20, style="TButton")
        back_button.grid(row=0, column=1, padx=10, pady=10)

        # Styling for the buttons
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), padding=10, relief="flat", background="#4F6D7A",
                        foreground="white")
        style.map("TButton", background=[("active", "#45a049")])

        # Optional: Set background color for the window if needed
        self.content_frame.config(bg="#f0f4fa")

    def edit_employee(self):
        self.clear_content()
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)

        # Title label with bold font and background color
        tk.Label(self.content_frame, text="Edit Employee Information", font=("Arial", 18, "bold"), bg="#4F6D7A",
                 fg="white").pack(pady=20)

        # Fetch employees from the database
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT employee_id, name FROM employees")
        employees = cursor.fetchall()
        cursor.close()

        if not employees:
            tk.Label(self.content_frame, text="No employees found!", fg="red", bg="#f0f4fa").pack(pady=10)
            ttk.Button(self.content_frame, text="Back", command=self.admin_dashboard).pack(pady=10)
            return

        # Create a frame for the form to keep everything organized
        form_frame = tk.Frame(self.content_frame, bg="#f0f4fa", padx=20, pady=20)
        form_frame.pack(pady=20, padx=20)  # Center form with padding

        # Label and dropdown for selecting an employee
        tk.Label(form_frame, text="Select Employee:", font=("Arial", 12), bg="#f0f4fa").grid(row=0, column=0,
                                                                                             sticky="w", pady=10)

        self.selected_employee = tk.StringVar()
        employee_dropdown = ttk.Combobox(form_frame, textvariable=self.selected_employee, state="readonly",
                                         font=("Arial", 12), width=50)
        employee_dropdown['values'] = [f"{emp[0]} - {emp[1]}" for emp in employees]
        employee_dropdown.grid(row=0, column=1, pady=10, padx=10, sticky="w")  # Align left

        # Styling for consistent button sizes
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), padding=10, relief="flat", background="#4F6D7A",
                        foreground="white", width=20)
        style.map("TButton", background=[("active", "#45a049")])

        # Load Details Button
        load_button = ttk.Button(form_frame, text="Load Details",
                                 command=lambda: self.load_employee_details(employee_dropdown))
        load_button.grid(row=1, column=0, columnspan=2, pady=15)

        # Create a frame for the buttons to align them nicely
        button_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        button_frame.pack(pady=10)

        # Back Button - Center it below the form
        back_button = ttk.Button(button_frame, text="Back", command=self.admin_dashboard)
        back_button.pack(pady=10)

        # Optional: Set background color for the content frame to make it consistent
        self.content_frame.config(bg="#f0f4fa")

    def load_employee_selection(self):
        """Load a dropdown to select an employee."""
        self.clear_content()

        # Header Frame
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)

        # Header Label
        tk.Label(header_frame, text="Select Employee", font=("Arial", 20, "bold"), bg="#4F6D7A", fg="white").pack()

        # Fetch employee list from the database
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT employee_id, name FROM employees")
        employees = cursor.fetchall()
        cursor.close()

        # Dropdown to select employee
        employee_names = [f"{emp[0]} - {emp[1]}" for emp in employees]
        self.employee_dropdown = ttk.Combobox(self.content_frame, values=employee_names, font=("Arial", 12), state="readonly")
        self.employee_dropdown.pack(pady=20, padx=20)

        # Button to load employee details
        load_button = tk.Button(self.content_frame, text="Load Details", command=lambda: self.load_employee_details(self.employee_dropdown), bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
        load_button.pack(pady=10)

        # Back Button
        back_button = tk.Button(self.content_frame, text="Back", command=self.admin_dashboard, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
        back_button.pack(pady=10)

    def load_employee_details(self, employee_dropdown):
        """Load and display employee details for editing."""
        employee_info = employee_dropdown.get()
        if not employee_info:
            messagebox.showwarning("Selection Required", "Please select an employee!")
            return

        emp_id = employee_info.split(" - ")[0]  # Extract employee ID

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT name, email, position, department, phone, address, password_hash FROM employees WHERE employee_id = %s",
                       (emp_id,))
        employee = cursor.fetchone()
        cursor.close()

        if not employee:
            messagebox.showerror("Error", "Employee not found!")
            return

        # Clear previous content
        self.clear_content()

        # Header Label with Styling
        tk.Label(
            self.content_frame, text="Edit Employee Information",
            font=("Arial", 18, "bold"), bg="#f0f4fa", fg="#0A192F"
        ).pack(pady=15)

        # Form Frame for Better Layout
        form_frame = tk.Frame(self.content_frame, bg="#f0f4fa", padx=30, pady=20)
        form_frame.pack(pady=10, padx=20)

        # Styling for Consistent Button Design
        style = ttk.Style()
        style.configure("Modern.TButton", font=("Arial", 12, "bold"), padding=10, relief="flat",
                        background="#4F6D7A", foreground="white", width=18)
        style.map("Modern.TButton", background=[("active", "#45a049")])

        # Fields and Input Boxes
        fields = ["Name:", "Email:", "Position:", "Department:", "Phone:", "Address:", "Password:"]
        self.entries = {}

        for i, field in enumerate(fields):
            # Label with left alignment
            label = tk.Label(form_frame, text=field, font=("Arial", 12, "bold"), bg="#f0f4fa", anchor="w")
            label.grid(row=i, column=0, sticky="w", pady=8, padx=10)

            # Entry field with modern width and padding
            entry = ttk.Entry(form_frame, font=("Arial", 12), width=35)
            entry.grid(row=i, column=1, pady=5, padx=10)
            if i < len(employee):  # Pre-fill with existing data (except password)
                entry.insert(0, employee[i])

            self.entries[field] = entry

        # Button Frame for Alignment
        button_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        button_frame.pack(pady=15)

        # Update and Back Buttons - Navy Blue
        update_button = ttk.Button(button_frame, text="Update", command=lambda: self.update_employee(emp_id),
                                   style="Modern.TButton")
        update_button.pack(side="left", padx=10)

        back_button = ttk.Button(button_frame, text="Back", command=self.admin_dashboard, style="Modern.TButton")
        back_button.pack(side="left", padx=10)

        # Set the background for the entire content frame
        self.content_frame.config(bg="#f0f4fa")

    def update_employee(self, emp_id):
        """Update employee details, including password (stored in plain text)."""
        updated_data = {key: entry.get() for key, entry in self.entries.items()}

        cursor = self.db_connection.cursor()
        query = """UPDATE employees SET name=%s, email=%s, position=%s, department=%s, phone=%s, address=%s, password_hash=%s WHERE employee_id=%s"""
        values = (
            updated_data["Name:"], updated_data["Email:"], updated_data["Position:"],
            updated_data["Department:"], updated_data["Phone:"], updated_data["Address:"],
            updated_data["Password:"],  # Store password in plain text (not recommended for production)
            emp_id
        )

        try:
            cursor.execute(query, values)
            self.db_connection.commit()
            messagebox.showinfo("Success", "Employee details updated successfully!")
            self.admin_dashboard()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to update: {err}")
        finally:
            cursor.close()
    def provide_review(self):
        self.clear_content()
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)
        tk.Label(self.content_frame, text="Provide Performance Review", font=("Arial", 14, "bold"), bg="#f0f4fa").pack(
            pady=10)

        # Fetch employee names and IDs from the database
        employees = []
        if self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT employee_id, name FROM employees")
            employees = cursor.fetchall()
            cursor.close()

        if not employees:
            tk.Label(self.content_frame, text="No employees found.", bg="#f0f4fa", fg="red").pack(pady=5)
            ttk.Button(self.content_frame, text="Back", command=self.admin_dashboard).pack(pady=10)
            return

        # Employee selection dropdown
        tk.Label(self.content_frame, text="Select Employee:", bg="#f0f4fa").pack()
        self.selected_employee = tk.StringVar()
        employee_dropdown = ttk.Combobox(self.content_frame, textvariable=self.selected_employee, state="readonly")
        employee_dropdown["values"] = [f"{emp[0]} - {emp[1]}" for emp in employees]
        employee_dropdown.pack(pady=5)

        # Review Entry
        tk.Label(self.content_frame, text="Performance Review:", bg="#f0f4fa").pack()
        self.review_entry = tk.Text(self.content_frame, height=5, width=50)
        self.review_entry.pack(pady=5)

        # Submit Button
        ttk.Button(self.content_frame, text="Submit Review", command=self.submit_review).pack(pady=10)


        # Back Button
        ttk.Button(self.content_frame, text="Back", command=self.admin_dashboard).pack(pady=10)

    def submit_review(self):
        """Handles storing the performance review in the database."""
        selected = self.selected_employee.get()
        review_text = self.review_entry.get("1.0", tk.END).strip()

        if not selected or not review_text:
            messagebox.showwarning("Input Error", "Please select an employee and enter a review.")
            return

        # Extract Employee ID from selection
        employee_id = selected.split(" - ")[0]  # Extracts the numeric ID

        # Insert the review into the database
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                query = "INSERT INTO performance_reviews (employee_id, review_text) VALUES (%s, %s)"
                cursor.execute(query, (employee_id, review_text))
                self.db_connection.commit()
                cursor.close()
                messagebox.showinfo("Success", "Performance review submitted successfully.")
                self.admin_dashboard()  # Redirect back to the dashboard
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error inserting review: {err}")

    def view_employees(self):
        self.clear_content()
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)
        tk.Label(self.content_frame, text="View Employee Details", font=("Arial", 14, "bold"), bg="#f0f4fa").pack(
            pady=10)

        # Frame to hold the Treeview and Scrollbars
        treeview_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        treeview_frame.pack(expand=True, fill=tk.BOTH)

        # Treeview widget
        columns = ("Employee ID", "Name", "Email", "Position", "Department", "Phone", "Address")
        self.tree = ttk.Treeview(treeview_frame, columns=columns, show="headings", selectmode="browse")

        # Define the column headings
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, width=150, anchor=tk.W)

        # Scrollbars
        vertical_scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=self.tree.yview)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        horizontal_scrollbar = ttk.Scrollbar(treeview_frame, orient="horizontal", command=self.tree.xview)
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        self.tree.pack(expand=True, fill=tk.BOTH)

        # Fetch employee data from the database
        if self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT employee_id, name, email, position, department, phone, address FROM employees")
            employees = cursor.fetchall()
            cursor.close()

            # Insert the data into the Treeview
            for employee in employees:
                self.tree.insert("", "end", values=employee)

        # Back Button
        ttk.Button(self.content_frame, text="Back", command=self.admin_dashboard).pack(pady=10)

    def connect_to_db(self):
        """Connect to MySQL database"""
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",  # Replace with your database username
                password="",  # Replace with your database password
                database="employee_management"  # Replace with your database name
            )
            self.cursor = self.db_connection.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")
            self.quit()

    def clear_content(self):
        """Clear the content of the current frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def employee_login(self):
        """Display the employee login form."""
        self.clear_content()
        # Header Frame
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)

        # Title Label
        title_label = tk.Label(header_frame, text="Employee Login", font=("Arial", 18, "bold"), bg="#4F6D7A", fg="white")
        title_label.pack()

        # Form Frame
        form_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        form_frame.pack(pady=20)

        # Username Input
        tk.Label(form_frame, text="Username:", font=("Arial", 12), bg="#f0f4fa", fg="#34495e").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.username_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Password Input
        tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="#f0f4fa", fg="#34495e").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Login Button
        login_button = ttk.Button(self.content_frame, text="Login", style="Accent.TButton", command=self.validate_employee_login)
        login_button.pack(pady=20)

    def validate_employee_login(self):
        """Validate the employee's login credentials."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.db_connection:
            cursor = self.db_connection.cursor()
            try:
                cursor.execute("SELECT * FROM employees WHERE username = %s AND password_hash = %s", (username, password))
                result = cursor.fetchone()
                if result:
                    messagebox.showinfo("Login Successful", "Welcome Employee!")
                    self.employee_dashboard()  # Redirect to employee dashboard
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password")
            except Exception as e:
                messagebox.showerror("Error", f"Error during login: {e}")
            finally:
                cursor.close()

    def clear_content(self):
        """Clear all widgets from the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def validate_employee_login(self):
        """Validate employee login credentials"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Input Error", "Please enter both username and password.")
            return

        # Connect to the database
        self.connect_to_db()

        # Query to check employee credentials
        query = "SELECT * FROM employees WHERE email = %s AND password_hash = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()

        if result:
            self.employee_id = result[0]  # Assuming the employee_id is the first column in the table
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            # Proceed to the employee dashboard or main system
            self.show_employee_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_employee_dashboard(self):
        """Display the employee dashboard after successful login"""
        self.clear_content()

        header_frame = tk.Frame(self.content_frame, bg="#2C3E50", padx=20, pady=30)  # Deeper, more sophisticated navy
        header_frame.pack(fill="x", pady=20)

        tk.Label(header_frame, text="Employee Dashboard", font=("Segoe UI", 22, "bold"), fg="white", bg="#2C3E50").pack(pady=10)

        button_frame = tk.Frame(self.content_frame, bg="#E0E8F9")
        button_frame.pack(pady=30, expand=True)

        buttons = [
            ("Check-in/Out", self.record_attendance),
            ("Salary History", self.view_salary_history),
            ("Feedback", self.submit_feedback),
            ("Personal Info", self.update_personal_info),
            ("Performance", self.view_performance_records),
            ("Notifications", self.view_employee_notifications)
        ]

        row, col = 0, 0
        for text, command in buttons:
            button = tk.Button(button_frame, text=text, command=command,
                               bg="#A9C2EB", fg="#2C3E50", padx=25, pady=12,
                               relief=tk.RAISED, borderwidth=0, font=("Segoe UI", 12), cursor="hand2")
            button.grid(row=row, column=col, padx=15, pady=15, sticky="nsew") #added sticky
            col += 1
            if col > 2:
                col = 0
                row += 1

        # Configure grid weights to make buttons expand evenly
        for i in range(3):
            button_frame.columnconfigure(i, weight=1)
        for i in range(2):
            button_frame.rowconfigure(i, weight=1)

        def go_back():
            self.employee_login()

        logout_button = tk.Button(self.content_frame, text="Log Out", command=go_back,
                                   bg="#A9C2EB", fg="#2C3E50", padx=25, pady=12,
                                   relief=tk.RAISED, borderwidth=0, font=("Segoe UI", 12), cursor="hand2")
        logout_button.pack(pady=30)
        logout_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

        self.start_notification_listener()


    def start_notification_listener(self):
        """Start WebSocket listener in a separate thread"""

        def listen():
            ws = websocket.WebSocketApp(f"ws://localhost:5000/socket.io/?transport=websocket",
                                        on_message=lambda ws, msg: messagebox.showinfo("New Notification", msg))
            ws.run_forever()

        threading.Thread(target=listen, daemon=True).start()

    def view_employee_notifications(self):
        """Fetch and display employee notifications."""
        self.clear_content()

        def go_back():
            """Go back to the employee dashboard."""
            self.show_employee_dashboard()

        # Header Frame
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)

        # Header Label
        tk.Label(header_frame, text="Your Notifications", font=("Arial", 20, "bold"), bg="#4F6D7A", fg="white").pack()

        # Back Button
        back_button = tk.Button(self.content_frame, text="Back", command=go_back, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
        back_button.pack(pady=10)

        # Fetch notifications from the API
        response = requests.get(f"http://localhost:5000/get_notifications/{self.employee_id}")
        notifications = response.json()

        # Create a Frame to hold the notifications
        notification_frame = tk.Frame(self.content_frame, bg="#E0F7FA")
        notification_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Add scrollable canvas for long notifications
        canvas = tk.Canvas(notification_frame, bg="#E0F7FA", highlightthickness=0)
        scroll_y = tk.Scrollbar(notification_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Create a frame to hold the notifications in the canvas
        inner_frame = tk.Frame(canvas, bg="#E0F7FA")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Check if there are any notifications
        if not notifications:
            tk.Label(inner_frame, text="No notifications found.", font=("Arial", 12), bg="#E0F7FA", fg="#4F6D7A").pack(pady=20)
            return

        # Loop through the notifications and display them
        for n in notifications:
            # Notification Container
            notification_container = tk.Frame(inner_frame, bg="white", bd=2, relief="solid", padx=10, pady=10)
            notification_container.pack(fill="x", pady=5, padx=5)

            # Notification Message (truncated to 50 characters initially)
            message = n["message"]
            truncated_message = message[:50] + "..." if len(message) > 50 else message

            message_label = tk.Label(notification_container, text=truncated_message, font=("Arial", 12), bg="white", wraplength=600, justify="left")
            message_label.pack(side="left", padx=10, pady=5, fill="x", expand=True)

            # Show Full Message Button (if message is longer than 50 characters)
            if len(message) > 50:
                def toggle_message():
                    """Toggle between truncated and full message."""
                    if message_label.cget("text") == truncated_message:
                        message_label.config(text=message)
                        toggle_button.config(text="Show Less")
                    else:
                        message_label.config(text=truncated_message)
                        toggle_button.config(text="Show Full")

                toggle_button = ttk.Button(notification_container, text="Show Full", command=toggle_message, style="Custom.TButton")
                toggle_button.pack(side="right", padx=5, pady=5)

            # Delete Button
            delete_button = ttk.Button(notification_container, text="Delete", command=lambda id=n["id"]: self.edelete_notification(id), style="Custom.TButton")
            delete_button.pack(side="right", padx=5, pady=5)

            # Divider between notifications
            divider = tk.Frame(inner_frame, bg="#4F6D7A", height=1)
            divider.pack(fill="x", pady=5)

        # Update the scrollable region
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Custom style for the buttons
        style = ttk.Style()
        style.configure("Custom.TButton", background="#FF5252", foreground="white", font=("Arial", 10, "bold"), borderwidth=0)

    def edelete_notification(self, notification_id):
        """Delete a notification by ID."""
        response = requests.delete(f"http://localhost:5000/delete_notification/{notification_id}")
        if response.status_code == 200:
            messagebox.showinfo("Success", "Notification deleted successfully.")
            self.view_employee_notifications()  # Refresh the notifications list
        else:
            messagebox.showerror("Error", "Failed to delete notification.")
    def view_admin_notifications(self):
        """Fetch and display all notifications with employee names, dates, and a 'View Full Message' feature."""
        self.clear_content()
        # Header Frame
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)

        # Title Label
        title_label = tk.Label(header_frame, text="All Notifications", font=("Arial", 18, "bold"), bg="#4F6D7A", fg="white")
        title_label.pack()

        # Create a main container frame with two columns
        main_container = tk.Frame(self.content_frame, bg="#f0f4fa")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Side: Notification List
        left_frame = tk.Frame(main_container, bg="#f0f4fa", width=400)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Create a canvas and scrollbars for the notification list
        canvas = tk.Canvas(left_frame, bg="#f0f4fa", highlightthickness=0)
        vertical_scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        horizontal_scrollbar = tk.Scrollbar(left_frame, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

        # Create a frame inside the canvas to hold the notifications
        notification_frame = tk.Frame(canvas, bg="#f0f4fa")
        notification_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=notification_frame, anchor="nw")

        # Pack the canvas and scrollbars
        canvas.pack(side="left", fill="both", expand=True)
        vertical_scrollbar.pack(side="right", fill="y")
        horizontal_scrollbar.pack(side="bottom", fill="x")

        # Right Side: Full Notification Display
        right_frame = tk.Frame(main_container, bg="white", width=400, relief="solid", bd=1)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Title for the full notification section
        tk.Label(right_frame, text="Full Notification", font=("Arial", 14, "bold"), bg="white", fg="#34495e").pack(pady=10)

        # Text widget to display the full notification
        self.full_message_text = tk.Text(right_frame, wrap="word", font=("Arial", 12), bg="white", relief="flat", height=20)
        self.full_message_text.pack(padx=10, pady=10, fill="both", expand=True)

        # Fetch notifications from the Flask endpoint
        response = requests.get("http://localhost:5000/get_admin_notifications")
        notifications = response.json()
        preview_length = 100  # Maximum number of characters to show in preview

        for n in notifications:
            # Create a frame for each notification
            frame = tk.Frame(notification_frame, bg="white", relief="solid", bd=1, padx=10, pady=10)
            frame.pack(pady=10, fill="x", padx=10)

            # Header: Employee name and notification date
            header_frame = tk.Frame(frame, bg="white")
            header_frame.pack(fill="x", pady=5)

            employee_label = tk.Label(header_frame, text=f"Employee: {n['employee_name']}",
                                      font=("Arial", 12, "bold"), bg="white", fg="#34495e")
            employee_label.pack(side="left", padx=10)

            date_label = tk.Label(header_frame, text=f"Sent on: {n['date_sent']}",
                                  font=("Arial", 10), bg="white", fg="#7f8c8d")
            date_label.pack(side="right", padx=10)

            # Notification message preview
            message = n["message"]
            if len(message) > preview_length:
                message_preview = message[:preview_length] + "..."
            else:
                message_preview = message

            message_label = tk.Label(frame, text=message_preview, bg="white",
                                     wraplength=350, justify="left", font=("Arial", 12), fg="#2c3e50", anchor="w")
            message_label.pack(pady=10, fill="x")

            # Button to view the full message
            view_button = ttk.Button(frame, text="View Full Message", style="Accent.TButton",
                                     command=lambda msg=message: self.display_full_message(msg))
            view_button.pack(side="left", padx=10)

            # Button to delete the notification
            delete_button = ttk.Button(frame, text="Delete", style="Accent.TButton",
                                       command=lambda id=n["id"]: self.delete_notification(id))
            delete_button.pack(side="right", padx=10)

        # Back button to return to the admin dashboard
        ttk.Button(self.content_frame, text="Back", style="Accent.TButton", command=self.admin_dashboard).pack(pady=20)

    def display_full_message(self, message):
        """Display the full notification message in the right frame."""
        self.full_message_text.config(state="normal")
        self.full_message_text.delete(1.0, tk.END)
        self.full_message_text.insert(tk.END, message)
        self.full_message_text.config(state="disabled")

    def delete_notification(self, notification_id):
        """Delete a specific notification"""
        response = requests.delete(f"http://localhost:5000/delete_notification/{notification_id}")

        if response.status_code == 200:
            messagebox.showinfo("Success", "Notification deleted successfully!")
            self.view_admin_notifications()  # Refresh the list
        else:
            messagebox.showerror("Error", "Failed to delete notification.")

    def record_attendance(self):
        """Check-in/Check-out attendance logic"""
        self.clear_content()
        # Header Frame
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)

        # Title Label
        title_label = tk.Label(header_frame, text="Record Attendance", font=("Arial", 18, "bold"), bg="#4F6D7A",
                               fg="white")
        title_label.pack()

        # Check if today's attendance record already exists
        query = "SELECT * FROM attendance WHERE employee_id = %s AND date = CURDATE()"
        self.cursor.execute(query, (self.employee_id,))
        attendance_record = self.cursor.fetchone()

        if attendance_record:  # If attendance record exists for today
            # If already checked in, show a check-out button
            if attendance_record[4] is None:  # check_out_time is NULL
                check_out_button = tk.Button(self.content_frame, text="Check-out", font=("Arial", 12, "bold"),
                                             bg="#34495e", fg="white", activebackground="#2ecc71",
                                             activeforeground="white",
                                             bd=0, padx=20, pady=10, command=self.check_out)
                check_out_button.pack(pady=20)
            else:
                tk.Label(self.content_frame, text="You have already checked out today.", font=("Arial", 12),
                         bg="#f0f4fa", fg="#34495e").pack(pady=20)
        else:
            # If no record exists for today, show a check-in button
            check_in_button = tk.Button(self.content_frame, text="Check-in", font=("Arial", 12, "bold"),
                                        bg="#34495e", fg="white", activebackground="#2ecc71", activeforeground="white",
                                        bd=0, padx=20, pady=10, command=self.check_in)
            check_in_button.pack(pady=20)

        # Back Button to go to dashboard
        back_button = tk.Button(self.content_frame, text="Back", font=("Arial", 12, "bold"),
                                bg="#34495e", fg="white", activebackground="#2ecc71", activeforeground="white",
                                bd=0, padx=20, pady=10, command=self.show_employee_dashboard)
        back_button.pack(pady=10)

    def check_in(self):
        """Record check-in time"""
        query = """
            INSERT INTO attendance (employee_id, date, check_in_time, created_at) 
            VALUES (%s, CURDATE(), NOW(), NOW())
        """
        try:
            self.cursor.execute(query, (self.employee_id,))
            self.db_connection.commit()
            messagebox.showinfo("Check-in", "Check-in recorded successfully.")
            self.record_attendance()  # Refresh the interface
        except Exception as e:
            messagebox.showerror("Error", f"Error recording check-in: {e}")

    def check_out(self):
        """Record check-out time"""
        query = """
            UPDATE attendance 
            SET check_out_time = NOW() 
            WHERE employee_id = %s AND date = CURDATE() AND check_out_time IS NULL
        """
        try:
            self.cursor.execute(query, (self.employee_id,))
            self.db_connection.commit()
            if self.cursor.rowcount > 0:
                messagebox.showinfo("Check-out", "Check-out recorded successfully.")
                self.record_attendance()  # Refresh the interface
            else:
                messagebox.showerror("Error", "No check-in record found for today.")
        except Exception as e:
            messagebox.showerror("Error", f"Error recording check-out: {e}")


    def view_salary_history(self):
        """View salary history linked to employee ID"""
        self.clear_content()

        def go_back():
            self.show_employee_dashboard()
            header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
            header_frame.pack(fill="x", pady=20)

        tk.Label(self.content_frame, text="Salary History", font=("Arial", 14, "bold"), bg="#f0f4fa").pack(pady=10)

        # Create a frame for the Treeview and scrollbars
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(pady=10, fill="both", expand=True)

        # Create Treeview
        salary_tree = ttk.Treeview(tree_frame, columns=("Salary", "Payment Date"), show="headings", height=10)

        # Define the columns
        salary_tree.heading("Salary", text="Salary Amount")
        salary_tree.heading("Payment Date", text="Payment Date")

        salary_tree.column("Salary", width=150, anchor="center")
        salary_tree.column("Payment Date", width=150, anchor="center")

        # Add vertical and horizontal scrollbars
        vertical_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=salary_tree.yview)
        vertical_scroll.pack(side="right", fill="y")
        salary_tree.configure(yscrollcommand=vertical_scroll.set)

        horizontal_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=salary_tree.xview)
        horizontal_scroll.pack(side="bottom", fill="x")
        salary_tree.configure(xscrollcommand=horizontal_scroll.set)

        salary_tree.pack(fill="both", expand=True)

        # Query to fetch salary history
        query = "SELECT salary_amount, payment_date FROM salary WHERE employee_id = %s"
        self.cursor.execute(query, (self.employee_id,))
        salary_data = self.cursor.fetchall()

        # Insert the data into the Treeview
        for row in salary_data:
            salary_tree.insert("", "end", values=(row[0], row[1]))

        # Back Button below the Treeview
        back_button = tk.Button(self.content_frame, text="Back", command=go_back)
        back_button.pack(pady=20)

    def submit_feedback(self):
        """Submit feedback for the employee"""
        self.clear_content()

        def go_back():
            """Go back to the employee dashboard."""
            self.show_employee_dashboard()

        # Header Label
        tk.Label(self.content_frame, text="Submit Feedback", font=("Arial", 16, "bold"), bg="#f0f4fa").pack(pady=20)

        # Feedback Label
        tk.Label(self.content_frame, text="Please provide your feedback below:", font=("Arial", 12), bg="#f0f4fa").pack(
            pady=5)

        # Create a frame for the feedback text area with padding
        feedback_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        feedback_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Text widget for multi-line feedback input
        feedback_text = tk.Text(feedback_frame, height=6, width=40, wrap=tk.WORD, font=("Arial", 12))
        feedback_text.pack(pady=10)

        # Optional: Add a scrollbar for the text area
        scrollbar = tk.Scrollbar(feedback_frame, orient="vertical", command=feedback_text.yview)
        scrollbar.pack(side="right", fill="y")
        feedback_text.config(yscrollcommand=scrollbar.set)

        # Submit Button
        submit_button = tk.Button(self.content_frame, text="Submit Feedback", font=("Arial", 12), bg="#4CAF50",
                                  fg="white",
                                  command=lambda: self.store_feedback(feedback_text.get("1.0", tk.END).strip()))
        submit_button.pack(pady=10)

        # Back Button to go to dashboard
        back_button = tk.Button(self.content_frame, text="Back to Dashboard", font=("Arial", 12), bg="#FF6347",
                                fg="white", command=go_back)
        back_button.pack(pady=10)

    def store_feedback(self, feedback):
        """Store the feedback in the feedback table"""
        if not feedback:
            messagebox.showerror("Error", "Please enter feedback.")
            return

        try:
            # Fetch the employee's name from the database
            query = "SELECT name FROM employees WHERE employee_id = %s"
            self.cursor.execute(query, (self.employee_id,))
            employee_name = self.cursor.fetchone()[0]  # Fetch the name from the result

            # Insert feedback into the database
            query = """
            INSERT INTO feedback (employee_id, name, feedback_text, submitted_at)
            VALUES (%s, %s, %s, NOW())
            """
            self.cursor.execute(query, (self.employee_id, employee_name, feedback))
            self.db_connection.commit()

            # Success message
            messagebox.showinfo("Feedback Submitted", "Your feedback has been submitted successfully!")

            # Redirect to the employee dashboard after submitting feedback
            self.show_employee_dashboard()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to submit feedback: {e}")
    import hashlib
    import tkinter as tk
    from tkinter import messagebox

    def update_personal_info(self):
        """Update personal information including email, phone, address, and password."""
        self.clear_content()

        def go_back():
            self.show_employee_dashboard()

        def save_changes():
            """Save updated personal information to the database"""
            new_email = email_entry.get().strip()
            new_phone = phone_entry.get().strip()
            new_address = address_entry.get().strip()
            new_password = password_entry.get().strip()

            if not new_email or not new_phone or not new_address:
                messagebox.showerror("Error", "Email, phone, and address cannot be empty!")
                return

            if new_email and not self.validate_email(new_email):
                messagebox.showerror("Error", "Invalid email format!")
                return

            if new_phone and not self.validate_phone(new_phone):
                messagebox.showerror("Error", "Invalid phone number!")
                return

            update_query = "UPDATE employees SET email = %s, phone = %s, address = %s WHERE employee_id = %s"
            update_values = (new_email, new_phone, new_address, self.employee_id)

            self.cursor.execute(update_query, update_values)
            self.db_connection.commit()

            # If the user provided a new password, update it in plain text
            if new_password:
                password_query = "UPDATE employees SET password_hash = %s WHERE employee_id = %s"
                self.cursor.execute(password_query, (new_password, self.employee_id))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Password updated successfully!")

            messagebox.showinfo("Success", "Personal information updated successfully!")
            self.show_employee_dashboard()

        # Fetch employee data
        self.cursor.execute("SELECT employee_id, name, email, phone, address FROM employees WHERE employee_id = %s",
                            (self.employee_id,))
        employee_data = self.cursor.fetchone()

        if not employee_data:
            messagebox.showerror("Error", "Employee data not found!")
            return

        emp_id, emp_name, emp_email, emp_phone, emp_address = employee_data

        # Page title
        tk.Label(self.content_frame, text="Update Personal Information", font=("Arial", 16, "bold"), bg="#f0f4fa", fg="#2c3e50").grid(
            row=0, column=0, columnspan=2, pady=10
        )

        # Create a frame to display employee info on the left side
        info_frame = tk.Frame(self.content_frame, bg="#e0e6f8", padx=20, pady=20, relief="ridge", bd=2)
        info_frame.grid(row=1, column=0, rowspan=5, padx=20, pady=10, sticky="n")

        tk.Label(info_frame, text="Employee Details", font=("Arial", 12, "bold"), bg="#e0e6f8", fg="#2c3e50").pack(pady=5)
        tk.Label(info_frame, text=f"ID: {emp_id}", bg="#e0e6f8", anchor="w", fg="#2c3e50").pack(fill="x")
        tk.Label(info_frame, text=f"Name: {emp_name}", bg="#e0e6f8", anchor="w", fg="#2c3e50").pack(fill="x")
        tk.Label(info_frame, text=f"Email: {emp_email}", bg="#e0e6f8", anchor="w", fg="#2c3e50").pack(fill="x")
        tk.Label(info_frame, text=f"Phone: {emp_phone}", bg="#e0e6f8", anchor="w", fg="#2c3e50").pack(fill="x")
        tk.Label(info_frame, text=f"Address: {emp_address}", bg="#e0e6f8", anchor="w", fg="#2c3e50").pack(fill="x")

        # Labels and Entry Fields (on the right side)
        tk.Label(self.content_frame, text="New Email:", bg="#f0f4fa", fg="#2c3e50").grid(row=1, column=1, sticky="e", padx=10, pady=5)
        email_entry = tk.Entry(self.content_frame, width=30, bg="white", fg="#2c3e50", insertbackground="#2c3e50")
        email_entry.insert(0, emp_email)
        email_entry.grid(row=1, column=2, padx=10, pady=5)

        tk.Label(self.content_frame, text="New Phone:", bg="#f0f4fa", fg="#2c3e50").grid(row=2, column=1, sticky="e", padx=10, pady=5)
        phone_entry = tk.Entry(self.content_frame, width=30, bg="white", fg="#2c3e50", insertbackground="#2c3e50")
        phone_entry.insert(0, emp_phone)
        phone_entry.grid(row=2, column=2, padx=10, pady=5)

        tk.Label(self.content_frame, text="New Address:", bg="#f0f4fa", fg="#2c3e50").grid(row=3, column=1, sticky="e", padx=10, pady=5)
        address_entry = tk.Entry(self.content_frame, width=30, bg="white", fg="#2c3e50", insertbackground="#2c3e50")
        address_entry.insert(0, emp_address)
        address_entry.grid(row=3, column=2, padx=10, pady=5)

        tk.Label(self.content_frame, text="New Password (Optional):", bg="#f0f4fa", fg="#2c3e50").grid(
            row=4, column=1, sticky="e", padx=10, pady=5
        )
        password_entry = tk.Entry(self.content_frame, width=30, show="*", bg="white", fg="#2c3e50", insertbackground="#2c3e50")
        password_entry.grid(row=4, column=2, padx=10, pady=5)

        # Back and Save buttons side by side
        button_frame = tk.Frame(self.content_frame, bg="#f0f4fa")
        button_frame.grid(row=5, column=1, columnspan=2, pady=20)

        back_button = tk.Button(button_frame, text="Back", command=go_back, bg="#95a5a6", fg="white", width=15, activebackground="#7f8c8d")
        back_button.pack(side="left", padx=10)

        save_button = tk.Button(button_frame, text="Save Changes", command=save_changes, bg="#27ae60", fg="white",
                                width=15, activebackground="#219150")
        save_button.pack(side="right", padx=10)

    def validate_email(self, email):
        """
        Validates the email format.
        A simple check to ensure the email contains an '@' and a '.'.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email is valid, False otherwise.
        """
        return "@" in email and "." in email

    def validate_phone(self, phone):
        """
        Validates the phone number format.
        A simple check to ensure the phone number contains only digits and is at least 10 characters long.

        Args:
            phone (str): The phone number to validate.

        Returns:
            bool: True if the phone number is valid, False otherwise.
        """
        return phone.isdigit() and len(phone) >= 10
    def view_performance_records(self):
        """View performance records linked to employee ID."""
        self.clear_content()

        def go_back():
            """Go back to the employee dashboard."""
            self.show_employee_dashboard()

        # Header Frame
        header_frame = tk.Frame(self.content_frame, bg="#4F6D7A", padx=20, pady=20)
        header_frame.pack(fill="x", pady=20)

        # Header Label
        tk.Label(header_frame, text="Performance Records", font=("Arial", 20, "bold"), bg="#4F6D7A", fg="white").pack()

        # Back Button to go to dashboard
        back_button = tk.Button(self.content_frame, text="Back", command=go_back, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
        back_button.pack(pady=10)

        # Fetch performance records from the database
        query = "SELECT * FROM performance_reviews WHERE employee_id = %s"
        self.cursor.execute(query, (self.employee_id,))
        performance_data = self.cursor.fetchall()

        # Create a Frame to hold the records
        record_frame = tk.Frame(self.content_frame, bg="#E0F7FA")
        record_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Add scrollable canvas for long text
        canvas = tk.Canvas(record_frame, bg="#E0F7FA")
        scroll_y = tk.Scrollbar(record_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Create a frame to hold the records in the canvas
        performance_frame = tk.Frame(canvas, bg="#E0F7FA")
        canvas.create_window((0, 0), window=performance_frame, anchor="nw")

        # Add a nice divider for each record
        divider = tk.Frame(performance_frame, bg="#4F6D7A", height=2)
        divider.pack(fill="x", pady=5)

        # Check if there are any records
        if not performance_data:
            messagebox.showinfo("No Records", "No performance reviews found.")
            return

        # Loop through the records and display them
        for row in performance_data:
            review_id, employee_id, review_text, review_date = row

            # Display each review in a structured format
            review_container = tk.Frame(performance_frame, bg="#FFFFFF", bd=2, relief="solid", padx=10, pady=5)
            review_container.pack(fill="x", pady=5, padx=10)

            # Review Date
            review_date_label = tk.Label(review_container, text=f"Review Date: {review_date}", font=("Arial", 12, "bold"), bg="#FFFFFF")
            review_date_label.grid(row=0, column=0, sticky="w")

            # Review Text (with ellipsis for large text)
            review_text_label = tk.Label(review_container, text=f"Review: {review_text[:100]}...", font=("Arial", 10), bg="#FFFFFF", wraplength=350, justify="left")
            review_text_label.grid(row=1, column=0, pady=5, sticky="w", padx=5)

            # Show full review in the same window (if it's longer than the preview)
            if len(review_text) > 100:
                def show_full_review():
                    """Toggle between showing the full review and the truncated version."""
                    if review_text_label.cget("text") == f"Review: {review_text[:100]}...":
                        review_text_label.config(text=f"Review: {review_text}", wraplength=700)
                        full_review_button.config(text="Show Less")
                    else:
                        review_text_label.config(text=f"Review: {review_text[:100]}...", wraplength=350)
                        full_review_button.config(text="Show Full Review")

                full_review_button = tk.Button(review_container, text="Show Full Review", command=show_full_review, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=5, pady=2)
                full_review_button.grid(row=2, column=0, pady=5, padx=5)

            # Add a divider between each review for clarity
            review_divider = tk.Frame(performance_frame, bg="#4F6D7A", height=2)
            review_divider.pack(fill="x", pady=5)

        # Update the scrollable region
        performance_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def quit(self):
        """Quit the application"""
        if self.db_connection:
            self.db_connection.close()
        self.root.quit()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()

    style = ttk.Style()
    style.configure("Accent.TButton", font=("Arial", 12), background="#34495e", foreground="white")
    style.map("Accent.TButton", background=[("active", "#2ecc71")])
