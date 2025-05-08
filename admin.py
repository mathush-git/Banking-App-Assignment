import random

is_admin = False


# ----- Bank Logins -----
def login_menu():
    while True:
        try:
            print("\n------LOGIN MENU------")
            print("1. Admin login")
            print("2. User Login")
            print("3. Exit")

            choice = input("Enter your Choice (1-3): ")
            if choice == "1":
                Logins()
            elif choice == "2":
                Logins()
            elif choice == "3":
                print("Exiting... Thank you! Come again!")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 3.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

# ------- Logins -------
def Logins():
    global is_admin
    admin_name = "unicom"
    admin_password = "123"

    
    User_name = customer_details_get("user_name")
    User_password = customer_details_get("user_password")

    name=input("Enter your Name:")
    password=input("Enter your Password:")

    if name == admin_name and password == admin_password:
        print("Admin Login successful!")
        is_admin = True
        MENU()
        
    elif name == User_name  and password == User_password:
        print("User Login successful!")
        MENU()
    else:
        print("Login failed")

# ------ User Details ------
user_details = {}

def customer_details_get():
    customer_name = input("Enter your NAME: ")
    customer_nic = input("Enter your NIC: ")
    customer_address = input("Enter your ADDRESS: ")
    customer_age = input("Enter your AGE: ")
    customer_tp_no = input("Enter your TP-NO: ")
    user_name = input("Enter your User_name: ")
    user_password = input("Enter your Password: ")

    return [customer_name,    customer_nic,    customer_address,    customer_age,    customer_tp_no,    user_name,    user_password]

def create_customer_next_id():
    try:
        with open("customers.txt", "r") as customers_file:
            lines = customers_file.readlines()
            if lines:
                last_id = int(lines[-1].split(",")[0][1:])
            else:
                last_id = 0
    except FileNotFoundError:
        last_id = 0  

    return f"C{last_id + 1:03}"  

# ------ Banking Application ------
account = {}

# Save account details to file
def save_accounts(customer_id, customer_info):
    with open("account.txt", "a") as account_file, open("customers.txt", "a") as customers_file, open("acc_num.txt", "a") as acc_num_file:
        account_file.write(f"{customer_id},{customer_info[0]},{customer_info[1]},{customer_info[2]},{customer_info[3]},{customer_info[4]}\n")
        customers_file.write(f"{customer_id},{customer_info[5]},{customer_info[6]}\n")
        acc_num_file.write(f"{account_number},{customer_id}\n")

def generate_account_number():
    while True:
        account_number = str(random.randint(1000, 9999))
        if account_number not in account:
            return account_number

# ------ Create Account ------
def created_account():
    customer_info = customer_details_get()

    while True:
        try:
            initial_balance = float(input("Enter your initial balance (must be non-negative): "))
            if initial_balance < 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid amount. Please enter a non-negative number.")

    customer_id = create_customer_next_id()
    account_number = generate_account_number()

    account[account_number] = {"customer_id": customer_id, "balance": initial_balance}
    save_accounts(customer_id, customer_info)

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

# ------- Withdraw Money -------
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
        print("Invalid withdraw amount or insufficient funds.")

# ------ Check Balance ------
def check_balance():
    acc_num = input("Enter account number: ")
    if acc_num in account:
        print(f"Current Balance: {account[acc_num]['balance']}")
    else:
        print("Account does not exist.")

# -------Money Transaction-------
def transfer_money():
    senter = input("Enter senter account number: ")
    receiver = input("Enter receiver account number: ")

    if senter not in account or receiver not in account:
        print("One or both accounts do not exist.")
        return
    
    try:
        amount = float(input("Enter amount to Transfer"))
        if amount <= 0:
            raise ValueError ("Amount must be positive")
        if account[senter]['balance'] < amount:
            raise ValueError("Insufficient Funds.")

    #------Perfom the Transfer------
        account[senter]['balance'] -= amount
        account[receiver]['balance'] += amount

    #------Record Transaction------
        account[senter]['transactions'].append(f"transferred {amount} to {receiver}")
        account[receiver]['Transactions'].append(f"received {amount} to {senter}")

        save_accounts() #Optional:presist datd to file 
        print("Transfer successful.")

    except ValueError as e:
        print("Error: ", e)

# ------ Transaction History ------
def transactions_history():
    acc_num = input("Enter account number: ")
    if acc_num in account:
        print("Transaction History:")
        for txn in account[acc_num]['transactions']:
            print(txn)
    else:
        print("Account does not exist.")

# ----- Bank Menu -----

def MENU():
    while True:
        try:
            print("\n====== BANK ACCOUNT MENU ======")
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
                print("Invalid choice. Please select a number between 0 and 5.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

# ----- Start Program -----
login_menu()
