from abc import ABC, abstractmethod

class RoomType(ABC):

    @abstractmethod
    def get_description(self):
        pass
class StandardRoom(RoomType):
    def get_description(self):
        return "Стандарт бөлме – базалық ыңғайлылықтар"


class SuiteRoom(RoomType):
    def get_description(self):
        return "Люкс бөлме – жоғары деңгейлі сервис"
class Room:
    def __init__(self, room_number, price, room_type: RoomType):
        self.__room_number = room_number
        self.__price = price
        self.__is_available = True
        self.__room_type = room_type

    # Getters
    def get_number(self):
        return self.__room_number

    def get_price(self):
        return self.__price

    def is_available(self):
        return self.__is_available

    def get_type_description(self):
        return self.__room_type.get_description()

    # Setter
    def book(self):
        self.__is_available = False

    def release(self):
        self.__is_available = True
class Customer:
    def __init__(self, name, email, customer_id):
        self.__name = name
        self.__email = email
        self.__id = customer_id

    def get_info(self):
        return f"{self.__name} ({self.__email}) ID: {self.__id}"
class Reservation:
    def __init__(self, room: Room, customer: Customer, check_in, check_out):
        self.room = room
        self.customer = customer
        self.check_in = check_in
        self.check_out = check_out

    def get_details(self):
        return f"Брондау: {self.customer.get_info()} | Бөлме {self.room.get_number()} | {self.check_in} - {self.check_out}"
class Hotel:
    def __init__(self):
        self.rooms = []
        self.reservations = []

    def add_room(self, room: Room):
        self.rooms.append(room)

    def show_available_rooms(self):
        print("Қолжетімді бөлмелер:")
        for room in self.rooms:
            if room.is_available():
                print(f"- Бөлме {room.get_number()} | Баға: {room.get_price()} | {room.get_type_description()}")

    def book_room(self, room_number, customer, check_in, check_out):
        for room in self.rooms:
            if room.get_number() == room_number and room.is_available():
                room.book()
                reservation = Reservation(room, customer, check_in, check_out)
                self.reservations.append(reservation)
                print("✅ Бөлме сәтті брондалды!")
                print(reservation.get_details())
                return
        print("❌ Бұл бөлме қолжетімсіз!")
# Бөлме типтері
std = StandardRoom()
suite = SuiteRoom()

# Қонақүй
hotel = Hotel()

# Бөлмелер
hotel.add_room(Room(101, 20000, std))
hotel.add_room(Room(102, 25000, std))
hotel.add_room(Room(201, 40000, suite))
hotel.add_room(Room(202, 45000, suite))

# Клиент
customer1 = Customer("Еламан", "elaman@mail.com", 1)

# Қолжетімді бөлмелер
hotel.show_available_rooms()

# Бөлме брондау
hotel.book_room(201, customer1, "2025-01-10", "2025-01-15")

# Тағы тексеру
hotel.show_available_rooms()
