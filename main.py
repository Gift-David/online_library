from user import login, sign_up
from menu import menu

def main():
    while True:
        menu("---Welcome to Your Online Library---", ["login", "sign up", "exit"])
        choice = int(input("Select an option: "))
        if choice == 1:
            login()
        elif choice == 2:
            sign_up()
        elif choice == 3:
            print("Exiting your online library!")
            break
        else:
            print("Invalid option")
    return

if __name__ == "__main__":
    main()
