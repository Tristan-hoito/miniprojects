import json
import os
import re
from datetime import datetime

DATA_FILE = "data.json"

# Simple color helpers (works on most terminals, no external deps)
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    GRAY = "\033[90m"
    WHITE = "\033[37m"


def color(text, *styles):
    if not styles:
        return text
    return "".join(styles) + str(text) + C.RESET

# --- Helper Functions ---
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")
    # On Windows cmd, enable ANSI if possible (best-effort)
    try:
        if os.name == "nt":
            os.system("")
    except Exception:
        pass

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}, "transactions": {}}
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
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
    print(color("Sign Up", C.BOLD))
    print(color("----------------", C.BOLD))
    print(color("Create a new user account.", C.DIM))
    print()
    confirm = input("Do you really want to sign up? (y/n): ").lower()
    if confirm != "y":
        print("Returning to main menu...")
        input("Press Enter to continue...")
        return

    email = input("Enter your email: ").strip()
    if not is_valid_email(email):
        print(color("❌ Invalid email format!", C.RED, C.BOLD))
        input("Press Enter to continue...")
        return

    username = input("Enter username: ").strip()
    if username in data["users"]:
        print(color("❌ Username already exists.", C.RED, C.BOLD))
        input("Press Enter to continue...")
        return

    while True:
        password = input("Enter password (must include A–Z, a–z, and 0–9 only): ").strip()
        if not is_valid_password(password):
            print(color("❌ Password must have at least one uppercase, one lowercase, one digit, and no special characters.", C.YELLOW))
            continue
        confirm_pass = input("Confirm password: ").strip()
        if password != confirm_pass:
            print(color("❌ Passwords do not match!", C.RED))
            continue
        break

    data["users"][username] = {"email": email, "password": password}
    data["transactions"][username] = []  # This should now work with the fixed load_data()
    save_data(data)
    print(color("✅ Account created successfully!", C.GREEN, C.BOLD))
    input("Press Enter to return to main menu...")

def login(data):
    clear_terminal()
    print(color("Login", C.BOLD))
    print(color("----------------", C.BOLD))
    print(color("Log in to your existing account.", C.DIM))
    print()
    confirm = input("Do you really want to log in? (y/n): ").lower()
    if confirm != "y":
        print("Returning to main menu...")
        input("Press Enter to continue...")
        return None

    print(color("\nCredentials", C.BOLD))
    user_input = input("Enter username or email: ").strip()
    username = None
    if is_valid_email(user_input):
        # Find username by email
        for u, info in data["users"].items():
            if info["email"] == user_input:
                username = u
                break
        if not username:
            print("❌ Email not found.")
            input("Press Enter to continue...")
            return None
    else:
        username = user_input
        if username not in data["users"]:
            print("❌ Username not found.")
            input("Press Enter to continue...")
            return None

    password = input("Enter password: ").strip()
    if password != data["users"][username]["password"]:
        print(color("❌ Incorrect password.", C.RED))
        input("Press Enter to continue...")
        return None

    print(color("✅ Login successful!", C.GREEN, C.BOLD))
    input("Press Enter to continue...")
    return username

def add_record(data, username):
    clear_terminal()
    print(color("Add Record", C.BOLD))
    print(color("----------------", C.BOLD))
    print(color("Add a new expense or income record.", C.DIM))
    print()
    confirm = input("Do you really want to add a record? (y/n): ").lower()
    if confirm != "y":
        print("Returning to main menu...")
        input("Press Enter to continue...")
        return

    clear_terminal()

    # Validate date with option for today
    while True:
        print(color("Date:", C.BOLD))
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
            print(color("❌ Please enter 'y' or 'n'.", C.YELLOW))

    # Validate type with menu for ease
    while True:
        print(color("\nSelect type:", C.BOLD))
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
            print(color("❌ Invalid choice. Enter 1 for Expense or 2 for Income.", C.RED))

    # Validate category based on type
    if type_ == "Expense":
        expense_categories = ["Food & Groceries", "Transportation", "Entertainment", "Personal Needs", "Personal Wants", "Bills", "School/Work"]
        print(color("\nSelect expense category:", C.BOLD))
        for i, cat in enumerate(expense_categories, 1):
            print(f"{i}. {cat}")
        while True:
            cat_choice = input("Choose (1-7): ").strip()
            if cat_choice.isdigit() and 1 <= int(cat_choice) <= 7:
                category = expense_categories[int(cat_choice) - 1]
                break
            else:
                print("❌ Invalid choice. Enter 1-7.")
    else:  # Income
        income_categories = ["Allowance", "Work", "Reward", "Gift"]
        print(color("\nSelect income category:", C.BOLD))
        for i, cat in enumerate(income_categories, 1):
            print(f"{i}. {cat}")
        while True:
            cat_choice = input("Choose (1-4): ").strip()
            if cat_choice.isdigit() and 1 <= int(cat_choice) <= 4:
                category = income_categories[int(cat_choice) - 1]
                break
            else:
                print("❌ Invalid choice. Enter 1-4.")

    # Validate amount
    while True:
        amount_input = input("\nEnter amount: ").strip()
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
    print(color("✅ Record added successfully!", C.GREEN, C.BOLD))
    input("Press Enter to return to main menu...")

def view_history(data, username):
    clear_terminal()
    print(color("View History", C.BOLD))
    print(color("----------------", C.BOLD))
    print(color("View your transaction history.", C.DIM))
    print()

    transactions = data["transactions"][username]
    if not transactions:
        print("No transactions found.")
        input("Press Enter to return to main menu...")
        return

    print(color("Filter options:", C.BOLD))
    print("1. All transactions")
    print("2. By category")
    print("3. By date")
    print("4. By type (Expense/Income)")
    print("5. Recent transactions")
    print("6. By specific date")
    filter_choice = input("Choose filter (1-6): ").strip()

    filtered = transactions

    if filter_choice == "2":
        clear_terminal()
        print(color("Select type:", C.BOLD))
        print("1. Expense")
        print("2. Income")
        type_choice = input("Choose (1 or 2): ").strip()
        if type_choice == "1":
            type_ = "Expense"
            categories = ["Food & Groceries", "Transportation", "Entertainment", "Personal Needs", "Personal Wants", "Bills", "School/Work"]
        elif type_choice == "2":
            type_ = "Income"
            categories = ["Allowance", "Work", "Reward", "Gift"]
        else:
            print("❌ Invalid choice.")
            input("Press Enter to continue...")
            return
        print(color("\nSelect category:", C.BOLD))
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        cat_choice = input(f"Choose (1-{len(categories)}): ").strip()
        if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(categories):
            category = categories[int(cat_choice) - 1]
            filtered = [t for t in transactions if t["category"] == category and t["type"] == type_]
        else:
            print("❌ Invalid choice.")
            input("Press Enter to continue...")
            return
    elif filter_choice == "3":
        clear_terminal()
        print(color("Choose date filter:", C.BOLD))
        print(color("1. By Day (YYYY-MM-DD)", C.WHITE))
        print(color("2. By Month (YYYY-MM)", C.WHITE))
        print(color("3. By Year (YYYY)", C.WHITE))
        group_choice = input("Choose (1-3): ").strip()
        
        def ymd_keys(d):
        # Returns (year, month, day)
            try:
                dt = datetime.strptime(d, "%Y-%m-%d")
                return dt.year, dt.month, dt.day
            except Exception:
                # Fallback if date is malformed
                parts = d.split("-")
                y = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
                m = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
                dd = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
                return y, m, dd
            
        order = input("Ascending or Descending by date (a/d): ").lower().strip()
        filtered = sorted(filtered, key=lambda x: x["date"], reverse=(order == "d"))

        if group_choice == "3":
            # Group by year
            groups = {}
            for t in filtered:
                y, _, _ = ymd_keys(t["date"])
                groups.setdefault(y, []).append(t)
            for y in sorted(groups.keys(), reverse=(order == "d")):
                print(color(f"\n------ {y} ------", C.BOLD))
                income_total = sum(x["amount"] for x in groups[y] if x["type"] == "Income")
                expense_total = sum(x["amount"] for x in groups[y] if x["type"] == "Expense")
                print(f"Total Income: ₱{income_total:.2f} | Total Expense: ₱{expense_total:.2f} | Balance: ₱{income_total - expense_total:.2f}")
                for t in groups[y]:
                    print(f"  [{t['id']}] {t['date']} | {t['type']} | ₱{t['amount']} | {t['category']} | {t['description']}")
        elif group_choice == "2":
            # Group by month (YYYY-MM)
            groups = {}
            for t in filtered:
                y, m, _ = ymd_keys(t["date"])
                key = f"{y:04d}-{m:02d}"
                groups.setdefault(key, []).append(t)
            for key in sorted(groups.keys(), reverse=(order == "d")):
                print(color(f"\n------ {key} ------", C.BOLD))
                income_total = sum(x["amount"] for x in groups[key] if x["type"] == "Income")
                expense_total = sum(x["amount"] for x in groups[key] if x["type"] == "Expense")
                print(f"Total Income: ₱{income_total:.2f} | Total Expense: ₱{expense_total:.2f} | Balance: ₱{income_total - expense_total:.2f}")
                for t in groups[key]:
                    print(f"  [{t['id']}] {t['date']} | {t['type']} | ₱{t['amount']} | {t['category']} | {t['description']}")
        elif group_choice == "1":
            # Group by day (YYYY-MM-DD)
            groups = {}
            for t in filtered:
                key = t["date"]
                groups.setdefault(key, []).append(t)
            for key in sorted(groups.keys(), reverse=(order == "d")):
                print(color(f"\n------ {key} ------", C.BOLD))
                income_total = sum(x["amount"] for x in groups[key] if x["type"] == "Income")
                expense_total = sum(x["amount"] for x in groups[key] if x["type"] == "Expense")
                print(f"Total Income: ₱{income_total:.2f} | Total Expense: ₱{expense_total:.2f} | Balance: ₱{income_total - expense_total:.2f}")
                for t in groups[key]:
                    print(f"  [{t['id']}] {t['date']} | {t['type']} | ₱{t['amount']} | {t['category']} | {t['description']}")
        else:
            # No grouping
            for t in filtered:
                print(color(f"\n[{t['id']}] {t['date']} | {t['type']} | ₱{t['amount']:.2f} | {t['category']} | {t['description']}", C.GRAY))

    elif filter_choice == "4":
        clear_terminal()
        print(color("Select type:", C.BOLD))
        print("1. Expense")
        print("2. Income")
        type_choice = input("Choose (1 or 2): ").strip()
        if type_choice == "1":
            type_ = "Expense"
        elif type_choice == "2":
            type_ = "Income"
        else:
            print("❌ Invalid choice.")
            input("Press Enter to continue...")
            return
        filtered = [t for t in transactions if t["type"] == type_]
    elif filter_choice == "5":
        while True:
            clear_terminal()
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
        filtered = transactions[-num:] if num < len(transactions) else transactions
    elif filter_choice == "6":
        clear_terminal()
        date = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            filtered = [t for t in transactions if t["date"] == date]
        except ValueError:
            print("❌ Invalid date format. Use YYYY-MM-DD.")
            input("Press Enter to continue...")
            return
    elif filter_choice != "1":
        print("❌ Invalid choice.")
        input("Press Enter to continue...")
        return

    if not filtered:
        print("No transactions match the filter.")
        input("Press Enter to return to main menu...")
        return

    # Calculate summary
    total_income = sum(t["amount"] for t in filtered if t["type"] == "Income")
    total_expense = sum(t["amount"] for t in filtered if t["type"] == "Expense")
    balance = total_income - total_expense

    # Display summary
    print(color("\n---------------- Summary ----------------", C.BOLD))
    print(color(f"Total Income: ₱{total_income:.2f}", C.GREEN))
    print(color(f"Total Expenses: ₱{total_expense:.2f}", C.RED))
    bal_color = C.GREEN if balance >= 0 else C.RED
    print(color(f"Total Balance: ₱{balance:.2f}", bal_color, C.BOLD))
    print()

    if filter_choice == "3":
        # For date filter, display grouped as before, but summary is overall
        pass  # Already handled above
    else:
        # Display transactions
        for t in filtered:
            print(color(f"[{t['id']}] {t['date']} | {t['type']} | ₱{t['amount']:.2f} | {t['category']} | {t['description']}", C.GRAY))

    input("\nPress Enter to return to main menu...")

def edit_record(data, username):
    clear_terminal()
    print(color("Edit Record", C.BOLD))
    print(color("----------------", C.BOLD))
    print(color("Edit an existing transaction record.", C.DIM))
    print()

    transactions = data["transactions"][username]
    if not transactions:
        print("No transactions found.")
        input("Press Enter to return to main menu...")
        return

    print(color("Date: ", C.BOLD))
    year = input("Enter year (YYYY): ").strip()
    month = input("Enter month (MM): ").strip()
    day = input("Enter day (DD): ").strip()

    filtered = [t for t in transactions if t["date"].startswith(f"{year}-{month}-{day}")]
    if not filtered:
        print("No transactions found for that date.")
        input("Press Enter to continue...")
        return

    print(color(f"\n--------------- {year}-{month}-{day} ---------------", C.BOLD))
    for t in filtered:
        print(color(f"[{t['id']}] {t['date']} | {t['type']} | ₱{t['amount']:.2f} | {t['category']} | {t['description']}", C.GRAY))

    tid_input = input("\nEnter transaction ID to edit: ").strip()
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
            print(color("\nWhat do you want to edit?", C.BOLD))
            print("1. Type\n2. Amount\n3. Category\n4. Description\n5. Date")
            choice = input("Choose between the options: ").strip()

            if choice == "1":
                while True:
                    clear_terminal()
                    print(color("\nSelect new type:", C.BOLD))
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
                    clear_terminal()
                    amount_input = input(color("New amount: ", C.BOLD)).strip()
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
                # Edit category based on current type
                clear_terminal()
                if t["type"] == "Expense":
                    expense_categories = ["Food & Groceries", "Transportation", "Entertainment", "Personal Needs", "Personal Wants", "Bills", "School/Work"]
                    print(color("Select new expense category:", C.BOLD))
                    for i, cat in enumerate(expense_categories, 1):
                        print(f"{i}. {cat}")
                    while True:
                        cat_choice = input("Choose (1-7): ").strip()
                        if cat_choice.isdigit() and 1 <= int(cat_choice) <= 7:
                            t["category"] = expense_categories[int(cat_choice) - 1]
                            break
                        else:
                            print("❌ Invalid choice. Enter 1-7.")
                else:  # Income
                    income_categories = ["Allowance", "Work", "Reward", "Gift"]
                    print(color("Select new income category:", C.BOLD))
                    for i, cat in enumerate(income_categories, 1):
                        print(f"{i}. {cat}")
                    while True:
                        cat_choice = input("Choose (1-4): ").strip()
                        if cat_choice.isdigit() and 1 <= int(cat_choice) <= 4:
                            t["category"] = income_categories[int(cat_choice) - 1]
                            break
                        else:
                            print("❌ Invalid choice. Enter 1-4.")
            elif choice == "4":
                clear_terminal()
                t["description"] = input(color("New description: ", C.BOLD)).strip()
            elif choice == "5":
                clear_terminal()
                while True:
                    print(color("New Date:", C.BOLD))
                    use_today = input("Use today's date? (y/n): ").lower().strip()
                    if use_today == "y":
                        new_date = datetime.now().strftime("%Y-%m-%d")
                        break
                    elif use_today == "n":
                        new_date = input("Enter date (YYYY-MM-DD): ").strip()
                        if not new_date:
                            print("❌ Date cannot be empty.")
                            continue
                        try:
                            datetime.strptime(new_date, "%Y-%m-%d")  # Check format
                            break
                        except ValueError:
                            print("❌ Invalid date format. Use YYYY-MM-DD (e.g., 2023-10-15).")
                    else:
                        print(color("❌ Please enter 'y' or 'n'.", C.YELLOW))
                t["date"] = new_date
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")
                return

            confirm = input("Save changes? (y/n): ").lower().strip()
            if confirm == "y":
                save_data(data)
                print(color("✅ Record updated successfully!", C.GREEN, C.BOLD))
            else:
                print("Changes discarded.")
            break
    else:
        print("Transaction not found.")

    input("Press Enter to return to main menu...")

def dashboard(data, username):
    while True:
        clear_terminal()
        transactions = data["transactions"][username]
        total_income = sum(t["amount"] for t in transactions if t["type"] == "Income")
        total_expense = sum(t["amount"] for t in transactions if t["type"] == "Expense")
        balance = total_income - total_expense

        # Calculate summaries by category
        income_summary = {}
        expense_summary = {}
        for t in transactions:
            if t["type"] == "Income":
                income_summary[t["category"]] = income_summary.get(t["category"], 0) + t["amount"]
            elif t["type"] == "Expense":
                expense_summary[t["category"]] = expense_summary.get(t["category"], 0) + t["amount"]

        print(color("Dashboard", C.BOLD))
        print(color("----------------", C.BOLD))
        print(color(f"Hello, {username}! Welcome!", C.DIM))
        print(color("Your financial dashboard.\nSummarizes your Money flow!", C.DIM))
        print()

        # Financial Summary Section
        print(color("------ Financial Summary ------", C.BOLD))
        print(color(f"Total Income: ₱{total_income:.2f}", C.GREEN))
        print(color(f"Total Expenses: ₱{total_expense:.2f}", C.RED))
        bal_color = C.GREEN if balance >= 0 else C.RED
        print(color(f"Total Balance: ₱{balance:.2f}", bal_color, C.BOLD))
        print()

        # Income Breakdown Section
        if income_summary:
            print(color("------ Income Breakdown ------", C.BOLD))
            for cat in sorted(income_summary.keys()):
                print(f"  - {cat}: ₱{income_summary[cat]:.2f}")
            print()

        # Expense Breakdown Section
        if expense_summary:
            print(color("------ Expense Breakdown ------", C.BOLD))
            for cat in sorted(expense_summary.keys()):
                print(f"  - {cat}: ₱{expense_summary[cat]:.2f}")
            print()

        # Options Section
        print(color("------ Options ------", C.BOLD))
        print(color("1. Add Record", C.WHITE))
        print(color("2. View History", C.WHITE))
        print(color("3. Edit Record", C.WHITE))
        print(color("4. Logout", C.WHITE))

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
        print(color("Expense & Savings Tracker", C.BOLD))
        print(color("----------------", C.BOLD))
        print(color("Track expenses and income.\nNo more disappearing Money!", C.DIM))
        print()
        print(color("Please choose a function:", C.BOLD))
        print(color("1. Sign Up", C.WHITE))
        print(color("2. Login", C.WHITE))
        print(color("3. Exit", C.WHITE))

        choice = input("Choose an option: ").strip()

        if choice == "1":
            sign_up(data)
        elif choice == "2":
            user = login(data)
            if user:
                dashboard(data, user)
        elif choice == "3":
            print(color("👋 Goodbye! See you next time.", C.GRAY))
            break
        else:
            print("Invalid choice.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
