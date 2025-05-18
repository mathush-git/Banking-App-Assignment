import random
import re
import datetime


is_admin = False

account = {}

# ----- Bank Logins -----

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
        name = input("Enter your User_name: ").strip()
        password = input("Enter your Password: ").strip()

        try:
            with open("customers.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) != 4:
                        continue  
                    acc_number, customer_id, u_name, u_pass = [p.strip() for p in parts]
                    if name == u_name and password == u_pass:
                        print("User Login successful!")
                        is_admin = False
                        load_accounts()
                        MENU()  
                        break
                else:
                    print("User login failed.")

        except FileNotFoundError:
            print("No users found. Please contact admin.")

#------------Customers Details------------
def customer_details():
    while True:
        print("\n------CUSTOMER DETAILS MENU------")
        print("1. Display Customer")
        print("2. Display Customer Details")
        print("3. Exit")

        choice = input("Enter your Choice (1-3): ")
        if choice == "1":
            display_customer()
        elif choice == "2":
            display_customer_Details()
        elif choice == "3":
            print("Exiting... Thank you! Come again!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 3.")
            
def validate_nic(nic):
    # If the NIC contains 'x' or 'v', its total length must be 10.
    if 'x' in nic or 'v' in nic:
        if len(nic) == 10 and bool(re.match(r'^[0-9]{9}[xv]$', nic)):
            return True
        else:
            print("Invalid NIC")
            return False
    # Otherwise, the NIC must have exactly 12 digits.
    elif len(nic) == 12 and bool(re.match(r'^[0-9]{12}$', nic)):
        return True
    else:
        print("Invalid NIC please Enter correct number")
        return False
    
# ----- Customer Detail Input -----
def customer_details_get():
    customer_name = input("Enter your CUSTOMER NAME: ")
    customer_nic = input("Enter your CUSTOMER NIC: ")
    customer_address = input("Enter your CUSTOMER ADDRESS: ")
    customer_age = input("Enter your CUSTOMER AGE: ")
    customer_tp_no = input("Enter your CUSTOMER TP-NO: ")
    u_name = input("Set your CUSTOMER USER_NAME: ")
    while True:
        u_password = input("Set your CUSTOMER PASSWORD: ")
        if len(u_password) == 6:
            print("Correct Password")
            break
        else:
            print("ReEnter the pasword")
            continue
    nic_validated =  validate_nic(customer_nic)
    if nic_validated:
        return [customer_name, customer_nic, customer_address, customer_age, customer_tp_no, u_name, u_password]
    

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

#------- Save All Account------
def save_all_accounts():
    with open("acc_num.txt", "a") as f:
        for acc_number, acc_data in account.items():
            customer_id = acc_data["customer_id"]
            balance = acc_data["balance"]
            transactions = "|".join(acc_data["transactions"])  
            f.write(f"{acc_number}, {customer_id}, {balance}, {transactions}\n")
 
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

    account[account_number] = {
        "customer_id" : customer_id,
        "balance" : initial_balance,
        "transactions" : [f"Initial deposit: {initial_balance}"]
    }

    save_accounts(customer_id, customer_info, account_number)
    save_all_accounts()  

    print(f"Account created successfully. Account number: {account_number}, Customer ID: {customer_id}")

#-------Display Customer List-------
def display_customer():
    try:
        with open("account.txt","r")as f:
            lines = f.readlines()
            if not lines:
                print("No Customers")
                return
            for line in lines:
                parts = line.strip().split(",")
                print(f"{parts[0]}:{parts[1]}:{parts[2]}")
    except FileNotFoundError:
        print("Customer data not available.")

def display_customer_Details():
    try:
        with open("account.txt","r")as f:
            lines = f.readlines()
            if not lines:
                print("No Customers Details")
                return
            for line in lines:
                parts = line.strip().split(",")
                print(f"{parts[0]}:{parts[1]}:{parts[2]}:{parts[3]}:{parts[4]}:{parts[5]}:{parts[6]}")
    except FileNotFoundError:
        print("Customer data not available.")


#-------Load_Accounts-------
def load_accounts():
    try:
        with open("acc_num.txt", "r") as f:
            for line in f:
                parts = [p.strip() for p in line.strip().split(",")]
                if len(parts) >= 4:
                    acc_number = parts[0]
                    customer_id = parts[1]
                    balance = float(parts[2])
                    transactions = parts[3].split("|") if parts[3] else []
                    account[acc_number] = {
                        "customer_id": customer_id,
                        "balance": balance,
                        "transactions": transactions
                    }
    except FileNotFoundError:
        pass


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
        now = datetime.datetime.now()
        account[acc_num]['balance'] += amount
        account[acc_num]['transactions'].append(f"{now} - Deposited: {amount}")
        save_all_accounts()
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
        now = datetime.datetime.now()
        account[acc_num]['balance'] -= amount
        account[acc_num]['transactions'].append(f"{now} - Withdrew: {amount}")
        save_all_accounts()
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
    
    sender = input("Enter sender account number: ").strip()
    receiver = input("Enter receiver account number: ").strip()

    # Check if accounts exist
    if sender not in account:
        print("Sender account does not exist.")
        return
    if receiver not in account:
        print("Receiver account does not exist.")
        return

    try:
        amount = float(input("Enter amount to transfer: "))
        
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if account[sender]['balance'] < amount:
            raise ValueError("Insufficient funds.")

        now = datetime.datetime.now()
        
        account[sender]['balance'] -= amount
        account[receiver]['balance'] += amount

        
        account[sender]['transactions'].append(f"{now} - Transferred ${amount:.2f} to {receiver}")
        account[receiver]['transactions'].append(f"{now} - Received ${amount:.2f} from {sender}")
        save_all_accounts()
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
            print("1. Customer Details Menu")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transfer Money")
        print("6. Transaction History")
        print("7. Exit")

        if is_admin:
            choice = input("Enter your Choice (0-7): ")
        else:
            choice = input("Enter your Choice (2-7): ")
        if choice == "0":
            if is_admin:
                created_account()
            else:
                print("Only admin can create accounts.")
        if choice == "1":
            if is_admin:
                customer_details()
            else:
                print("Only admin can display accounts.")
        elif choice == "2":
            deposit_money()
        elif choice == "3":
            withdraw_money()
        elif choice == "4":
            check_balance()
        elif choice == "5":
            transfer_money()
        elif choice == "6":
            transactions_history()
        elif choice == "7":
            print("Exiting... Thank you! Come again!")
            break
        else:
            print("Invalid choice. Please select a number between 0 and 6.")

# Start Program
login_menu()