# Eric Wang #011777714
# WGUPS Routing Program

import csv
from datetime import datetime, timedelta
from HashTable import HashTable

# Global variables
TRUCK_SPEED = 18  # miles per hour
MAX_PACKAGES_PER_TRUCK = 16
START_TIME = datetime.strptime("8:00 AM", "%I:%M %p")


class Truck:
    def __init__(self, id):
        self.id = id
        self.packages = []
        self.mileage = 0
        self.current_location = "4001 South 700 East"  # WGU address
        self.current_time = START_TIME

    def deliver_package(self, package, distance):
        travel_time = distance / TRUCK_SPEED
        self.current_time += timedelta(hours=travel_time)
        self.mileage += distance
        self.current_location = package["address"]
        package_table.update_status(package["id"], "Delivered", self.current_time)
        self.packages.remove(package["id"])


def load_distances(filename):
    distances = {}
    with open(filename, "r") as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)[1:]  # Skip the first column in the header
        for row in csv_reader:
            from_address = row[0]
            distances[from_address] = {
                headers[i]: float(row[i + 1]) if row[i + 1] else 0
                for i in range(len(headers))
            }
    return distances


def load_packages(filename, hash_table):
    with open(filename, "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            deadline = row[5]
            weight = int(row[6])
            status = "At hub"
            hash_table.insert(
                id, address, deadline, f"{city}, {state}", zip_code, weight, status
            )


def find_nearest_address(current_address, undelivered_packages, distances):
    nearest_distance = float("inf")
    nearest_package = None
    for package in undelivered_packages:
        distance = distances[current_address][package["address"]]
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_package = package
    return nearest_package, nearest_distance


def load_trucks(hash_table, num_trucks):
    all_packages = hash_table.get_all_packages()
    trucks = [Truck(i + 1) for i in range(num_trucks)]

    # Simple loading strategy (can be improved)
    truck_index = 0
    for package in all_packages:
        if len(trucks[truck_index].packages) < MAX_PACKAGES_PER_TRUCK:
            trucks[truck_index].packages.append(package.id)
        else:
            truck_index = (truck_index + 1) % num_trucks
            trucks[truck_index].packages.append(package.id)

    return trucks


def deliver_packages(trucks, distances, hash_table):
    for truck in trucks:
        while truck.packages:
            undelivered_packages = [hash_table.lookup(pid) for pid in truck.packages]
            nearest_package, distance = find_nearest_address(
                truck.current_location, undelivered_packages, distances
            )
            truck.deliver_package(nearest_package, distance)


def print_results(trucks, hash_table):
    total_mileage = sum(truck.mileage for truck in trucks)
    print(f"Total mileage for all trucks: {total_mileage:.2f} miles")

    for truck in trucks:
        print(f"Truck {truck.id} mileage: {truck.mileage:.2f} miles")

    all_packages = hash_table.get_all_packages()
    for package in all_packages:
        print(
            f"Package {package.id}: {package.status}, Delivered at: {package.delivery_time}"
        )


def main():
    # Initialize data structures
    global package_table
    package_table = HashTable()
    distances = load_distances("WGUPS Distance Table.csv")
    load_packages("WGUPS Package File.csv", package_table)

    # Initialize and load trucks
    trucks = load_trucks(package_table, 2)  # Assuming 2 trucks

    # Deliver packages
    deliver_packages(trucks, distances, package_table)

    # Print results
    print_results(trucks, package_table)


if __name__ == "__main__":
    main()
