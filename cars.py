from abc import ABC, abstractmethod

# ================================
# 1. Абстракт машина класы
# ================================

class CarBase(ABC):
    @abstractmethod
    def model(self):
        pass

    @abstractmethod
    def price(self):
        pass

    @abstractmethod
    def fuel_type(self):
        pass

    def info(self):
        print(f"Модель: {self.model()}")
        print(f"Бағасы: {self.price()} тг")
        print(f"Отын түрі: {self.fuel_type()}")


# ================================
# 2. Автосалондағы нақты машиналар
# ================================

class Toyota(CarBase):
    def model(self):
        return "Toyota Camry 70"

    def price(self):
        return 18000000

    def fuel_type(self):
        return "Бензин"


class BMW(CarBase):
    def model(self):
        return "BMW X5"

    def price(self):
        return 35000000

    def fuel_type(self):
        return "Бензин"


class Tesla(CarBase):
    def model(self):
        return "Tesla Model S"

    def price(self):
        return 42000000

    def fuel_type(self):
        return "Электро"


# ================================
# 3. Төлем жүйесі интерфейсі
# ================================

class PaymentInterface(ABC):
    @abstractmethod
    def authorize(self):
        pass

    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def refund(self, amount):
        pass


# ================================
# 4. Нақты төлем жүйелері
# ================================

class KaspiPay(PaymentInterface):
    def authorize(self):
        print("Kaspi жүйесі арқылы авторизация жасалды.")

    def pay(self, amount):
        print(f"Kaspi арқылы {amount} тг төленді.")

    def refund(self, amount):
        print(f"Kaspi арқылы {amount} тг қайтарылды.")


class VisaPay(PaymentInterface):
    def authorize(self):
        print("Visa авторизациясы сәтті өтті.")

    def pay(self, amount):
        print(f"Visa арқылы {amount} тг төленді.")

    def refund(self, amount):
        print(f"Visa арқылы {amount} тг қайтарылды.")


class PayPal(PaymentInterface):
    def authorize(self):
        print("PayPal тексерілді.")

    def pay(self, amount):
        print(f"PayPal арқылы {amount} тг төленді.")

    def refund(self, amount):
        print(f"PayPal арқылы {amount} тг қайтарылды.")


# ================================
# 5. Автосалон жүйесі
# ================================

class AutoSalon:
    def __init__(self):
        self.cars = [Toyota(), BMW(), Tesla()]

    def show_all_cars(self):
        print("\n=== Біздің автокөліктер ===")
        for car in self.cars:
            print("----------------------------")
            car.info()

    def buy_car(self, index, payment: PaymentInterface):
        if index < 0 or index >= len(self.cars):
            print("Мұндай индекс жоқ.")
            return

        car = self.cars[index]
        print(f"\nСіз {car.model()} таңдадыңыз.")
        payment.authorize()
        payment.pay(car.price())
        print("Сатып алу аяқталды!")


# ================================
# 6. Жүйені іске қосу
# ================================

salon = AutoSalon()
salon.show_all_cars()

print("\nTesla сатып алу:")
payment = KaspiPay()
salon.buy_car(2, payment)
