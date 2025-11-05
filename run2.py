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

    # создаём граф как словарь множеств, у каждого узла есть список соседей
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

        # находим все возможные узлы, соединённые с выбранным шлюзом
        connected_nodes = sorted([node for node in graph[nearest_gateway] if node.islower()])

        if connected_nodes:
            # выбираем лексикографически минимальный узел для отключения
            node_to_disconnect = connected_nodes[0]
            graph[nearest_gateway].remove(node_to_disconnect)
            graph[node_to_disconnect].remove(nearest_gateway)
            actions.append(f"{nearest_gateway}-{node_to_disconnect}")

        # после нашего хода вирус делает один шаг вперёд
        distances = bfs(virus_position)
        reachable_gateways = [g for g in gateways if g in distances]
        if not reachable_gateways:
            # если пути нет то вирус остаётся на месте
            continue

        # выбираем ближайший шлюз из оставшихся
        nearest_gateway_distance = float('inf')
        nearest_gateway_for_move = None
        for g in reachable_gateways:
            if distances[g] < nearest_gateway_distance or (distances[g] == nearest_gateway_distance and g < nearest_gateway_for_move):
                nearest_gateway_distance = distances[g]
                nearest_gateway_for_move = g

        # вирус двигается на один узел ближе к ближайшему шлюзу
        next_position = None
        for neighbor in sorted(graph[virus_position]):
            if neighbor in distances and distances[neighbor] == distances[nearest_gateway_for_move] - 1:
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
            node1, separator, node2 = line.partition('-')
            edges.append((node1, node2))

    result = solve(edges)
    for r in result:
        print(r)


if __name__ == "__main__":
    main()
