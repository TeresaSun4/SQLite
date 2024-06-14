#Teresa Sun - Database Application

#Import
import sqlite3
import datetime
#Database
DATABASE = '/Users/teresa/sqlite/music.dp'

#Database and Table
def init_db():
    #Create a customer table
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers(
            customer_id TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT
        )
    ''')
    #Create a CD table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CD(
            cd_id INTEGER PRIMARY KEY,
            cd_name TEXT,
            cd_type TEXT,
            cd_quantity INTEGER,
            cd_artist TEXT,
            cd_released_Year INTEGER
        )
    ''')
    #Create a uses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrow(
            borrow_number INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            CD_id INTEGER,
            borrow_date TEXT,
            return_date TEXT,
            Location TEXT,
            pre_order TEXT,
            overtime_payment REAL,
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY(cd_id) REFERENCES CD(cd_id)
        )
    ''')
    conn.commit()
    conn.close()

#Add CD data
def add_initial_cd_data():
    #List of CD data
    cd_data = [
        (1, 'Seventeenth Heaven', 'kpop', 56, 'Seventeen', 2023),
        (2, 'FML', 'kpop', 23, 'Seventeen', 2023),
        (3, '17 Carat', 'kpop', 65, 'Seventeen', 2024),
        (4, 'Face the Sun', 'kpop', 34, 'Seventeen', 2020),
        (5, '17 Is Right Here', 'kpop', 64, 'Seventeen', 2019),
        (6, '5-Star', 'kpop', 43, 'Stray Kids', 2022),
        (7, 'Rock-Star', 'kpop', 64, 'Stray Kids', 2022),
        (8, 'ODDINARY', 'kpop', 24, 'Stray Kids', 2021),
        (9, 'Mixtape', 'kpop', 12, 'Stray Kids', 2018),
        (10, 'The Sound', 'kpop', 54, 'Stray Kids', 2017),
        (11, 'XOXO', 'kpop', 76, 'EXO', 2014),
        (12, 'The War', 'kpop', 45, 'EXO', 2017),
        (13, 'Don\'t Fight the Feeling', 'kpop', 35, 'EXO', 2016),
        (14, 'OBSESSION', 'kpop', 98, 'EXO', 2015)
    ]
    #Connect to sqLite databse
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql="INSERT INTO CD (cd_id, cd_name, cd_types, cd_quantity, cd_artist, cd_released_year) VALUES (?, ?, ?, ?, ?, ?);"
    db.commit()
    #Close connection
    db.close()

#New user
def add_user(customer_id, first_name, last_name, email):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        #Add a new user to the customer table if they don't have an id yet
        c.execute('INSERT INTO customers (customer_id, first_name, last_name, email) VALUES (?, ?, ?, ?);',
                  (customer_id, first_name, last_name, email))
        conn.commit()
        print("Customer added successfully.")
    except sqlite3.IntegrityError:
        print("Customer with this ID already exists.")
    #Close connection
    conn.close()

#Authrnticate a user from their email and user_id
def authenticate_user(customer_id,email):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    #Check does the uer have already got an email
    cursor.execute('SELECT * FROM customers WHERE customer_id=? AND email=?',(customer_id,email))
    user = c.fetchone()
    conn.close()
    return user is not None

#Borrow Cds
def borrow_cd(cd_id, customer_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT cd_quantity FROM CD WHERE cd_id=?', (cd_id,))
    result = c.fetchone()
    if result is None:
        print("CD does not exists.")
    elif result[0] == 0:
        print("CD is not available.")
    else:
        borrow_date = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor.execute('UPDATE CD SET cd_quantity = cd_quantity-1 WHERE cd_id=?',(cd_id))
        cursor.execute('INSERT INTO borrow (customer_id, CD_id, borrow_date, location) VALUES (?, ?, ?, ?);',
                  (customer_id,cd_id,borrow_date,'kpop'))
        conn.commit()
        print("CD borrowed successfully.")
    #Close connection
    conn.close()

#Return CDs
def return_cd(borrow_number):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT cd_id, borrow_date FROM borrow WHERE borrow_number=?', (borrow_number,))
    result = c.fetchone()
    if result is None:
        print("Borrow record does not exist.")
    else:
        cd_id, borrow_date = result[0], datetime.datetime.strptime(result[1], "%Y-%m-%d")
        return_date = datetime.datetime.now().strftime("%Y-%m-%d")
        #Calculate the overdue payment
        overdue_days = (datetime.datetime.now() - borrow_date).days - 14
        overdue_payment = max(0, overdue_days * 1.0)
        #Record the time
        cursor.execute('UPDATE CD SET cd_quantity=cd_quantity+1 WHERE cd_id=?', (cd_id,))
        cursor.execute('UPDATE borrow SET return_date=?, overtime_payment=? WHERE borrow_number=?', 
                   (return_date, overdue_payment, borrow_number))
        conn.commit()
        print("CD returned successfully.")
        if overdue_payment >0:
            print(f"Overdue fee: ${overdue_payment: .2f}")
        #Close connection
        conn.close()

#List all the CDs        
def list_all_CD():
    conn = sqlite3.connect('cd.dp.db')
    cursor = conn.cursor()
    cursor.execute('SELEXT cd_id, cd_name, cd_quantity FROM CD')
    CDs = cursor.fetchall()
    if not CDs:
        print("No CDs found.")
    else:
        print("Available CDs:")
        for cd_id, cd_name, cd_quantity in CDs:
            status = "Available" if cd_quantity > 0 else "Out of stock"
            print(f"ID: {cd_id}, Title:{cd_name}, Status:{status}")
    #Close connection
    conn.close()
   

#Run the actual CD_borrow program
def main():
    init_db()
    add_initial_cd_data()
    customer_id = None

    #Menu
    while True:
        print("\nOptions:") #Option
        print("1. Register") #Register a new user
        print("2. Login") #Login to this program
        print("3. Borrow CD") #Borrow avaliable CDs
        print("4. Return CD") #Return a borrowed CD
        print("5. List All CDs") #List all the avaliable CDs
        print("0. Exit") #Logout the program
        user_option= input("Choose an option: ")
        if user_option== '1':
            customer_id = input("Enter customer ID: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            add_user(customer_id, first_name, last_name, email)
        elif user_option=='2':
            customer_id = input("Enter customerID: ")
            email = input("Enter email: ")
            if authenticate_user(customer_id, email):
                print("Login successful.")
            else:
                print("Invalid ID or email.")
                customer_id = None
        elif user_option=='3':
            if customer_id:
                cd_id = input("Enter CD ID: ")
                borrow_cd(cd_id, customer_id)
            else:
                print("Please log in first.")
        elif user_option== '4':
            if customer_id:
                borrow_number = input("Enter borrow number: ")
                return_cd(borrow_number)
            else:
                print("Please log in first.")
        elif user_option== '5':
            list_all_CD()
        elif user_option== '0':
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()




        
