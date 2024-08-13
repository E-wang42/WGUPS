class Truck:
    def __init__(self, truckID, speed, packages, mileage, address, depart_time):
        self.truckID = truckID
        self.speed = speed
        self.packages = packages if packages is not None else []
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self):
        return f"#Truck: {self.truckID} carrying {len(self.packages)} packages, Mileage: {self.mileage}"
