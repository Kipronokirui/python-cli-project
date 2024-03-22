from project import User, Transaction
import sqlite3

CONN = sqlite3.connect('project.db')
cursor = CONN.cursor()

# create the tables
def tablecreation():
    print("Tables Creation has started")
    User.createTable(cursor, CONN)
    print("User Table Creation finished")
    print("Transactions Table Creation has started")
    Transaction.createTable(cursor, CONN)
    print("Transactions Table Creation finished")

def getAllUsers():
    arrayData = User.queryAll(cursor, CONN)
    for user in arrayData:
        print(f'''
    Name: {user[1]}
    Phone Number: {user[2]}
    Account Balance: {user[3]}
    ***************
        ''')

def createUser():
    while True:
        name = input('Name: ')
        phoneNumber = input('Phone Number: ')

        cursor.execute("SELECT COUNT(*) FROM user WHERE phoneNumber = ?", (phoneNumber,))
        user_count = cursor.fetchone()[0]

        if user_count == 0:
            newUser = User(name, phoneNumber, 0.0)
            newUser.save(cursor, CONN)
            print('User created successfully')
            break
        else:
            print("User with that phone number already exists.")
            return

def sendMoney():
    sender = input("Enter Sender`s Phone Number: ")
    
    # Check if sender phone number exist in the User table
    cursor.execute("SELECT COUNT(*) FROM user WHERE phoneNumber = ?", (sender,))
    sender_count = cursor.fetchone()[0]
    if sender_count == 0:
        print(f"Sender phone number '{sender}' does not exist in the database.")
        return
    
    receiver = input("Enter Receiver`s Phone Number: ")

    # Check if receiver phone number exist in the User table
    cursor.execute("SELECT COUNT(*) FROM user WHERE phoneNumber = ?", (receiver,))
    receiver_count = cursor.fetchone()[0]

    if receiver_count == 0:
        print(f"Receiver phone number '{receiver}' does not exist in the database.")
        return
    
    if sender == receiver:
        print("You cannot send money to yourself")
        return
    
    amount = int(input("Enter the amount to send: "))
    
    # Checking Sender Account balance 
    sender_balance = User.check_balance(cursor, CONN, sender)
    print(f"Sender Account balance is: {sender_balance}")
    if amount < sender_balance:
        User.complete_send_money(cursor, CONN, sender, receiver, amount)
        transaction = Transaction(sender, receiver, amount)
        transaction.save(cursor, CONN)
    else:
        print("The account balance is insufficient to complete this transaction")

    
def getAllTransactions():
    arrayData = Transaction.queryAll(cursor, CONN)
    for transaction in arrayData:
        print(f'''
            Sender: {transaction[1]}
            Receiver: {transaction[2]}
            Amount: {transaction[3]}
            *************
        ''')

def getAllUserTransactions():
    yourNumber = input("Enter Your Phone Number: ")
    arrayData = Transaction.user_transactions(yourNumber, cursor, CONN)
    print("Below is a list of your transactions")
    for transaction in arrayData:
        print(f'''
            Sender: {transaction[1]}
            Receiver: {transaction[2]}
            Amount: {transaction[3]}
            *************
        ''')

def checkBalance():
    accountPhoneNumber = input("Enter Your Phone Number: ")
    
    balance = User.check_balance(cursor, CONN, accountPhoneNumber)
    print(f"Your balance is: {balance}")
    if balance is not None:
        print(f"The account balance for phone number {accountPhoneNumber} is: {balance}")
    else:
        print(f"No user found with the phone number {accountPhoneNumber}") 
        
def depositMoney():
    accountPhoneNumber = input("Enter Your Phone Number: ")
    amount = input("Enter the amount to deposit: ")

    balance = User.check_balance(cursor, CONN, accountPhoneNumber)
    if balance is not None:
        user = User("", accountPhoneNumber, balance)
        user.deposit(amount, cursor, CONN)
    else:
        print(f"No user found with the phone number {accountPhoneNumber}")

def main():

    selectOption = input('Option >> ')

    if selectOption == '0':
        exit()
    elif selectOption == '1':
        getAllUsers()
        print("All Users Listed")
        # pass
    elif selectOption == '2':
        getAllTransactions()
        # pass 
    elif selectOption == '3':
        sendMoney()
        # pass 
    elif selectOption == '4':
        createUser() 
    elif selectOption == '5':
        checkBalance()
        # pass 
    elif selectOption == '6':
        getAllUserTransactions()
        # pass 
    elif selectOption == '7':
        depositMoney()
        # pass 
    else:
        print('Invalid Option')

    main()


if __name__ == '__main__':
    # create tables if not created
    tablecreation()

    options = '''
0 - Exit Program
1 - List all Users
2 - List all Transactions
3 - Send Money
4 - Register New User
5 - Check Account Balance
6 - List all your transactions
7 - Deposit money
'''
    print(options)

    main()








