'''Connects to and perform mysql CRUD operations'''

import mysql.connector
from dotenv import load_dotenv
import os
from validators import InvalidEmailError, validate_email

# Load environment variables from .env file
load_dotenv()

def connect_db():
    """Connect to the MySQL database using environment variables."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        # print("Database connection successful")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def add_book():
    title = str(input("Enter book title: ")).title().strip()
    author = str(input("Enter the author: ")).title().strip()
    isbn = str(input("Enter the ISBN: ")).title().strip()
    sql = "INSERT INTO Books (title, author, isbn) VALUES (%s, %s, %s)"
    val = (title, author, isbn)

    connection = connect_db()
    my_cursor = connection.cursor()
    my_cursor.execute(sql, val)
    connection.commit()
    print(my_cursor.rowcount, "record(s) inserted")
    connection.close()
    my_cursor.close()

def search_book():
    title = str(input("Enter book title: ")).title().strip()
    sql = f"SELECT * FROM Books WHERE title = '{title}'"
    # val = (title)

    connection = connect_db()
    my_cursor = connection.cursor()
    my_cursor.execute(sql)
    result = my_cursor.fetchone()
    print(result)
    connection.close()
    my_cursor.close()

def view_books():
    print("List of Books")
    sql = "SELECT * FROM Books"
    connection = connect_db()
    my_cursor = connection.cursor()
    my_cursor.execute(sql)
    results = my_cursor.fetchall()
    for result in results:
        print(result)
    connection.close()
    my_cursor.close()

def delete_book():
    print("--- Deleting books---")
    id = str(input("Entet ID of book to be deleted"))
    sql = f"DELETE FROM Books WHERE id = '{id}'"
    connection = connect_db()
    my_cursor = connection.cursor()
    my_cursor.execute(sql)
    connection.commit()
    print(my_cursor.rowcount, "record(s) deleted")
    connection.close()
    my_cursor.close()

def assign_admin():
    email = str(input("Enter your Email: "))
    try:
        validate_email(email)
    except InvalidEmailError as err:
        print(f"Error: {err}")
        return
    sql = f"UPDATE users SET status = 'admin' WHERE email = '{email}'"
    connection = connect_db()
    my_cursor = connection.cursor()
    my_cursor.execute(sql)
    connection.commit()
    connection.close()
    my_cursor.close()

def view_users():
    print("List of Books")
    sql1 = "SELECT status, COUNT(*) AS UserCount FROM users GROUP BY status ORDER BY status;"
    sql = "SELECT FirstName, LastName, email, status, created_at FROM Users"
    connection = connect_db()
    my_cursor = connection.cursor()
    my_cursor.execute(sql)
    results = my_cursor.fetchall()
    my_cursor.execute(sql1)
    count = my_cursor.fetchall()

    print("----Total Number of Users----")
    print(f"{'Role':<10} | {'Count':<10}")
    for i in count:
        print(f"{i[0]:<10} | {i[1]:<10}")

    print("----List of Users----")
    print(f"{'First Name':<20} | {'Last Name':<20} | {'Email':<50} | {'Status':<10} | {'Registered Date':<30}")
    for i in results:
        print(f"{i[0]:<20} | {i[1]:<20} | {i[2]:<50} | {i[3]:<10} | {i[4]:<30}")
    connection.close()
    my_cursor.close()