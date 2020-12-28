class Node:

    def __init__(self, data, indexloc=None):
        self.data = data
        self.index = indexloc


class Graph:

    @classmethod
    def create_from_nodes(self, nodes):
        return Graph(len(nodes), len(nodes), nodes)

    def __init__(self, row, col, nodes=None):
        # установка матрица смежности
        self.adj_mat = [[0] * col for _ in range(row)]
        self.nodes = nodes
        for i in range(len(self.nodes)):
            self.nodes[i].index = i

    # Связывает node1 с node2
    # Обратите внимание, что ряд - источник, а столбец - назначение
    # Обновлен для поддержки взвешенных ребер (поддержка алгоритма Дейкстры)
    def connect_dir(self, node1, node2, weight=1):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        self.adj_mat[node1][node2] = weight

    # Опциональный весовой аргумент для поддержки алгоритма Дейкстры
    def connect(self, node1, node2, weight=1):
        self.connect_dir(node1, node2, weight)
        self.connect_dir(node2, node1, weight)

    # Получает ряд узла, отметить ненулевые объекты с их узлами в массиве self.nodes
    # Выбирает любые ненулевые элементы, оставляя массив узлов
    # которые являются connections_to (для ориентированного графа)
    # Возвращает значение: массив кортежей (узел, вес)
    def connections_from(self, node):
        node = self.get_index_from_node(node)
        return [(self.nodes[col_num], self.adj_mat[node][col_num]) for col_num in range(len(self.adj_mat[node])) if
                self.adj_mat[node][col_num] != 0]

    # Проводит матрицу к столбцу узлов
    # Проводит любые ненулевые элементы узлу данного индекса ряда
    # Выбирает только ненулевые элементы
    # Обратите внимание, что для неориентированного графа
    # используется connections_to ИЛИ connections_from
    # Возвращает значение: массив кортежей (узел, вес)
    def connections_to(self, node):
        node = self.get_index_from_node(node)
        column = [row[node] for row in self.adj_mat]

        return [(self.nodes[row_num], column[row_num]) for row_num in range(len(column)) if column[row_num] != 0]

    def print_adj_mat(self):
        for row in self.adj_mat:
            print(row)

    def node(self, index):
        return self.nodes[index]

    def remove_conn(self, node1, node2):
        self.remove_conn_dir(node1, node2)
        self.remove_conn_dir(node2, node1)

    # Убирает связь в направленной манере (nod1 к node2)
    # Может принять номер индекса ИЛИ объект узла
    def remove_conn_dir(self, node1, node2):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        self.adj_mat[node1][node2] = 0

        # Может пройти от node1 к node2

    def can_traverse_dir(self, node1, node2):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        return self.adj_mat[node1][node2] != 0

    def has_conn(self, node1, node2):
        return self.can_traverse_dir(node1, node2) or self.can_traverse_dir(node2, node1)

    def add_node(self, node):
        self.nodes.append(node)
        node.index = len(self.nodes) - 1
        for row in self.adj_mat:
            row.append(0)
        self.adj_mat.append([0] * (len(self.adj_mat) + 1))

    # Получает вес, представленный перемещением от n1
    # к n2. Принимает номера индексов ИЛИ объекты узлов
    def get_weight(self, n1, n2):
        node1, node2 = self.get_index_from_node(n1), self.get_index_from_node(n2)
        return self.adj_mat[node1][node2]

    # Разрешает проводить узлы ИЛИ индексы узлов
    def get_index_from_node(self, node):
        if not isinstance(node, Node) and not isinstance(node, int):
            raise ValueError("node must be an integer or a Node object")
        if isinstance(node, int):
            return node
        else:
            return node.index

    def dijkstra(self, node):
        # Получает индекс узла (или поддерживает передачу int)
        nodenum = self.get_index_from_node(node)
        # Заставляет массив отслеживать расстояние от одного до любого узла
        # в self.nodes. Инициализирует до бесконечности для всех узлов, кроме
        # начального узла, сохраняет "путь", связанный с расстоянием.
        # Индекс 0 = расстояние, индекс 1 = перескоки узла
        dist = [None] * len(self.nodes)
        for i in range(len(dist)):
            dist[i] = [float("inf")]
            dist[i].append([self.nodes[nodenum]])

        dist[nodenum][0] = 0
        # Добавляет в очередь все узлы графа
        # Отмечает целые числа в очереди, соответствующие индексам узла
        # локаций в массиве self.nodes
        queue = [i for i in range(len(self.nodes))]
        # Набор увиденных на данный момент номеров
        seen = set()
        while len(queue) > 0:
            # Получает узел в очереди, который еще не был рассмотрен
            # и который находится на кратчайшем расстоянии от источника
            min_dist = float("inf")
            min_node = None
            for n in queue:
                if dist[n][0] < min_dist and n not in seen:
                    min_dist = dist[n][0]
                    min_node = n

            # Добавляет мин. расстояние узла до увиденного, убирает очередь
            queue.remove(min_node)
            seen.add(min_node)
            # Получает все следующие перескоки
            connections = self.connections_from(min_node)
            # Для каждой связи обновляет путь и полное расстояние от
            # исходного узла, если полное расстояние меньше
            # чем текущее расстояние в массиве dist
            for (node, weight) in connections:
                tot_dist = weight + min_dist
                if tot_dist < dist[node.index][0]:
                    dist[node.index][0] = tot_dist
                    dist[node.index][1] = list(dist[min_node][1])
                    dist[node.index][1].append(node)
        return dist

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    nodes = [Node(str(i)) for i in range(1, 11)]

    graph = Graph.create_from_nodes(nodes)
    positions = [(1, 9), (3, 6), (3, 9), (4, 10), (5, 8), (6, 10), (7, 9), (8, 9), (9, 10)]
    for i in range(9):
        s, e = positions[i]
        for j in range(s, e):
            if s == 4 and e == 10:
                if (j == 6):
                    continue
            graph.connect(nodes[i], nodes[j])

    graph.print_adj_mat()

    w_graph = Graph.create_from_nodes(nodes)
    mt = [
        [8, 12, 7, 5, 4, 1, 5, 13],
        [4, 7, 4],
        [13, 3, 2, 5, 9, 5],
        [7, 6, 0, 3, 3, 8],
        [19, 12, 13],
        [3, 16, 12, 11],
        [3, 13],
        [7],
        [12]
    ]
    for i in range(9):
        s, e = positions[i]
        for index, m in enumerate(mt[i], start=s):
            w_graph.connect(nodes[i], nodes[index], m)

    w_graph.print_adj_mat()

    print([(weight, [n.data for n in node]) for (weight, node) in w_graph.dijkstra(nodes[1])])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
