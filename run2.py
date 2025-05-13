import sys
from collections import deque
from typing import List, Tuple, Set
from dataclasses import dataclass

# Направления движения: вверх, вниз, влево, вправо
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

@dataclass
class MapInfo:
    """
    grid: поле
    robots: позиции роботов
    all_keys_mask: битовая маска всех ключей
    """
    grid: List[List[str]]
    robots: List[Tuple[int, int]]
    all_keys_mask: int

def get_input() -> List[str]:
    """Читает строки карты из стандартного ввода."""
    return [line.strip() for line in sys.stdin if line.strip()]

def parse_map(map_lines: List[str]) -> MapInfo:
    grid = [list(line) for line in map_lines]
    robots = []
    all_keys_mask = 0

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '@':
                robots.append((x, y))
            elif 'a' <= cell <= 'z':
                key_bit = 1 << (ord(cell) - ord('a'))
                all_keys_mask |= key_bit

    return MapInfo(grid=grid, robots=robots, all_keys_mask=all_keys_mask)

def solve(map_info: MapInfo) -> int:
    grid = map_info.grid
    robots = map_info.robots
    all_keys_mask = map_info.all_keys_mask

    rows, cols = len(grid), len(grid[0])
    initial_positions = tuple(robots)

    visited: Set[Tuple[Tuple[int, int], int]] = set()
    queue = deque([(initial_positions, 0, 0)])  # (позиции, ключи, шаги)
    visited.add((initial_positions, 0))

    while queue:
        positions, keys_collected, steps = queue.popleft()

        if keys_collected == all_keys_mask:
            return steps  # Все ключи собраны

        for robot_index in range(len(robots)):
            x, y = positions[robot_index]

            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy

                if not (0 <= nx < cols and 0 <= ny < rows):
                    continue  # Выход за границы

                cell = grid[ny][nx]
                if cell == '#':
                    continue  # Стена

                # Проверка двери
                if 'A' <= cell <= 'Z':
                    required_key = 1 << (ord(cell.lower()) - ord('a'))
                    if not (keys_collected & required_key):
                        continue  # Нет ключа от двери

                new_keys = keys_collected
                if 'a' <= cell <= 'z':
                    new_keys |= 1 << (ord(cell) - ord('a'))  # Собран новый ключ

                # Обновляем позицию только текущего робота
                new_positions = list(positions)
                new_positions[robot_index] = (nx, ny)

                # Роботы не могут стоять на одной клетке
                if len(set(new_positions)) < len(robots):
                    continue

                state = (tuple(new_positions), new_keys)
                if state not in visited:
                    visited.add(state)
                    queue.append((tuple(new_positions), new_keys, steps + 1))

    return -1  # Не удалось собрать все ключи

if __name__ == "__main__":
    map_lines = get_input()
    map_info = parse_map(map_lines)
    result = solve(map_info)
    print(result)
