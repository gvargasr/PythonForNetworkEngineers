import getpass

device_ip = input("Enter the device ip: ")
username = input("Enter username: ")
# password = getpass.getpass("Password: ")

password_is_too_short = True

while password_is_too_short:
    password = getpass.getpass("Enter password at least 5 characters: ")
    if len(password) >= 5:
        password_is_too_short = False
    else:
        print("Password entered is too short")
# print(f"Your password entered is: {password}")


print(f"Device ip: {device_ip}")
print(f"username: {username}")
print(f"password: {password}")
