# vehicle_schedule.py
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List
from pathlib import Path

# -------------------------------
#   1. Деректер моделі (Vehicle)
# -------------------------------
@dataclass
class Vehicle:
    id: str
    driver: str
    route: str
    depart_time: str
    arrive_time: Optional[str] = None
    notes: Optional[str] = None

    def to_dict(self):
        return asdict(self)


# -------------------------------
#   2. Көмекші функциялар
# -------------------------------
TIME_FORMAT = "%H:%M"

def valid_time_string(t: str) -> bool:
    try:
        datetime.strptime(t, TIME_FORMAT)
        return True
    except ValueError:
        return False

def normalize_time(t: str) -> str:
    dt = datetime.strptime(t, TIME_FORMAT)
    return dt.strftime(TIME_FORMAT)


# -------------------------------
#   3. Негізгі кесте басқару класы
# -------------------------------
class Schedule:
    def __init__(self, store_path="schedule.json"):
        self.store_path = Path(store_path)
        self.vehicles: List[Vehicle] = []
        self.load()

    def add_vehicle(self, vehicle: Vehicle) -> None:
        # уақыт тексеру
        if not valid_time_string(vehicle.depart_time):
            raise ValueError("Қате уақыт форматы: " + vehicle.depart_time)
        vehicle.depart_time = normalize_time(vehicle.depart_time)

        if vehicle.arrive_time:
            if not valid_time_string(vehicle.arrive_time):
                raise ValueError("Қате уақыт форматы: " + vehicle.arrive_time)
            vehicle.arrive_time = normalize_time(vehicle.arrive_time)

        # бірдей ID тексеру
        if any(v.id == vehicle.id for v in self.vehicles):
            raise ValueError("Бұл ID бар: " + vehicle.id)

        self.vehicles.append(vehicle)
        self.save()

    def remove_vehicle(self, vehicle_id: str) -> bool:
        before = len(self.vehicles)
        self.vehicles = [v for v in self.vehicles if v.id != vehicle_id]
        if len(self.vehicles) != before:
            self.save()
            return True
        return False

    def update_vehicle(self, vehicle_id: str, **fields) -> bool:
        for v in self.vehicles:
            if v.id == vehicle_id:
                for key, val in fields.items():
                    if key in ("depart_time", "arrive_time") and val:
                        if not valid_time_string(val):
                            raise ValueError("Қате уақыт: " + val)
                        val = normalize_time(val)
                    if hasattr(v, key):
                        setattr(v, key, val)
                self.save()
                return True
        return False

    def list_all(self):
        return self.vehicles

    def find_by_time(self, time_str: str):
        if not valid_time_string(time_str):
            raise ValueError("Қате уақыт форматы")
        t = normalize_time(time_str)
        return [v for v in self.vehicles if v.depart_time == t]

    def save(self):
        with open(self.store_path, "w", encoding="utf-8") as f:
            json.dump([v.to_dict() for v in self.vehicles], f, ensure_ascii=False, indent=2)

    def load(self):
        if not self.store_path.exists():
            self.vehicles = []
            return
        try:
            with open(self.store_path, "r", encoding="utf-8") as f:
                arr = json.load(f)
                self.vehicles = [Vehicle(**item) for item in arr]
        except:
            self.vehicles = []


# -------------------------------
#   4. Бағдарламаны іске қосу
# -------------------------------
def main():
    sched = Schedule()

    while True:
        print("\n=== КӨЛІК КЕСТЕСІ ЖҮЙЕСІ ===")
        print("1. Көлік қосу")
        print("2. Көлікті өшіру")
        print("3. Көлікті өзгерту")
        print("4. Барлық жазбаларды көру")
        print("5. Уақыт бойынша іздеу")
        print("0. Шығу")

        choice = input("Таңдау: ")

        if choice == "1":
            id_ = input("ID: ")
            driver = input("Жүргізуші: ")
            route = input("Маршрут: ")
            depart = input("Шығу уақыты (HH:MM): ")
            arrive = input("Келу уақыты (HH:MM, бос қалса OK): ")
            notes = input("Ескертпе: ")

            try:
                v = Vehicle(id_, driver, route, depart, arrive or None, notes or None)
                sched.add_vehicle(v)
                print("✔ Көлік қосылды!")
            except Exception as e:
                print("Қате:", e)

        elif choice == "2":
            vid = input("ID енгізіңіз: ")
            if sched.remove_vehicle(vid):
                print("✔ Өшірілді")
            else:
                print("ID табылмады.")

        elif choice == "3":
            vid = input("ID: ")
            field = input("Өріс (driver/route/depart_time/arrive_time/notes): ")
            val = input("Жаңа мән: ")

            if sched.update_vehicle(vid, **{field: val}):
                print("✔ Өзгертілді.")
            else:
                print("ID табылмады.")

        elif choice == "4":
            print("\n=== БАРЛЫҚ КЕСТЕ ===")
            for v in sched.list_all():
                print(v)

        elif choice == "5":
            t = input("Уақыт (HH:MM): ")
            res = sched.find_by_time(t)
            print(f"\n{t} уақытына шықатын рейстер:")
            for v in res:
                print(v)

        elif choice == "0":
            print("Бағдарлама жабылды.")
            break

        else:
            print("Қате таңдау.")


if __name__ == "__main__":
    main()
