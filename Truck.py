class Truck:
    def __init__(self, truckID, speed, packages, mileage, address, depart_time):
        self.truckID = truckID
        self.speed = speed
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time

    def __str__(self):
        return f"#Truck: {self.truckID} carrying {self.packages} of packages"
