import bcrypt
import re

def hash_password(password):
    #encode password to byte
    pass_bytes = password.encode('utf-8')
    #generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pass_bytes, salt)
    #decode the hash back to a string to store it in a text file
    return hashed_password.decode('utf-8')

def verify_pass(password, hashed_password):
    #encode both password and hashed password to byte
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    #using bcrypt.checkpw() to verify the password
    return bcrypt.checkpw(password_bytes, hashed_bytes)

#registering user
def register(username, password):
    with open("users.txt", "r") as f:
        for line in f:
            stored_user = line.strip().split(',', 1)[0]
            if stored_user == username:
                print(f"Username '{username}' already exists. Please choose a different one.")
                return

    hashed_password = hash_password(password)
    #making a file and writing the username and pass into it
    with open("users.txt","a") as f:
        f.write(f"{username},{hashed_password}\n")
        print(f"user {username} registered successfully")

#user login
def login(username, password):
    with open("users.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line or ',' not in line:
                continue
            parts = line.split(',', 1)
            if len(parts) != 2:
                continue
            user, hash = parts
            if user == username:
                return verify_pass(password, hash)
    return False

def validate_username(username):
    if len(username) < 3 or len(username) > 20:
        return False,"username must be between 3 and 20 characters"
    if not re.match("^[A-Za-z0-9_]+$",username):
        return False,"username must contain only letters, numbers and underscores"

    return True,""

#validating password
def validate_pass(password):
    if len(password) < 8:
        return False,"password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return False,"password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False,"password must contain at-least one lowercase letter"
    if not re.search(r"\d", password):
        return False,"password must contain at least one digit"
    if not re.search(r"[!@#$%^&*]", password):
        return False,"password must contain at least one special character"
    return True,""

#main menu
def display_menu():
    print("\n"+"="*50)
    print("MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("secure authentication system")
    print("="*50)
    print("\n[1] Register a User")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    print("\nWelcome to week 7 Authentication system")

    while True:
        display_menu()
        choice = input("Enter your choice (1-3): ").strip()

        #registering a user
        if choice == "1":
            print("\n--- USER REGISTRATION ---")

            # validating user name
            username = input("Enter Username: ").strip()
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f'Error: {error_msg}')
                continue

            # validating password
            password = input("Enter Password: ").strip()
            is_valid, error_msg = validate_pass(password)
            if not is_valid:
                print(f'Error: {error_msg}')
                continue

            #confirm password
            pass_confirm = input("Confirm Password: ").strip()
            if pass_confirm != password:
                print("Error:Passwords do not match")
                continue

            #register user
            register(username, password)
            input("Press enter to return to main menu")

        #login
        elif choice == "2":
            print("\n--- LOGIN ---")
            username = input("Enter Username: ").strip()
            password = input("Enter Password: ").strip()

            #login attempt
            if login(username, password):
                print("Login Successful")
            else:
                print("Error:Invalid username or password")
            input("Press enter to return to main menu")

        #exit
        elif choice == "3":
            print("\nThank you for using user authentication system")
            print("Exiting..")
            break

        else:
            print("Error:Invalid choice choose an option from the main menu")

if __name__ == "__main__":
    main()






