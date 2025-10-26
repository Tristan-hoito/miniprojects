import json
import os
import re
from datetime import datetime

DATA_FILE = "data.json"

# --- Helper Functions ---
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}, "transactions": {}}
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
    # Ensure required keys exist (for backward compatibility)
    if "users" not in data:
        data["users"] = {}
    if "transactions" not in data:
        data["transactions"] = {}
    return data

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def is_valid_email(email):
    return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))

def is_valid_password(password):
    # Must contain at least one lowercase, one uppercase, and one number, no special characters
    return bool(re.fullmatch(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z0-9]+", password))

# --- Core Features ---
def sign_up(data):
    clear_terminal()
    print("=== SIGN UP ===")
    confirm = input("Do you really want to sign up? (y/n): ").lower()
    if confirm != "y":
        print("Returning to main menu...")
        input("Press Enter to continue...")
        return

    email = input("Enter your email: ").strip()
    if not is_valid_email(email):
        print("❌ Invalid email format!")
        input("Press Enter to continue...")
        return

    username = input("Enter username: ").strip()
    if username in data["users"]:
        print("❌ Username already exists.")
        input("Press Enter to continue...")
        return

    while True:
        password = input("Enter password (must include A–Z, a–z, and 0–9 only): ").strip()
        if not is_valid_password(password):
            print("❌ Password must have at least one uppercase, one lowercase, one digit, and no special characters.")
            continue
        confirm_pass = input("Confirm password: ").strip()
        if password != confirm_pass:
            print("❌ Passwords do not match!")
            continue
        break

    verify = input("Are you sure you want to create this account? (y/n): ").lower()
    if verify != "y":
        print("Cancelled registration.")
        input("Press Enter to continue...")
        return

    data["users"][username] = {"email": email, "password": password}
    data["transactions"][username] = []  # This should now work with the fixed load_data()
    save_data(data)
    print("✅ Account created successfully!")
    input("Press Enter to return to main menu...")

def login(data):
    clear_terminal()
    print("=== LOGIN ===")
    confirm = input("Do you really want to log in? (y/n): ").lower()
    if confirm != "y":
        print("Returning to main menu...")
        input("Press Enter to continue...")
        return None

    username = input("Enter username: ").strip()
    if username not in data["users"]:
        print("❌ Username not found.")
        input("Press Enter to continue...")
        return None

    email = input("Enter registered email: ").strip()
    if email != data["users"][username]["email"]:
        print("❌ Incorrect email.")
        input("Press Enter to continue...")
        return None

    password = input("Enter password: ").strip()
    if password != data["users"][username]["password"]:
        print("❌ Incorrect password.")
        input("Press Enter to continue...")
        return None

    verify = input("Are you sure you want to continue logging in? (y/n): ").lower()
    if verify != "y":
        print("Login cancelled.")
        input("Press Enter to continue...")
        return None

    print("✅ Login successful!")
    input("Press Enter to continue...")
    return username

def add_record(data, username):
    clear_terminal()
    print("=== ADD RECORD ===")
    confirm = input("Do you really want to add a record? (y/n): ").lower()
    if confirm != "y":
        print("Returning to main menu...")
        input("Press Enter to continue...")
        return

    # Validate date with option for today
    while True:
        use_today = input("Use today's date? (y/n): ").lower().strip()
        if use_today == "y":
            date = datetime.now().strftime("%Y-%m-%d")
            break
        elif use_today == "n":
            date = input("Enter date (YYYY-MM-DD): ").strip()
            if not date:
                print("❌ Date cannot be empty.")
                continue
            try:
                datetime.strptime(date, "%Y-%m-%d")  # Check format
                break
            except ValueError:
                print("❌ Invalid date format. Use YYYY-MM-DD (e.g., 2023-10-15).")
        else:
            print("❌ Please enter 'y' or 'n'.")

    # Validate type with menu for ease
    while True:
        print("Select type:")
        print("1. Expense")
        print("2. Income")
        type_choice = input("Choose (1 or 2): ").strip()
        if type_choice == "1":
            type_ = "Expense"
            break
        elif type_choice == "2":
            type_ = "Income"
            break
        else:
            print("❌ Invalid choice. Enter 1 for Expense or 2 for Income.")

    # Validate amount
    while True:
        amount_input = input("Enter amount: ").strip()
        if not amount_input:
            print("❌ Amount cannot be empty. Please enter a valid number.")
            continue
        try:
            amount = float(amount_input)
            if amount <= 0:
                print("❌ Amount must be a positive number greater than 0.")
                continue
            break  # Valid input, exit loop
        except ValueError:
            print("❌ Invalid amount. Please enter a valid number (e.g., 100.50).")

    category = input("Enter category: ").strip()
    desc = input("Add description? (y/n): ").lower().strip()
    description = input("Enter description: ").strip() if desc == "y" else "N/A"

    transaction = {
        "id": len(data["transactions"][username]) + 1,
        "date": date,
        "type": type_,
        "amount": amount,
        "category": category,
        "description": description,
        "timestamp": datetime.now().isoformat()
    }

    data["transactions"][username].append(transaction)
    save_data(data)
    print("✅ Record added successfully!")
    input("Press Enter to return to main menu...")

def view_history(data, username):
    clear_terminal()
    print("=== VIEW HISTORY ===")

    transactions = data["transactions"][username]
    if not transactions:
        print("No transactions found.")
        input("Press Enter to return to main menu...")
        return

    choice = input("View all (a) or recent (r)? ").lower().strip()
    if choice == "a":
        to_show = transactions
    else:
        while True:
            num_input = input("How many recent transactions? ").strip()
            if not num_input:
                print("❌ Number cannot be empty.")
                continue
            try:
                num = int(num_input)
                if num <= 0:
                    print("❌ Number must be a positive integer.")
                    continue
                break
            except ValueError:
                print("❌ Invalid number. Please enter a positive integer.")
        to_show = transactions[-num:] if num < len(transactions) else transactions

    order = input("Ascending or Descending (a/d): ").lower().strip()
    to_show = sorted(to_show, key=lambda x: x["date"], reverse=(order == "d"))

    for t in to_show:
        print(f"\n[{t['id']}] {t['date']} | {t['type']} | ₱{t['amount']} | {t['category']} | {t['description']}")

    input("\nPress Enter to return to main menu...")

def edit_record(data, username):
    clear_terminal()
    print("=== EDIT RECORD ===")

    transactions = data["transactions"][username]
    if not transactions:
        print("No transactions found.")
        input("Press Enter to return to main menu...")
        return

    year = input("Enter year (YYYY): ").strip()
    month = input("Enter month (MM): ").strip()
    day = input("Enter day (DD): ").strip()

    filtered = [t for t in transactions if t["date"].startswith(f"{year}-{month}-{day}")]
    if not filtered:
        print("No transactions found for that date.")
        input("Press Enter to continue...")
        return

    for t in filtered:
        print(f"[{t['id']}] {t['date']} | {t['type']} | ₱{t['amount']} | {t['category']} | {t['description']}")

    tid_input = input("Enter transaction ID to edit: ").strip()
    if not tid_input:
        print("❌ ID cannot be empty.")
        input("Press Enter to continue...")
        return
    try:
        tid = int(tid_input)
    except ValueError:
        print("❌ Invalid ID. Must be a number.")
        input("Press Enter to continue...")
        return

    for t in transactions:
        if t["id"] == tid:
            print("\nWhat do you want to edit?")
            print("1. Type\n2. Amount\n3. Category\n4. Description")
            choice = input("Choose: ").strip()

            if choice == "1":
                while True:
                    print("Select new type:")
                    print("1. Expense")
                    print("2. Income")
                    new_choice = input("Choose (1 or 2): ").strip()
                    if new_choice == "1":
                        t["type"] = "Expense"
                        break
                    elif new_choice == "2":
                        t["type"] = "Income"
                        break
                    else:
                        print("❌ Invalid choice. Enter 1 or 2.")
            elif choice == "2":
                while True:
                    amount_input = input("New amount: ").strip()
                    if not amount_input:
                        print("❌ Amount cannot be empty.")
                        continue
                    try:
                        new_amount = float(amount_input)
                        if new_amount <= 0:
                            print("❌ Amount must be positive.")
                            continue
                        t["amount"] = new_amount
                        break
                    except ValueError:
                        print("❌ Invalid amount. Enter a number.")
            elif choice == "3":
                t["category"] = input("New category: ").strip()
            elif choice == "4":
                t["description"] = input("New description: ").strip()
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")
                return

            confirm = input("Save changes? (y/n): ").lower().strip()
            if confirm == "y":
                save_data(data)
                print("✅ Record updated successfully!")
            else:
                print("Changes discarded.")
            break
    else:
        print("Transaction not found.")

    input("Press Enter to return to main menu...")

def dashboard(data, username):
    while True:
        clear_terminal()
        print(f"=== DASHBOARD ({username}) ===")
        print("1. Add Record")
        print("2. View History")
        print("3. Edit Record")
        print("4. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_record(data, username)
        elif choice == "2":
            view_history(data, username)
        elif choice == "3":
            edit_record(data, username)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
            input("Press Enter to continue...")

def main():
    data = load_data()
    while True:
        clear_terminal()
        print("=== EXPENSE & SAVINGS TRACKER ===")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            sign_up(data)
        elif choice == "2":
            user = login(data)
            if user:
                dashboard(data, user)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
