import sys
from collections import deque, defaultdict

def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """


    # Создаём граф как словарь множеств, у каждого узла есть список соседей
    graph = defaultdict(set)
    for n1, n2 in edges:
        graph[n1].add(n2)
        graph[n2].add(n1)

    # находим все шлюзы (большие буквы)
    gateways = sorted([n for n in graph if n.isupper()])

    # вирус всегда начинает в узле а
    virus_position = 'a'

    # сюда пишем порядок отключаемых связей, то что пойдет в ответ
    actions = []

    def bfs(start: str) -> dict:
        """
            поиск в ширину
            функция для нахождения кратчайших расстояний от узла до всех остальных узлов
        """
        distances = {start: 0}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            # перебираем всех соседей текущего узла
            for neighbor in sorted(graph[current]):
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        return distances

    # цикл работает пока есть активные шлюзы
    while True:
        # Список оставшихся шлюзов подключённых к обычным узлам
        active_gateway_edges = [
            (gateway, neighbor)
            for gateway in gateways
            for neighbor in graph[gateway]
            if neighbor.islower()
        ]

        # если таких связей больше нет, значит все шлюзы изолированы
        if not active_gateway_edges:
            break

        # считаем расстояния от вируса до всех узлов
        distances = bfs(virus_position)

        # ищем ближайший шлюз
        nearest_gateway = None
        min_distance = float('inf')
        for gateway in gateways:
            if gateway in distances:
                distance = distances[gateway]
                if distance < min_distance or (distance == min_distance and gateway < nearest_gateway):
                    nearest_gateway = gateway
                    min_distance = distance

        # если вирус не может добраться ни до одного шлюза то он изолирован
        if nearest_gateway is None:
            break

        # находим путь до ближайшего шлюза
        previous = {}
        visited = {virus_position}
        queue = deque([virus_position])
        found_gateway = False

        while queue and not found_gateway:
            current = queue.popleft()
            for neighbor in sorted(graph[current]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    previous[neighbor] = current
                    queue.append(neighbor)
                    if neighbor == nearest_gateway:
                        found_gateway = True
                        break

        # восстанавливаем путь (от вируса до шлюза)
        path = []
        node = nearest_gateway
        while node != virus_position:
            path.append(node)
            node = previous[node]
        path.append(virus_position)
        path.reverse() # это уже путь от вируса к шлюзу

        # проверка соединен ли вирус со шлюзом напрямую
        direct_connection = None
        for gateway in gateways:
            if virus_position in graph[gateway]:
                direct_connection = (gateway, virus_position)
                break

        if direct_connection:
            # если вирус прямо у шлюза то соединение обрубается
            gateway, node = direct_connection
            graph[gateway].remove(node)
            graph[node].remove(gateway)
            actions.append(f"{gateway}-{node}")
        else:
            # если вирус не у шлюза то отключаем последнюю связь в найденном пути
            if len(path) >= 2:
                node_before_gateway = path[-2]  # узел перед шлюзом
                gateway = path[-1]
                graph[gateway].remove(node_before_gateway)
                graph[node_before_gateway].remove(gateway)
                actions.append(f"{gateway}-{node_before_gateway}")

        # после нашего хода вирус делает один шаг вперёд
        distances = bfs(virus_position)
        if nearest_gateway not in distances:
            # если пути нет то вирус остаётся на месте
            continue

        # вирус двигается на один узел ближе к шлюзу
        next_position = None
        for neighbor in sorted(graph[virus_position]):
            if neighbor in distances and distances[neighbor] == distances[nearest_gateway] - 1:
                next_position = neighbor
                break
        if next_position:
            virus_position = next_position

    return actions


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            n1, sep, n2 = line.partition('-')
            edges.append((n1, n2))

    result = solve(edges)
    for r in result:
        print(r)


if __name__ == "__main__":
    main()
