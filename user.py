'''Module for users Authentication and Authorization'''

import hashlib
from mysqlconnector import connect_db
from datetime import datetime
from validators import InvalidEmailError, validate_email
from library import view_books, add_book, search_book, delete_book, assign_admin, view_users, revoke_admin
from menu import menu

def hash_password(password:str) -> str:
    return hashlib.sha224(password.encode('utf-8')).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    if hash_password(password) == hashed:
        return True

def sign_up():
    connection = connect_db()
    user_cursor = connection.cursor()
    print("Create an account")
    try:
        firstname = str(input("Enter your first name: ")).title().strip()
        lastname = str(input("Enter your last name: ")).title().strip()
        email = str(input("Enter your email: ")).strip()
        validate_email(email)
    except InvalidEmailError as err:
        print(f"Error: Invalid Email")
    except Exception as err:
        print(f"Error: Invalid Email")
        return True
    else:
        password = str(input("Enter your password: "))
        confirm_password = str(input("Confirm password: "))
        if not password == confirm_password:
            print("Oooops! Password mismatch!")
            return True
        hash = hash_password(password)
        role = "user"
        created_at = datetime.now()
        sql1 = "SELECT email FROM users"
        user_cursor.execute(sql1)
        user_email = user_cursor.fetchall()
        for i in user_email:
            if i[0] == email:
                # print(i)
                print("Email already exists!")
                return
        
        sql = "INSERT INTO users (firstname, lastname, email, role, password_hash, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (firstname, lastname, email, role, hash, created_at)
        
        user_cursor.execute(sql, val)
        connection.commit()
        print("Account created successfully!")
        connection.close()
        user_cursor.close()


def login():
    print("Login to your account")
    email = str(input("Enter your Email: "))
    try:
        validate_email(email)
    except InvalidEmailError:
        print(f"Error: Invalid Email")
        return
    password = str(input("Enter your password: "))
    sql = f"SELECT password_hash FROM users WHERE email = '{email}'"
    connection = connect_db()
    user_cursor = connection.cursor()
    user_cursor.execute(sql)
    hashed = user_cursor.fetchone()

    if hashed == None or not verify_password(password, hashed[0]):
        print("Invalid Email or Password")
    else:
        print("login successfully")
        user_dashboard(email)
        return
    connection.close()
    user_cursor.close()


def user_dashboard(email):
    sql = f"SELECT role, FirstName FROM users WHERE email = '{email}'"
    connection = connect_db()
    user_cursor = connection.cursor()
    user_cursor.execute(sql)
    user = user_cursor.fetchone()
    if user[0].lower().strip() == "user":
        while True:
            menu(f"---Welcome  {user[1]}!---", ["View books", "search book", "logout"])
            choice = int(input("Enter option: "))
            if choice == 1:
                view_books()
            elif choice == 2:
                search_book()
            elif choice == 3:
                print("Logging out...")
                break
            else:
                print("Invalid Input")
        
    elif user[0].lower().strip() == "admin":
        while True:
            menu(f"---Welcome {user[1]}!---", ["View books", "search book", "add book", "delete book", "assign admin", "revoke admin", "view users", "logout"])
            choice = int(input("Enter option: "))
            if choice == 1:
                view_books()
            elif choice == 2:
                search_book()
            elif choice == 3:
                add_book()
            elif choice == 4:
                delete_book()
            elif choice == 5:
                assign_admin()
            elif choice == 6:
                revoke_admin()
            elif choice == 7:
                view_users()
            elif choice == 8:
                print("logging out...")
                break
            else:
                print("Invalid Input")
    else:
        print("Invalid User")
    connection.close()
    user_cursor.close()
    return


def view_profile():
    pass

# def user_profile:


    


