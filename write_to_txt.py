# --------------------Ejemplo 1--------------------------

# data = 'Switch1 is located in San Jose'

# with open('switch.txt', 'w') as file:
#     file.write(data)

# --------------------Ejemplo 2--------------------------

# data = 'Switch2 is located in Chicago'

# with open('switch.txt', 'a') as f:
#     f.write(data)

# --------------------Ejemplo 3--------------------------

# data = 'Switch2 is located in Chicago'

# with open('switch.txt', 'a') as f:
#     f.write('\n')
#     f.write(data)

# --------------------Ejemplo 4--------------------------

data = ["Switch3 is located in Miami", "\n" "Switch4 is located in London"]

with open("switch.txt", "w") as f:
    f.writelines(data)

    