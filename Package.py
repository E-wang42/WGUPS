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

    def update_status(self, time):
        if self.deliveryTime < time:
            self.status = "Delivered"
        elif self.departureTime > time:
            self.status = "En route"
        else:
            self.status = "At hub"

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
