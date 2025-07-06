'''Module for interacting with the mysql database'''

from mysqlconnector import connect_db
from validators import InvalidEmailError, validate_email

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
    if result == None:
        print(result)
    else:
        print(f"ID: {result[0]}. {result[1]} by {result[2]}. ISBN: {result[3]}")
    connection.close()
    my_cursor.close()

def view_books():
    print("List of Books")
    sql1 = "SELECT COUNT(*) FROM books;"
    sql = "SELECT * FROM Books"
    connection = connect_db()
    my_cursor = connection.cursor()
    my_cursor.execute(sql)
    results = my_cursor.fetchall()
    my_cursor.execute(sql1)
    count = my_cursor.fetchone()
    print(f"Total Number of Books: {count[0]}")

    if not results:
        print("There's no book recorded yet")
        return
    print("----List of Books----")
    print(f"{'Id':<6} | {'Title':<20} | {'Author':<50} | {'ISBN':<20}")
    for i in results:
        print(f"{i[0]:<6} | {i[1]:<20} | {i[2]:<50} | {i[3]:<20}")
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
    email = str(input("Enter user's Email: "))
    try:
        validate_email(email)
    except InvalidEmailError as err:
        print(f"Error: {err}")
        return
    sql = f"UPDATE users SET status = 'admin' WHERE email = '{email}'"
    connection = connect_db()
    my_cursor = connection.cursor()
    my_cursor.execute(sql)
    print("User is now an admin")
    connection.commit()
    connection.close()
    my_cursor.close()

def revoke_admin():
    email = str(input("Enter admin's Email: "))
    try:
        validate_email(email)
    except InvalidEmailError as err:
        print(f"Error: {err}")
        return
    sql = f"UPDATE users SET status = 'user' WHERE email = '{email}'"
    connection = connect_db()
    my_cursor = connection.cursor()
    my_cursor.execute(sql)
    print("Admin access successfully revoked")
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
    print(f"{'First Name':<20} | {'Last Name':<20} | {'Email':<50} | {'Role':<10} | {'Registered Date':<30}")
    for i in results:
        print(f"{i[0]:<20} | {i[1]:<20} | {i[2]:<50} | {i[3]:<10} | {i[4]}")
    connection.close()
    my_cursor.close() 