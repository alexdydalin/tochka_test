import sys
import heapq


# Разрешённые позиции коридора, где можно останавливаться (нельзя на 2, 4, 6, 8)
hallway_available_spots = [0, 1, 3, 5, 7, 9, 10]

# Целевые позиции комнат в коридоре
rooms_positions = {'A': 2, 'B': 4, 'C': 6, 'D': 8}

# Стоимость перемещения для каждого типа амфиподов
costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


def collect_rooms_info(lines):
    """
            функция парсит строки из входящего файла, возвращает:
            rooms: словарь с объектами по комнатам
            room_size: размер комнат (2 или 4)
    """
    # пропускаем стены
    hallway = tuple(lines[1][1:12])

    room_depth = len(lines) - 3

    rooms = {'A': [], 'B': [], 'C': [], 'D': []}
    for lvl in range(room_depth):
        line = lines[2 + lvl]
        rooms['A'].append(line[3])
        rooms['B'].append(line[5])
        rooms['C'].append(line[7])
        rooms['D'].append(line[9])

    # Преобразуем в кортежи, нужно для хешируемости состояний
    rooms_tuple = tuple(tuple(rooms[r]) for r in 'ABCD')
    return hallway, rooms_tuple


def is_solved(rooms) -> bool:
    """
        Проверяет, находится ли каждый тип амфипода в своей целевой комнате.
    """
    for i, r in enumerate('ABCD'):
        if any(x != r for x in rooms[i]):
            return False
    return True


def moves_from_room(hallway, rooms, room_idx, room_depth) -> list:
    """
        Генерирует все возможные ходы, когда амфипод выходит из комнаты в коридор.
    """
    room = rooms[room_idx]
    room_pos = list(rooms_positions.values())[room_idx]
    moves = []

    # Найти верхнего амфипода, который может выйти
    for depth, pod in enumerate(room):
        if pod != '.':
            break
    else:
        return moves  # комната пуста

    # Если все под ним правильного типа — он уже на месте
    if all(p == 'ABCD'[room_idx] for p in room[depth:]):
        return moves

    # Проверяем возможные остановки в коридоре
    for target in hallway_available_spots:
        start, end = sorted([room_pos, target])
        # Путь должен быть полностью свободен
        if all(hallway[i] == '.' for i in range(start, end + 1) if i != room_pos):
            steps = depth + 1 + abs(room_pos - target)
            cost = steps * costs[pod]

            # Формируем новое состояние
            new_hallway = list(hallway)
            new_hallway[target] = pod
            new_rooms = [list(r) for r in rooms]
            new_rooms[room_idx][depth] = '.'

            moves.append(
                (cost, tuple(new_hallway), tuple(tuple(r) for r in new_rooms))
            )

    return moves


def moves_to_room(hallway, rooms, room_depth):
    """
        Генерирует все возможные ходы, когда амфипод из коридора заходит в свою комнату.
    """
    moves = []

    for pos, pod in enumerate(hallway):
        if pod == '.':
            continue

        target_room_idx = 'ABCD'.index(pod)
        target_room = rooms[target_room_idx]

        # Нельзя заходить, если внутри есть другой тип
        if any(r != '.' and r != pod for r in target_room):
            continue

        room_pos = list(rooms_positions.values())[target_room_idx]
        start, end = sorted([pos, room_pos])

        # Проверяем свободен ли путь до комнаты
        if not all(hallway[i] == '.' for i in range(start, end + 1) if i != pos):
            continue

        # Находит самую глубокую свободную позицию
        depth = max(i for i, r in enumerate(target_room) if r == '.')
        steps = abs(pos - room_pos) + depth + 1
        cost = steps * costs[pod]

        # Формируем новое состояние
        new_hallway = list(hallway)
        new_hallway[pos] = '.'
        new_rooms = [list(r) for r in rooms]
        new_rooms[target_room_idx][depth] = pod

        moves.append(
            (cost, tuple(new_hallway), tuple(tuple(r) for r in new_rooms))
        )

    return moves


def solve(lines: list[str]) -> int:
    """
        Основная функция решения задачи.
        Реализует алгоритм Дейкстры для поиска минимальной энергии.
        Возвращает минимальную энергию для достижения целевого состояния
    """
    hallway, rooms = collect_rooms_info(lines)
    room_depth = len(rooms[0])
    start = (hallway, rooms)

    # Очередь приоритетов (энергия, состояние)
    heap = [(0, start)]
    visited = {}

    while heap:
        energy, state = heapq.heappop(heap)

        # Если уже видели это состояние с меньшей энергией то пропускаем
        if state in visited and visited[state] <= energy:
            continue
        visited[state] = energy

        hall, rms = state

        # Проверяем достигнута ли цель
        if is_solved(rms):
            return energy

        # Ходы из комнаты в коридор
        for i in range(4):
            for cost, nhall, nrms in moves_from_room(hall, rms, i, room_depth):
                heapq.heappush(heap, (energy + cost, (nhall, nrms)))

        # Ходы из коридора в комнату
        for cost, nhall, nrms in moves_to_room(hall, rms, room_depth):
            heapq.heappush(heap, (energy + cost, (nhall, nrms)))

    return 0



def main():
    # Чтение входных данных
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()
