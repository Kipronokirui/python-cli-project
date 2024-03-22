class User:
    def __init__(self, name, phoneNumber, accountBalance):
        self.id = None
        self.name = name
        self.phoneNumber = phoneNumber
        self.accountBalance = round(float(accountBalance), 2)

    @classmethod
    def createTable(cls, cursor, CONN):
        query = """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            phoneNumber VARCHAR(15) UNIQUE,
            accountBalance DECIMAL(10, 2) DEFAULT 0.00
        )
        """
        cursor.execute(query)
        CONN.commit()

    def save(self, cursor, CONN):
        query = f"""
            INSERT INTO user(name, phoneNumber, accountBalance)
                        VALUES('{self.name}', '{self.phoneNumber}', '{self.accountBalance}')
        """
        cursor.execute(query)
        CONN.commit()

        self.id = cursor.lastrowid

    @classmethod
    def queryAll(cls, cursor, CONN):
        query = '''
        SELECT * FROM user
        '''
        cursor.execute(query)
        return cursor.fetchall()
    
    @classmethod
    def check_balance(cls, cursor, CONN, accountPhoneNumber):
        query = f'''
        SELECT accountBalance FROM user WHERE phoneNumber = ?
        '''
        cursor.execute(query, (accountPhoneNumber,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None  

    @classmethod
    def complete_send_money(cls, cursor, CONN, sender_number, receiver_number, amount_transacted):
        sender_query = f'''
        SELECT accountBalance FROM user WHERE phoneNumber = ?
        '''
        cursor.execute(sender_query, (sender_number,))
        result = cursor.fetchone()
        sender_account_balance = result[0]
        new_sender_account_balance = sender_account_balance - amount_transacted 

        # Update the Sender balance in the database
        saving_sender_query = f"""
            UPDATE user
            SET accountBalance = ?
            WHERE phoneNumber = ?
        """
        cursor.execute(saving_sender_query, (new_sender_account_balance, sender_number))
        CONN.commit()

        #  Handling Receiving Account 
        receiver_query = f'''
        SELECT accountBalance FROM user WHERE phoneNumber = ?
        '''
        cursor.execute(receiver_query, (receiver_number,))
        result = cursor.fetchone()
        receiver_account_balance = result[0]
        new_receiver_account_balance = receiver_account_balance + amount_transacted 

        # Update the Receiver account balance in the database
        saving_receiver_query = f"""
            UPDATE user
            SET accountBalance = ?
            WHERE phoneNumber = ?
        """
        cursor.execute(saving_receiver_query, (new_receiver_account_balance, receiver_number))
        CONN.commit()
        print("Transaction completed succesfully")
        # return result
    
    def deposit(self, amount, cursor, CONN):
        # Ensure amount is positive
        amount = max(0, round(float(amount), 2))
        
        # Update the account balance
        self.accountBalance += amount

        # Update the balance in the database
        query = f"""
            UPDATE user
            SET accountBalance = {self.accountBalance}
            WHERE phoneNumber = '{self.phoneNumber}'
        """
        cursor.execute(query)
        CONN.commit()

        print(f"Deposited {amount} into account for {self.phoneNumber}. New balance: {self.accountBalance}")

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.id = None
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    @classmethod
    def createTable(cls, cursor, CONN):
        query = """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender INT,
                receiver INT,
                amount INT
            )
        """
        cursor.execute(query)
        CONN.commit()

    def save(self, cursor, CONN):
        query = f"""
            INSERT INTO transactions (sender, receiver, amount)
                        VALUES({self.sender}, {self.receiver}, {self.amount})
        """
        cursor.execute(query)
        CONN.commit()

        self.id = cursor.lastrowid

    @classmethod
    def queryAll(cls, cursor, CONN):
        query = '''
        SELECT * FROM transactions
        '''
        cursor.execute(query)
        return cursor.fetchall()
    
    @classmethod
    def user_transactions(cls, entredPhoneNumber, cursor, CONN):
        query = f'''
            SELECT * FROM transactions
            WHERE sender = ? OR receiver = ?
        '''
        cursor.execute(query, (entredPhoneNumber, entredPhoneNumber)) 
        transactions = cursor.fetchall()
        return transactions