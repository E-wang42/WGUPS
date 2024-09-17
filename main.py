# Eric Wang #011777714
# WGUPS ROUTING PROGRAM

import csv
import datetime
from Truck import Truck
from HashTable import HashTable
from Package import Package


# Load CSV data into lists
def load_csv_data(filename):
    """
    Reads a CSV file and returns a list of its contents.
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    with open(filename, mode="r", encoding="utf-8-sig") as file:
        return list(csv.reader(file))


# Create package objects from CSV and load into the hash table
def load_package_data(package_data, package_hash_table):
    """
    Creates Package objects and inserts them into the hash table.
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    for package in package_data:
        pID = int(package[0])
        pAddress = package[1]
        pCity = package[2]
        pState = package[3]
        pZipcode = package[4]
        pDeadline_time = package[5]
        pWeight = package[6]
        pStatus = "At Hub"

        package_obj = Package(
            pID, pAddress, pCity, pState, pZipcode, pDeadline_time, pWeight, pStatus
        )
        package_hash_table.insert(pID, package_obj)


# Calculate the distance between two addresses
def calculate_distance(x_value, y_value, distance_data):
    if x_value is None or y_value is None:
        raise ValueError(f"Invalid address index: x_value={x_value}, y_value={y_value}")

    # print(f"x_value: {x_value}, y_value: {y_value}")  # Debugging statement
    distance = distance_data[x_value][y_value]
    if distance == "":
        distance = distance_data[y_value][x_value]
    return float(distance)


# Get the address index based on address string
def get_address_index(address, address_data):
    """
    Returns the index of the address in the address list.
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    for row in address_data:
        if address in row[2]:
            return int(row[0])
    return None


# Load data from CSV files
distance_data = load_csv_data("data/Distance.csv")
address_data = load_csv_data("data/Address.csv")
package_data = load_csv_data("data/Package.csv")

# Create hash table and load package data
package_hash_table = HashTable()
load_package_data(package_data, package_hash_table)

# Define the trucks with their initial settings
trucks = [
    Truck(
        1,
        18,
        [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40],
        0.0,
        "4001 South 700 East",
        datetime.timedelta(hours=8),
    ),
    Truck(
        2,
        18,
        [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39],
        0.0,
        "4001 South 700 East",
        datetime.timedelta(hours=10, minutes=20),
    ),
    Truck(
        3,
        18,
        [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33],
        0.0,
        "4001 South 700 East",
        datetime.timedelta(hours=9, minutes=5),
    ),
]


# Order packages using the Nearest Neighbor algorithm and deliver
def deliver_packages(truck, distance_data, address_data, package_hash_table):
    """
    Orders and delivers packages using the Nearest Neighbor algorithm.
    Time Complexity: O(n^2)
    Space Complexity: O(n)
    """
    undelivered_packages = [package_hash_table.get(pid) for pid in truck.packages]
    truck.packages.clear()

    truck.time = truck.depart_time

    while undelivered_packages:
        nearest_package = min(
            undelivered_packages,
            key=lambda package: calculate_distance(
                get_address_index(truck.address, address_data),
                get_address_index(package.address, address_data),
                distance_data,
            ),
        )
        distance_to_next = calculate_distance(
            get_address_index(truck.address, address_data),
            get_address_index(nearest_package.address, address_data),
            distance_data,
        )
        # truck.packages.append(nearest_package.id)
        undelivered_packages.remove(nearest_package)
        truck.mileage += distance_to_next
        truck.address = nearest_package.address
        travel_time = datetime.timedelta(hours=distance_to_next / truck.speed)
        truck.time += travel_time
        # truck.time += datetime.timedelta(hours=distance_to_next / 18)
        nearest_package.deliveryTime = truck.time
        nearest_package.departureTime = truck.depart_time
        nearest_package.status = "Delivered"


# Deliver packages using the trucks
for truck in trucks:
    deliver_packages(truck, distance_data, address_data, package_hash_table)

# Ensure truck 3 leaves after truck 1 or 2 returns
trucks[2].depart_time = min(trucks[0].time, trucks[1].time)
deliver_packages(trucks[2], distance_data, address_data, package_hash_table)


# Main Program Class
class Main:
    def __init__(self):
        print(
            f"""
 __     __     ______     __  __     ______   ______    
/\ \  _ \ \   /\  ___\   /\ \/\ \   /\  == \ /\  ___\   
\ \ \/ ".\ \  \ \ \__ \  \ \ \_\ \  \ \  _-/ \ \___  \  
 \ \__/".~\_\  \ \_____\  \ \_____\  \ \_\    \/\_____\ 
  \/_/   \/_/   \/_____/   \/_____/   \/_/     \/_____/ 
  """
        )

        while True:
            print("\nSelect from the options below:")
            print("1. Display the Status of All Packages and the Route's Total Mileage")
            print("2. Display the Status of An Individual Package at a Particular Time")
            print("3. Display the Status of All Packages at a Particular Time")
            print("4. Exit Program")

            try:
                choice = int(input("Enter your choice: "))  # Get User Input

                if choice == 1:
                    self.display_all_packages_status()
                elif choice == 2:
                    self.display_individual_package_status()
                elif choice == 3:
                    self.display_all_packages_at_time()
                elif choice == 4:
                    print("Program Ended")
                    break
                else:
                    print("Invalid Choice. Please Try Again")
            except ValueError:
                print(
                    "Invalid input. Please enter a number corresponding to the options."
                )

    def display_all_packages_status(self):
        """Display total mileage and the status of all packages."""
        total_mileage = sum(truck.mileage for truck in trucks)
        print(
            f"The existing route covers a total distance of {total_mileage} miles for package delivery\n"
        )

        for packageID in range(1, 41):
            package = package_hash_table.get(packageID)
            if packageID in {2, 3, 9, 18, 36, 38, 39, 7, 8, 10, 11, 12, 23, 24}:
                print(
                    f"Package {package.id}: {package.address} {package.city} {package.state} "
                    f"{package.zipcode} {package.deadline} {package.weight} "
                    f"Delivered at {package.delivery_time} by Truck 2"
                )
            elif packageID in {13, 1, 14, 19, 16, 15, 20, 40, 29, 30, 31, 34, 37, 17}:
                print(
                    f"Package {package.id}: {package.address} {package.city} {package.state} "
                    f"{package.zipcode} {package.deadline} {package.weight} "
                    f"Delivered at {package.delivery_time} by Truck 1"
                )
            elif packageID in {4, 5, 6, 28, 32, 33, 21, 22, 35, 27, 25, 26, 24}:
                print(
                    f"Package {package.id}: {package.address} {package.city} {package.state} "
                    f"{package.zipcode} {package.deadline} {package.weight} "
                    f"Delivered at {package.delivery_time} by Truck 3"
                )

    def display_individual_package_status(self):
        """Display the status of a specific package at a specific time."""
        while True:
            try:
                chosen = int(input("Enter a Package ID: "))
                if 1 <= chosen <= 40:
                    break
                else:
                    print("Invalid Package ID. Please Enter a Number between 1 and 40")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 40.")

        while True:
            print("Please enter a time for checking the status of the package")
            print("Enter in the format of HH:MM:SS.")
            print("For Example: 8:30 AM would be 08:30:00 & 2:30 PM would be 14:30:00")

            user_time = input("Your time?: ")
            try:
                h, m, s = map(int, user_time.split(":"))
                convert_timedelta = datetime.timedelta(hours=h, minutes=m, seconds=s)
                break
            except ValueError:
                print("Invalid time format. Please enter the time in HH:MM:SS format.")

        package = package_hash_table.get(chosen)
        package.update_status(convert_timedelta)
        print(
            f"Package {package.id}: {package.address} {package.city} {package.state} "
            f"{package.zipcode} {package.deadline} {package.weight} {package.status}"
        )

    def display_all_packages_at_time(self):
        """Display the status of all packages at a certain time."""
        while True:
            print("Please enter a time for checking the status of the packages")
            print("Enter in the format of HH:MM:SS.")
            print("For Example: 8:30 AM would be 08:30:00 & 2:30 PM would be 14:30:00")

            user_time = input("Your time?: ")
            try:
                h, m, s = map(int, user_time.split(":"))
                convert_timedelta = datetime.timedelta(hours=h, minutes=m, seconds=s)
                break
            except ValueError:
                print("Invalid time format. Please enter the time in HH:MM:SS format.")

        for packageID in range(1, 41):
            package = package_hash_table.get(packageID)
            package.update_status(convert_timedelta)
            print(
                f"Package {package.id}: {package.address} {package.city} {package.state} "
                f"{package.zipcode} {package.deadline} {package.weight} {package.status}"
            )


# Execute the program
if __name__ == "__main__":
    Main()
