
import random
is_admin = False

#-----Bank_Logins-----
def login_menu():
    while True:    
        try:
            print("\n------LOGIN MENU------")
            print("1.Admin login.")
            print("2.User Login.")
            print("3. Exit")
            

            choice = input("Enter your Choice (1-3): ")
            if choice == "1" :
                Logins()

            elif choice == "2" :
                Logins()
                
            
            elif choice == "3" :
                print("Exiting... Thank you!","come again!")
                break
    
            else: 
                print("Invalid choice. Please select a number between 1 and 4.")  
    
        except ValueError:
            print("Invalid Number....Please Enter the correct number")


        


#-------Logins-------
def Logins():
    admin_name="unicom"
    admin_password="123"

    name=input("Enter your Name:")
    password=input("Enter your Password:")
    if name==admin_name and password==admin_password:
        print("login successful!")
        is_admin = True
        MENU()
    else:
        print("login failed")
    
#------UASER_DETAILS------
user_details = {}
#------USER APPLICATION------
def user_details_get():
    user_name = input("Enter your NAME")
    user_nic = int(input("Enter your NIC"))
    user_address = input("Enter your ADDRESS")
    user_age = int(input("Enter your AGE"))
    user_tp_no = int(input("Enter your TP-NO"))

    user_details



#------Banking Application------
account = {}
import random

# Save account details to file
def save_accounts():
    with open("account.txt", "a") as file:
        file.write(f"{account_number} \t")
        file.write(f"{name} \t")
        file.write(f"{intial_balance} /t")
        file.write(f"Account created with balance:{intial_balance} /t")
        file.write("\n")

def generate_account_number():
    while True:
        account_number = str(random.randint(0000,9999))
        while account_number not in account:
            return account_number


#------Created Accounts-------
def created_account():   
    name = input("Enter your Name: ")
    while True:
        try:
            intial_balance = float(input("Enter your intial_balance(must be non-negative):"))
            if intial_balance < 0:
                raise ValueError
            break
        except ValueError:
            print("invalid amount.please enter a non-negative number")
    account_number = generate_account_number()
   

    account[account_number] = {"name":name,"balance":intial_balance,"transactions":[f'Account created with balance:{intial_balance}']}
    print(f'Account created successfully. Account number:{account_number}')

 #------Deposit Money------
def deposit_money():
    acc_num = input("Enter account number")
    if acc_num not in account:
        print("Acconunt does not exist.")
        return
    try:
        amount = float(input("Enter deposit amount: "))
        if amount < 0:
            raise ValueError
        account[acc_num]['balance'] += amount
        account[acc_num]["transactions"].append(f"Deposited:{amount}")
        save_accounts()
        print("Deposit successful")
    except ValueError:
        print("Invalid deposit number.")

#-------Withdraw Money-------
def withdraw_money():
    acc_num = input("Enter account number")
    if acc_num not in account:
        print("Acconunt does not exist.")
        return
    try:
        amount = int(input("Enter Withdraw amount: "))
        if amount < 0 and amount >  account[acc_num]['balance']:
            raise ValueError
        account[acc_num]['balance'] -= amount
        account[acc_num]["transactions"].append(f"Withdrew:{amount}")
        save_accounts()
        print("Withdrawal successful.")
    except ValueError:
        print("Invalid Withdrawal number.")

#------Check Balance------
def check_balance():
    acc_num = input("Enter account number")
    if acc_num in account:
        print(f"Current Balance: {account[acc_num]['balance']}")
    else:
        print("Account does not exist.")

#------Transaction History------
def transactions_history():
    acc_num = input("Enter account number")
    if acc_num in account:
        print("Transaction History")
        for transactions in account[acc_num]['transactions']:
            print(transactions)
    else:
        print("Account does not exist.")






#-----Bank Menu-----

def MENU():
 while True:    
    try:
        print("\n====== USER ACCOUNT MENU ======") 
        print("0. Create Account") 
        print("1. Deposit Money") 
        print("2. Withdraw Money") 
        print("3. Check Balance") 
        print("4. Money Transaction") 
        print("5. Transaction History") 
        print("6. Change Password") 
        print("7. Exit")

        choice = input("Enter your Choice (0-7): ")
        if choice == "0" :
            if is_admin :
                created_account()
            else:
                print("User can't access.!")

        elif choice == "1" :
            deposit_money()

        elif choice == "2" :
            withdraw_money()

        elif choice == "3" :
            check_balance()

        # elif choice == "4" :
        #     transactions_history()

        elif choice == "5" :
            transactions_history()

        # elif choice == "6" :
        #     transactions_history()

        elif choice == "7" :
            print("Exiting... Thank you!","come again!")
            break
    
        else: 
            print("Invalid choice. Please select a number between 1 and 4.")  
    
    except ValueError:
        print("Invalid Number....Please Enter the correct number")

    
Logins()
# Call the function


        


