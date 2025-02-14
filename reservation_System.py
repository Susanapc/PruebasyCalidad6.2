"""
    This is the class Hotel
"""
import json
import os
import unittest


class Hotel:
    """
        This is the class Hotel
    """
    def __init__(self, hotel_id, name, location, rooms):
        """
        Brief description of what the function does.
        """
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = rooms  # Dictionary with room number as key and availability as value

    def to_dict(self):
        """
        Brief description of what the function does.
        """
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "rooms": self.rooms
        }

    @staticmethod
    def from_dict(data):
        """
        Brief description of what the function does.
        """
        return Hotel(data['hotel_id'], data['name'], data['location'], data['rooms'])


class Customer:
    """
        This is the class Customer
    """
    def __init__(self, customer_id, name, email):
        """
        Brief description of what the function does.
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self):
        """
        Brief description of what the function does.
        """
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email
        }

    @staticmethod
    def from_dict(data):
        """
        Brief description of what the function does.
        """
        return Customer(data['customer_id'], data['name'], data['email'])


class Reservation:
    """
        This is the class Reservation
    """
    def __init__(self, reservation_id, customer_id, hotel_id, room_number):
        """
        Brief description of what the function does.
        """
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.room_number = room_number

    def to_dict(self):
        """
        Brief description of what the function does.
        """
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "room_number": self.room_number
        }

    @staticmethod
    def from_dict(data):
        """
        Brief description of what the function does.
        """
        return Reservation(data['reservation_id'], data['customer_id'], data['hotel_id'], data['room_number'])


class HotelManagementSystem:
    """
        This is the class to manage the hotel system
    """
    def __init__(self):
        """
        Brief description of what the function does.
        """
        self.hotels_file = 'hotels.json'
        self.customers_file = 'customers.json'
        self.reservations_file = 'reservations.json'
        self.hotels = self.load_data(self.hotels_file)
        self.customers = self.load_data(self.customers_file)
        self.reservations = self.load_data(self.reservations_file)

    def load_data(self, file_name):
        """
        Brief description of what the function does.
        """
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    print(f"Error reading {file_name}. File might be corrupted.")
                    return {}
        return {}

    def save_data(self, file_name, data):
        """
        Brief description of what the function does.
        """
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file)

    # Hotel methods
    def create_hotel(self, hotel):
        """
        Brief description of what the function does.
        """
        if hotel.hotel_id in self.hotels:
            print(f"Hotel with ID {hotel.hotel_id} already exists.")
            return False
        self.hotels[hotel.hotel_id] = hotel.to_dict()
        self.save_data(self.hotels_file, self.hotels)
        return True

    def delete_hotel(self, hotel_id):
        """
        Brief description of what the function does.
        """
        if hotel_id in self.hotels:
            del self.hotels[hotel_id]
            self.save_data(self.hotels_file, self.hotels)
            return True
        print(f"Hotel with ID {hotel_id} does not exist.")
        return False

    def display_hotel_info(self, hotel_id):
        """
        Brief description of what the function does.
        """
        if hotel_id in self.hotels:
            return Hotel.from_dict(self.hotels[hotel_id])
        print(f"Hotel with ID {hotel_id} does not exist.")
        return None

    def modify_hotel_info(self, hotel):
        """
        Brief description of what the function does.
        """
        if hotel.hotel_id in self.hotels:
            self.hotels[hotel.hotel_id] = hotel.to_dict()
            self.save_data(self.hotels_file, self.hotels)
            return True
        print(f"Hotel with ID {hotel.hotel_id} does not exist.")
        return False

    def reserve_room(self, reservation):
        """
        Brief description of what the function does.
        """
        if reservation.hotel_id in self.hotels:
            hotel = Hotel.from_dict(self.hotels[reservation.hotel_id])
            if reservation.room_number in hotel.rooms and hotel.rooms[reservation.room_number]:
                hotel.rooms[reservation.room_number] = False  # Mark room as reserved
                if reservation.reservation_id not in self.reservations:
                    self.reservations[reservation.reservation_id] = reservation.to_dict()
                    self.save_data(self.reservations_file, self.reservations)
                    # Update hotel data with reserved room status
                    self.modify_hotel_info(hotel)
                    return True
                # else:
                print(f"Reservation with ID {reservation.reservation_id} already exists.")
                return False
            # else:
            print(f"Room number {reservation.room_number} is not available.")
            return False
        print(f"Hotel with ID {reservation.hotel_id} does not exist.")
        return False

    def cancel_reservation(self, reservation_id):
        """
        Brief description of what the function does.
        """
        if reservation_id in self.reservations:
            reservation = Reservation.from_dict(self.reservations[reservation_id])
            if reservation.hotel_id in self.hotels:
                hotel = Hotel.from_dict(self.hotels[reservation.hotel_id])
                if reservation.room_number in hotel.rooms and not hotel.rooms[reservation.room_number]:
                    hotel.rooms[reservation.room_number] = True  # Mark room as available
                    del self.reservations[reservation.reservation_id]
                    # Update hotel data with available room status
                    self.modify_hotel_info(hotel)
                    # Save updated reservations data
                    self.save_data(self.reservations_file, self.reservations)
                    return True
                # else:
                print(f"Room number {reservation.room_number} is already available.")
                return False
            # else:
            print(f"Hotel with ID {reservation.hotel_id} does not exist.")
            return False
        print(f"Reservation with ID {reservation_id} does not exist.")
        return False

    # Customer methods
    def create_customer(self, customer):
        """
        Brief description of what the function does.
        """
        if customer.customer_id in self.customers:
            print(f"Customer with ID {customer.customer_id} already exists.")
            return False
        self.customers[customer.customer_id] = customer.to_dict()
        self.save_data(self.customers_file, self.customers)
        return True

    def delete_customer(self, customer_id):
        """
        Brief description of what the function does.
        """
        if customer_id in self.customers:
            del self.customers[customer_id]
            # Save updated customers data
            self.save_data(self.customers_file, self.customers)
            return True
        print(f"Customer with ID {customer_id} does not exist.")
        return False

    def display_customer_info(self, customer_id):
        """
        Brief description of what the function does.
        """
        if customer_id in self.customers:
            return Customer.from_dict(self.customers[customer_id])
        print(f"Customer with ID {customer_id} does not exist.")
        return None

    def modify_customer_info(self, customer):
        """
        Brief description of what the function does.
        """
        if customer.customer_id in self.customers:
            # Update customer information and save it to the file.
            self.customers[customer.customer_id] = customer.to_dict()
            # Save updated customers data.
            self.save_data(self.customers_file, self.customers)
            return True
        print(f"Customer with ID {customer.customer_id} does not exist.")
        return False


# Unit tests for the HotelManagementSystem class.
class TestHotelManagementSystem(unittest.TestCase):
    """
        This is the class for the tests
    """

    @classmethod
    def setUpClass(cls):
        """
        Brief description of what the function does.
        """
        cls.system = HotelManagementSystem()

    def test_create_hotel(self):
        """
        Brief description of what the function does.
        """
        hotel = Hotel("1", "Hotel One", "Location One", {"101": True, "102": True})
        self.assertTrue(self.system.create_hotel(hotel))

    def test_delete_hotel(self):
        """
        Brief description of what the function does.
        """
        self.assertTrue(self.system.delete_hotel("1"))

    def test_delete_hotel2(self):
        """
        Brief description of what the function does.
        """
        self.assertFalse(self.system.delete_hotel("1"))

    def test_display_hotel_info(self):
        """
        Brief description of what the function does.
        """
        hotel = Hotel("2", "Hotel Two", "Location Two", {"201": True, "202": True})
        self.system.create_hotel(hotel)
        self.assertIsNotNone(self.system.display_hotel_info("2"))

    def test_modify_hotel_info(self):
        """
        Brief description of what the function does.
        """
        hotel = Hotel("2", "Hotel Two Modified", "Location Two", {"201": True, "202": True})
        self.assertTrue(self.system.modify_hotel_info(hotel))

    def test_reserve_room(self):
        """
        Brief description of what the function does.
        """
        reservation = Reservation("1", "1", "2", "201")
        self.assertTrue(self.system.reserve_room(reservation))

    def test_reserve_room2(self):
        """
        Brief description of what the function does.
        """
        reservation = Reservation("2", "1", "2", "202")
        self.assertTrue(self.system.reserve_room(reservation))

    def test_zcancel_reservation(self):
        """
        Brief description of what the function does.
        """
        self.assertTrue(self.system.cancel_reservation("1"))

    def test_zcancel_reservation2(self):
        """
        Brief description of what the function does.
        """
        self.assertFalse(self.system.cancel_reservation("1"))

    def test_zcancel_reservation2(self):
        """
        Brief description of what the function does.
        """
        self.assertFalse(self.system.cancel_reservation("5"))

    def test_create_customer(self):
        """
        Brief description of what the function does.
        """
        customer = Customer("1", "Customer One", "customer1@example.com")
        self.assertTrue(self.system.create_customer(customer))

    def test_create_customer2(self):
        """
        Run the test again to cover the code of failure while trying to create the same customer.
        """
        customer = Customer("1", "Customer One", "customer1@example.com")
        self.assertFalse(self.system.create_customer(customer))

    def test_delete_customer(self):
        """
        Brief description of what the function does.
        """
        self.assertTrue(self.system.delete_customer("1"))

    def test_delete_customer2(self):
        """
        Brief description of what the function does.
        """
        self.assertFalse(self.system.delete_customer("8"))

    def test_display_customer_info(self):
        """
        Brief description of what the function does.
        """
        customer = Customer("2", "Customer Two", "customer2@example.com")
        self.system.create_customer(customer)
        self.assertIsNotNone(self.system.display_customer_info("2"))

    def test_modify_customer_info(self):
        """
        Brief description of what the function does.
        """
        customer = Customer("2", "Customer Two Modified", "customer2@example.com")
        self.assertTrue(self.system.modify_customer_info(customer))


if __name__ == '__main__':
    unittest.main()
