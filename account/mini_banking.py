import random

is_admin = False

account = {}

# ----- Bank Logins -----
#test-commit
def login_menu():
    while True:
        print("\n------LOGIN MENU------")
        print("1. Admin login")
        print("2. User Login")
        print("3. Exit")

        choice = input("Enter your Choice (1-3): ")
        if choice == "1":
            login(admin=True)
        elif choice == "2":
            login(admin=False)
        elif choice == "3":
            print("Exiting... Thank you! Come again!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 3.")

# ----- Logins -----
def login(admin):
    global is_admin
    if admin:
        name = input("Enter Admin Name: ")
        password = input("Enter Admin Password: ")
        if name == "unicom" and password == "123":
            print("Admin Login successful!")
            is_admin = True
            MENU()
        else:
            print("Admin login failed.")
    else:
        name = input("Enter your User_name: ")
        password = input("Enter your Password: ")
        try:
            with open("customers.txt", "r") as f:
                for line in f:
                    _, u_name, u_pass = line.strip().split(",")
                    if name == u_name and password == u_pass:
                        print("User Login successful!")
                        is_admin = False
                        MENU()
                        return
                print("User login failed.")
        except FileNotFoundError:
            print("No users found. Please contact admin.")

# ----- Customer Detail Input -----
def customer_details_get():
    customer_name = input("Enter your NAME: ")
    customer_nic = input("Enter your NIC: ")
    customer_address = input("Enter your ADDRESS: ")
    customer_age = input("Enter your AGE: ")
    customer_tp_no = input("Enter your TP-NO: ")
    user_name = input("Set your User_name: ")
    user_password = input("Set your Password: ")

    return [customer_name, customer_nic, customer_address, customer_age, customer_tp_no, user_name, user_password]

def create_customer_next_id():
    try:
        with open("customers.txt", "r") as f:
            lines = f.readlines()
            if lines:
                last_id = int(lines[-1].split(",")[0][1:])
            else:
                last_id = 0
    except FileNotFoundError:
        last_id = 0
    return f"C{last_id + 1:03}"

def generate_account_number():
    while True:
        acc_number = str(random.randint(1000, 9999))
        if acc_number not in account:
            return acc_number

def save_accounts(customer_id, customer_info, acc_number):
    with open("account.txt", "a") as account_file, open("customers.txt", "a") as customers_file:
        account_file.write(f"{acc_number},   {customer_id},   {customer_info[0]},   {customer_info[1]},   {customer_info[2]},   {customer_info[3]},   {customer_info[4]}\n")
        customers_file.write(f"{acc_number},   {customer_id},   {customer_info[5]},   {customer_info[6]}\n")

# ------ Create Account ------
def created_account():
    customer_info = customer_details_get()

    while True:
        try:
            initial_balance = float(input("Enter your initial balance (non-negative): "))
            if initial_balance < 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid amount. Must be non-negative.")

    customer_id = create_customer_next_id()
    account_number = generate_account_number()

    account[account_number] = (
        "customer_id" == customer_id,
        "balance" == initial_balance,
        "transactions" == [f"Initial deposit: {initial_balance}"]
    )

    save_accounts(customer_id, customer_info, account_number)
    print(f"Account created successfully. Account number: {account_number}, Customer ID: {customer_id}")

# ------ Deposit Money ------
def deposit_money():
    acc_num = input("Enter account number: ")
    if acc_num not in account:
        print("Account does not exist.")
        return
    try:
        amount = float(input("Enter deposit amount: "))
        if amount < 0:
            raise ValueError
        account[acc_num]['balance'] += amount
        account[acc_num]['transactions'].append(f"Deposited: {amount}")
        print("Deposit successful.")
    except ValueError:
        print("Invalid deposit amount.")

# ------ Withdraw Money ------
def withdraw_money():
    acc_num = input("Enter account number: ")
    if acc_num not in account:
        print("Account does not exist.")
        return
    try:
        amount = float(input("Enter withdraw amount: "))
        if amount < 0 or amount > account[acc_num]['balance']:
            raise ValueError
        account[acc_num]['balance'] -= amount
        account[acc_num]['transactions'].append(f"Withdrew: {amount}")
        print("Withdrawal successful.")
    except ValueError:
        print("Invalid amount or insufficient funds.")

# ------ Check Balance ------
def check_balance():
    acc_num = input("Enter account number: ")
    if acc_num in account:
        print(f"Current Balance: {account[acc_num]['balance']}")
    else:
        print("Account does not exist.")

# ------ Money Transfer ------
def transfer_money():
    sender = input("Enter sender account number: ")
    receiver = input("Enter receiver account number: ")

    if sender not in account or receiver not in account:
        print("One or both accounts do not exist.")
        return

    try:
        amount = float(input("Enter amount to transfer: "))
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if account[sender]['balance'] < amount:
            raise ValueError("Insufficient funds.")

        account[sender]['balance'] -= amount
        account[receiver]['balance'] += amount

        account[sender]['transactions'].append(f"Transferred {amount} to {receiver}")
        account[receiver]['transactions'].append(f"Received {amount} from {sender}")

        print("Transfer successful.")
    except ValueError as e:
        print(f"Error: {e}")

# ------ Transaction History ------
def transactions_history():
    acc_num = input("Enter account number: ")
    if acc_num in account:
        print("Transaction History:")
        for txn in account[acc_num]['transactions']:
            print(txn)
    else:
        print("Account does not exist.")

# ------ Main Menu ------
def MENU():
    while True:
        print("\n====== BANK ACCOUNT MENU ======")
        if is_admin:
            print("0. Create Account")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Transfer Money")
        print("5. Transaction History")
        print("6. Exit")

        choice = input("Enter your Choice (0-6): ")
        if choice == "0":
            if is_admin:
                created_account()
            else:
                print("Only admin can create accounts.")
        elif choice == "1":
            deposit_money()
        elif choice == "2":
            withdraw_money()
        elif choice == "3":
            check_balance()
        elif choice == "4":
            transfer_money()
        elif choice == "5":
            transactions_history()
        elif choice == "6":
            print("Exiting... Thank you! Come again!")
            break
        else:
            print("Invalid choice. Please select a number between 0 and 6.")

# Start Program
login_menu()

