import csv

# try:
#     with open("data/Address.csv") as file:
#         address_data = csv.reader(file)
#         address_data = list(address_data)
#         print(address_data)
# except FileNotFoundError:
#     print("File was not found or does not exist")
# except PermissionError:
#     print("Permissions required")

# print(
#     f"""
#  __     __     ______     __  __     ______   ______
# /\ \  _ \ \   /\  ___\   /\ \/\ \   /\  == \ /\  ___\
# \ \ \/ ".\ \  \ \ \__ \  \ \ \_\ \  \ \  _-/ \ \___  \
#  \ \__/".~\_\  \ \_____\  \ \_____\  \ \_\    \/\_____\
#   \/_/   \/_/   \/_____/   \/_____/   \/_/     \/_____/
#   """
# )

a = input("Enter your name: ")
if a == "Eric":
    print("Hello Eric")
else:
    print("Hello World")
