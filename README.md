
# Electricity Bill Payment System ⚡💡

Welcome to the **Electricity Bill Payment System**! This Python-based application helps users manage their electricity bills. Built with **Tkinter**, it provides a user-friendly interface for adding bills, processing payments, and tracking dues. 🧾💰

## Features 🔑
- **Bill Management** 📝: Add new bills, view bill history, and track unpaid dues for each user.
- **Payment Processing** 💳: Upload payment details and mark bills as paid.
- **Delay Handling** ⏳: Delay payments and apply additional charges based on the delay (2% for 10 days, 5% for 20 days, 10% for 30 days).
- **Amount Due** 💵: View the total amount due, including any overdue charges.
- **User-Friendly Interface** 👩‍💻: Easy-to-use interface built with **Tkinter**.
- **Error Handling** 🚫: Provides error messages when incorrect or missing data is entered.

## How It Works ⚙️
- **Generate User ID** 🆔: Each user gets a unique ID using `uuid`.
- **Add Bill** 💸: Add new bills for users, specifying the amount.
- **Pay Bill** 💳: Upload payment details and mark bills as paid.
- **Delayed Payment** ⏰: Delay the payment by 10, 20, or 30 days, with an automatic surcharge applied.
- **View History** 📜: View the history of bills and payment statuses for each user.

## Installation 🛠️
Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/Electricity-Bill-Payment-System.git
```

Then, run the application:

```bash
python bill_payment_system.py
```

## Requirements 📦
- Python 3.x
- Tkinter (comes with Python by default)

## License 📝
This project is licensed under the MIT License.
