import sqlite3

def setup_database():
    """Set up the database and create the accounts table if it doesn't exist."""
    connection = sqlite3.connect("bank.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0.0
        )
    """)
    connection.commit()
    connection.close()

def add_account(name, initial_amount):
    """Add a new account with the specified name and initial amount."""
    connection = sqlite3.connect("bank.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, initial_amount))
    connection.commit()
    account_number = cursor.lastrowid
    connection.close()
    print(f"Account created! Your account number is {account_number}.")

def make_deposit(account_number, amount):
    """Deposit money into an account."""
    connection = sqlite3.connect("bank.db")
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
    result = cursor.fetchone()
    if result:
        new_balance = result[0] + amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, account_number))
        connection.commit()
        print(f"Deposited {amount:.2f}. New balance is {new_balance:.2f}.")
    else:
        print("Account not found.")
    connection.close()

def make_withdrawal(account_number, amount):
    """Withdraw money from an account."""
    connection = sqlite3.connect("bank.db")
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
    result = cursor.fetchone()
    if result:
        if result[0] >= amount:
            new_balance = result[0] - amount
            cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, account_number))
            connection.commit()
            print(f"Withdrew {amount:.2f}. New balance is {new_balance:.2f}.")
        else:
            print("Not enough funds.")
    else:
        print("Account not found.")
    connection.close()

def view_balance(account_number):
    """Check the balance of an account."""
    connection = sqlite3.connect("bank.db")
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
    result = cursor.fetchone()
    connection.close()
    if result:
        print(f"Current balance: {result[0]:.2f}")
    else:
        print("Account not found.")

def main():
    setup_database()
    while True:
        print("\nBank Management System")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter your name: ")
            initial_amount = float(input("Enter initial deposit amount: "))
            add_account(name, initial_amount)
        elif choice == "2":
            account_number = int(input("Enter account number: "))
            amount = float(input("Enter deposit amount: "))
            make_deposit(account_number, amount)
        elif choice == "3":
            account_number = int(input("Enter account number: "))
            amount = float(input("Enter withdrawal amount: "))
            make_withdrawal(account_number, amount)
        elif choice == "4":
            account_number = int(input("Enter account number: "))
            view_balance(account_number)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()