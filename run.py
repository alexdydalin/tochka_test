import json
import heapq
from datetime import datetime


class Person:
    def __init__(self, name, check_in, check_out):
        self.name = name
        self.check_in = check_in
        self.check_out = check_out

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        check_in = datetime.strptime(data["check-in"], "%Y-%m-%d").date()
        check_out = datetime.strptime(data["check-out"], "%Y-%m-%d").date()
        return cls(data["name"], check_in, check_out)


def check_capacity(max_capacity: int, guests: list) -> bool:
    guests.sort(key=lambda person: person.check_in)
    heap = []
    for g in guests:
        entry = (g.check_out, g)
        if len(heap) < max_capacity:
            heapq.heappush(heap, entry)
        else:
            if g.check_in >= heap[0][0]:
                heapq.heappushpop(heap, entry)
            else:
                return False

    return True


if __name__ == "__main__":
    # изначально
    # Чтение входных данных
    max_capacity = int(input())
    n = int(input())
    guests = []
    for _ in range(n):
      guest_json = input()
      guest_data = json.loads(guest_json)
      guests.append(guest_data)
    # 1

    guest_obj_list = [Person.from_json(i) for i in guests]
    result = check_capacity(max_capacity, guest_obj_list)
    print(result)
