import datetime


class Package:
    def __init__(self, id, address, city, state, zipcode, deadline, weight, notes):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = "At hub"
        self.deliveryTime = None
        self.departureTime = None
        self.address_corrected = False

    def update_status(self, time):
        if self.id == 9 and not self.address_corrected:
            correction_time = datetime.timedelta(hours=10, minutes=20)
            if time >= correction_time:
                self.address = "410 S State St"
                self.city = "Salt Lake City"
                self.state = "UT"
                self.zipcode = "84111"
                self.address_corrected = True

        if self.departureTime and time < self.departureTime:
            self.status = "At Hub"
            self.deliveryTime = None
        elif self.deliveryTime and time < self.deliveryTime:
            self.status = "En Route"
        elif self.deliveryTime and time >= self.deliveryTime:
            self.status = "Delivered"
        else:
            self.status = "At Hub"

    def __str__(self):
        if self.status == "Delivered":
            return (
                f"Package {self.id}: {self.status}, Delivered at: {self.deliveryTime}.\n"
                f"Address: {self.address}, {self.city}, {self.state} {self.zipcode}.\n"
                f"Weight: {self.weight} lbs, Deadline: {self.deadline}, Notes: {self.notes}."
            )
        return (
            f"Package latest status: {self.status}.\n"
            f"Address: {self.address}, {self.city}, {self.state} {self.zipcode}.\n"
            f"Weight: {self.weight} lbs, Deadline: {self.deadline}, Notes: {self.notes}."
        )
