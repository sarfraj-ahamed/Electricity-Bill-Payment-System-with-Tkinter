import tkinter as tk
from tkinter import messagebox
import uuid


class ElectricityBillSystem:
    def __init__(self):
        self.bills = {}  # A dictionary to hold the bills for each user

    def generate_user_id(self):
        return str(uuid.uuid4())  # Generates a unique user ID using uuid

    def add_bill(self, user_id, amount):
        """Adds a new bill for a user."""
        if user_id not in self.bills:
            self.bills[user_id] = []  # Create an empty list of bills for new users
        self.bills[user_id].append({
            "amount": amount,
            "total_amount": amount,
            "status": "Unpaid",
            "payment_details": None
        })
        return user_id

    def get_bill_history(self, user_id):
        """Returns all bills history for a user."""
        return self.bills.get(user_id, [])

    def get_total_amount_due(self, user_id):
        """Returns the total amount due for a user."""
        total_due = 0
        if user_id in self.bills:
            for bill in self.bills[user_id]:
                if bill["status"] == "Unpaid":
                    total_due += bill["total_amount"]
        return total_due

    def update_payment_status(self, user_id, bill_index, payment_details, payment_amount, status):
        """Updates payment status and details for a specific bill."""
        if user_id in self.bills and 0 <= bill_index < len(self.bills[user_id]):
            self.bills[user_id][bill_index]["status"] = status
            self.bills[user_id][bill_index]["payment_details"] = {"details": payment_details, "amount": payment_amount}
            self.bills[user_id][bill_index]["total_amount"] = payment_amount  # Update the total amount
            return True
        return False

    def delay_payment(self, user_id, bill_index, days):
        """Handles delayed payment and updates the status, with added percentage depending on days delayed."""
        if user_id in self.bills and 0 <= bill_index < len(self.bills[user_id]):
            bill = self.bills[user_id][bill_index]
            original_amount = bill["amount"]
            total_amount = bill["total_amount"]
            
            # Calculate additional amount based on delay days
            if days == 10:
                extra_amount = total_amount * 0.02  # 2% for 10 days delay
            elif days == 20:
                extra_amount = total_amount * 0.05  # 5% for 20 days delay
            elif days == 30:
                extra_amount = total_amount * 0.10  # 10% for 30 days delay
            else:
                extra_amount = 0

            new_total_amount = total_amount + extra_amount
            # Update the bill's total amount to include the surcharge
            self.bills[user_id][bill_index]["total_amount"] = new_total_amount
            
            return True
        return False


class BillApp:
    def __init__(self, root, system):
        self.system = system
        self.root = root
        self.root.title("Electricity Bill Payment System")
        self.root.geometry("600x500")
        self.root.configure(bg="#fafafa")
        self.create_main_frame()

    def create_main_frame(self):
        """Main frame with options to add/view bills."""
        self.clear_frame()  # Clear any existing frames
        self.main_frame = tk.Frame(self.root, bg="#e6f7ff", bd=2, relief="ridge", padx=10, pady=10)
        self.main_frame.pack(fill="both", expand=True)

        label_font = ("Helvetica", 12, "bold")
        tk.Label(self.main_frame, text="Electricity Bill Payment System", font=("Helvetica", 16, "bold"), bg="#e6f7ff").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Button(self.main_frame, text="Add New Bill", command=self.add_bill_page, bg="#66b3ff", fg="white", width=20).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(self.main_frame, text="View Bill History", command=self.view_bill_history_page, bg="#66b3ff", fg="white", width=20).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.main_frame, text="Upload Payment Details", command=self.upload_payment_page, bg="#66b3ff", fg="white", width=20).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.main_frame, text="View Amount Due", command=self.view_amount_due_page, bg="#66b3ff", fg="white", width=20).grid(row=4, column=0, columnspan=2, pady=10)

    def clear_frame(self):
        """Clears the current frame"""
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def add_bill_page(self):
        """Page to add a new bill for a user."""
        self.clear_frame()  # Clear current frame

        self.add_bill_frame = tk.Frame(self.root, bg="#e6f7ff", bd=2, relief="ridge")
        self.add_bill_frame.pack(fill="both", expand=True, padx=10, pady=10)

        label_font = ("Helvetica", 12, "bold")
        tk.Label(self.add_bill_frame, text="Enter User ID:", font=label_font, bg="#e6f7ff").grid(row=0, column=0, pady=5, padx=10, sticky="e")
        self.user_id_entry = tk.Entry(self.add_bill_frame, width=25)
        self.user_id_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.add_bill_frame, text="Enter Bill Amount:", font=label_font, bg="#e6f7ff").grid(row=1, column=0, pady=5, padx=10, sticky="e")
        self.amount_entry = tk.Entry(self.add_bill_frame, width=25)
        self.amount_entry.grid(row=1, column=1, pady=5)

        tk.Button(self.add_bill_frame, text="Add Bill", command=self.confirm_add_bill, bg="#66b3ff", fg="white", width=20).grid(row=2, column=0, columnspan=2, pady=15)
        tk.Button(self.add_bill_frame, text="Back", command=self.back_to_main, bg="#cccccc", fg="black", width=20).grid(row=3, column=0, columnspan=2, pady=5)

    def confirm_add_bill(self):
        """Confirms and adds the new bill to the system."""
        user_id = self.user_id_entry.get()
        try:
            amount = float(self.amount_entry.get())
            self.system.add_bill(user_id, amount)
            messagebox.showinfo("Bill Added", f"New bill of amount ${amount} added for User ID: {user_id}.")
            self.create_main_frame()  # Go back to the main page
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")

    def back_to_main(self):
        """Navigates back to the main menu."""
        self.create_main_frame()  # Go back to the main page

    def upload_payment_page(self):
        """Page for an employee to upload payment details for a user."""
        self.clear_frame()  # Clear current frame

        self.upload_frame = tk.Frame(self.root, bg="#e6f7ff", bd=2, relief="ridge")
        self.upload_frame.pack(fill="both", expand=True, padx=10, pady=10)

        label_font = ("Helvetica", 12, "bold")
        tk.Label(self.upload_frame, text="User ID:", font=label_font, bg="#e6f7ff").grid(row=0, column=0, pady=5, padx=10, sticky="e")
        self.user_id_upload_entry = tk.Entry(self.upload_frame, width=25)
        self.user_id_upload_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.upload_frame, text="Payment Details:", font=label_font, bg="#e6f7ff").grid(row=1, column=0, pady=5, padx=10, sticky="e")
        self.payment_details_entry = tk.Entry(self.upload_frame, width=25)
        self.payment_details_entry.grid(row=1, column=1, pady=5)

        # Payment delay options
        self.payment_option_var = tk.StringVar()

        tk.Button(self.upload_frame, text="Pay Now", command=self.pay_now, bg="#66b3ff", fg="white", width=20).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.upload_frame, text="Delay for 10 Days", command=self.delay_10_days, bg="#ff9900", fg="white", width=20).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.upload_frame, text="Delay for 20 Days", command=self.delay_20_days, bg="#ff9900", fg="white", width=20).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self.upload_frame, text="Delay for 30 Days", command=self.delay_30_days, bg="#ff9900", fg="white", width=20).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.upload_frame, text="Back", command=self.back_to_main, bg="#cccccc", fg="black", width=20).grid(row=6, column=0, columnspan=2, pady=5)

    def pay_now(self):
        """Handles immediate payment and updates the bill status."""
        user_id = self.user_id_upload_entry.get()
        payment_details = self.payment_details_entry.get()
        
        if user_id and payment_details:
            payment_amount = self.system.get_total_amount_due(user_id)  # Get total amount due
            if payment_amount > 0:
                # Enable the payment details and update payment status
                self.system.update_payment_status(user_id, 0, payment_details, payment_amount, "Paid")
                messagebox.showinfo("Payment Successful", f"Payment of ${payment_amount} has been successfully processed.")
                self.create_main_frame()  # Go back to the main page
            else:
                messagebox.showerror("No Dues", "There are no unpaid bills for this user.")
        else:
            messagebox.showerror("Missing Information", "Please enter payment details.")

    def delay_10_days(self):
        """Handles delayed payment for 10 days."""
        self.delay_payment(10)

    def delay_20_days(self):
        """Handles delayed payment for 20 days."""
        self.delay_payment(20)

    def delay_30_days(self):
        """Handles delayed payment for 30 days."""
        self.delay_payment(30)

    def delay_payment(self, days):
        """Handles delayed payment and updates the status with additional charges."""  
        user_id = self.user_id_upload_entry.get()
        
        if user_id:
            payment_amount = self.system.get_total_amount_due(user_id)
            if payment_amount > 0:
                # Update bill status to 'Unpaid' and delay the payment (ensure no payment details)
                self.system.delay_payment(user_id, 0, days)
                messagebox.showinfo("Payment Delayed", f"Payment delayed by {days} days.")
                self.create_main_frame()  # Go back to the main page
            else:
                messagebox.showerror("No Dues", "There are no unpaid bills for this user.")
        else:
            messagebox.showerror("Missing Information", "Please enter a valid User ID.")

    def view_bill_history_page(self):
        """View bill history of a user."""
        self.clear_frame()

        self.history_frame = tk.Frame(self.root, bg="#e6f7ff", bd=2, relief="ridge")
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=10)

        label_font = ("Helvetica", 12, "bold")
        tk.Label(self.history_frame, text="Enter User ID:", font=label_font, bg="#e6f7ff").grid(row=0, column=0, pady=5, padx=10, sticky="e")
        self.user_id_history_entry = tk.Entry(self.history_frame, width=25)
        self.user_id_history_entry.grid(row=0, column=1, pady=5)

        tk.Button(self.history_frame, text="Show History", command=self.show_bill_history, bg="#66b3ff", fg="white", width=20).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(self.history_frame, text="Back", command=self.back_to_main, bg="#cccccc", fg="black", width=20).grid(row=2, column=0, columnspan=2, pady=5)

    def show_bill_history(self):
        """Displays the bill history for the user."""
        user_id = self.user_id_history_entry.get()
        bills = self.system.get_bill_history(user_id)

        if bills:
            history_window = tk.Toplevel(self.root)
            history_window.title("Bill History")

            for i, bill in enumerate(bills):
                status = bill["status"]
                total_amount = bill["total_amount"]
                tk.Label(history_window, text=f"Bill {i + 1}: Status: {status}, Total Amount: ${total_amount}", font=("Helvetica", 12)).pack(pady=5)
        else:
            messagebox.showerror("No History", "No bills found for this user.")


    def view_amount_due_page(self):
        """View total amount due of a user."""
        self.clear_frame()

        self.due_frame = tk.Frame(self.root, bg="#e6f7ff", bd=2, relief="ridge")
        self.due_frame.pack(fill="both", expand=True, padx=10, pady=10)

        label_font = ("Helvetica", 12, "bold")
        tk.Label(self.due_frame, text="Enter User ID:", font=label_font, bg="#e6f7ff").grid(row=0, column=0, pady=5, padx=10, sticky="e")
        self.user_id_due_entry = tk.Entry(self.due_frame, width=25)
        self.user_id_due_entry.grid(row=0, column=1, pady=5)

        tk.Button(self.due_frame, text="Show Amount Due", command=self.show_amount_due, bg="#66b3ff", fg="white", width=20).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(self.due_frame, text="Back", command=self.back_to_main, bg="#cccccc", fg="black", width=20).grid(row=2, column=0, columnspan=2, pady=5)

    def show_amount_due(self):
        """Displays the total amount due for a user."""
        user_id = self.user_id_due_entry.get()
        total_due = self.system.get_total_amount_due(user_id)

        if total_due > 0:
            messagebox.showinfo("Total Amount Due", f"Total amount due for user {user_id}: ${total_due}")
        else:
            messagebox.showinfo("No Dues", "There are no dues for this user.")


if __name__ == "__main__":
    system = ElectricityBillSystem()
    root = tk.Tk()
    app = BillApp(root, system)
    root.mainloop()