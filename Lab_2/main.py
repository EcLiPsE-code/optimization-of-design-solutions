import sys

class HungarianMethod:
    def __init__(self) -> None:
        self._matrix = None
        self.col = None
        self.row = None
        self._mask = []  #True - (0 помечен точкой), (-1) - (0 вычеркнут)
        self.result = None
        self._min_elements_in_lines: [int] = None  # минимальные элементы в каждой строке
        self._min_elements_in_columns: [int] = None  # минимальные элементы в каждодм столбце

    def set_row(self, row):
        self.row = row

    def set_col(self, col):
        self.col = col

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def set_matrix(self, matrix) -> None:
        self._matrix = matrix

    def get_matrix(self) -> None:
        for i in range(len(self._matrix)):
            for j in range(len(self._matrix[0])):
                print("{}".format(self._matrix[i][j]), end="\t")
            print()

    def _search_min_elements_in_lines(self) -> None:  # функция для поиска минимльного значения в каждой строке
        self._min_elements_in_lines = [0 for i in range(self.row)]
        for i in range(self.row):
            temp_min = sys.maxsize
            for j in range(self.col):
                if self._matrix[i][j] < temp_min:
                    temp_min = self._matrix[i][j]
            self._min_elements_in_lines[i] = temp_min

    def _search_min_elements_in_columns(self) -> None:  # поиск мин значений в каждом столбце
        self._min_elements_in_columns = [0 for i in range(self.col)]
        for i in range(self.col):
            temp_min = sys.maxsize
            for j in range(self.row):
                if self._matrix[j][i] < temp_min:
                    temp_min = self._matrix[j][i]
            self._min_elements_in_columns[i] = temp_min

    def _calc_min_elements_in_lines(self) -> None:  # отнимает найденное минимальное значение от всех эл строки
        for i in range(self.row):
            for j in range(self.col):
                self._matrix[i][j] -= self._min_elements_in_lines[i]

    def _calc_min_elements_in_columns(self) -> None:  # отнимает найденное минимальное значение от всех эл столбца
        for i in range(self.col):
            for j in range(self.row):
                self._matrix[j][i] -= self._min_elements_in_columns[i]

    def getting_zeros(self) -> None:  # получение 0 в строках и столбцах
        self._search_min_elements_in_lines()
        self._calc_min_elements_in_lines()
        self._search_min_elements_in_columns()
        self._calc_min_elements_in_columns()

    def find_optimal_solution(self) -> None:  # нахождение первноначального плана
        self._mask = [[False for i in range(self.col)]
                     for j in range(self.row)]

        for i in range(self.row):   #True - помечен точкой, -1 - зачеркнут
            for j in range(self.col):
                if self._matrix[i][j] == 0 and self._mask[i][j] != True and self._mask[i][j] != -1:
                    self._mask[i][j] = True
                    for k in range(self.col):  # зачеркиваем все остальные нули в строке
                        if self._matrix[i][k] == 0 and self._mask[i][k] == False:
                            self._mask[i][k] = -1
                    for m in range(self.row):
                        if self._matrix[m][i] == 0 and self._mask[i][m] == False:
                            self._mask[m][i] = -1

    def check_result(self) -> bool:  # проверка количества полученных нулей в mask (n = column)
        self.hungarian()
        if len(self.result) == self.col:
            print("Тк число отмеченных 0 равно n, то решение является полным, а план оптимальным, "
                  "производим расчет целевой функции...")
            print("Значение целевой функции равно: {}".format(self.calc_objective_function()))
        else:
            print("План не оптимальный выполняем перерасчет...")
            self.hungarian()
            self.check_result()

    def hungarian(self):
        # Значения, вычитаемые из строк (u) и столбцов (v)
        u = [0 for i in range(self.row)]
        v = [0 for j in range(self.col)]

        # Индекс помеченной клетки в каждом столбце
        mark_indexes = [-1 for i in range(self.col)]

        count = 0
        for i in range(self.row):
            links = [-1 for i in range(self.col)]
            mins = [sys.maxsize for i in range(self.col)]
            visited = [0 for i in range(self.col)]

            # Разрешение коллизий (создание "чередующейся цепочки" из нулевых элементов)
            markedI = i
            markedJ = -1
            j = 0
            while markedI != -1:
                j = -1
                for j_1 in range(self.col):
                    if visited[j_1] != 1:
                        if self._matrix[markedI][j_1] - u[markedI] - v[j_1] < mins[j_1]:
                            mins[j_1] = self._matrix[markedI][j_1] - u[markedI] - v[j_1]
                            links[j_1] = markedJ
                        if j == -1 or (mins[j_1] < mins[j]):
                            j = j_1
                delta = mins[j]
                for j_1 in range(self.col):
                    if visited[j_1] == 1:
                        u[mark_indexes[j_1]] += delta
                        v[j_1] -= delta
                    else:
                        mins[j_1] -= delta
                u[i] += delta

                visited[j] = 1
                markedJ = j
                markedI = mark_indexes[j]
                count += 1

            while links[j] != -1:
                mark_indexes[j] = mark_indexes[links[j]]
                j = links[j]
            mark_indexes[j] = i

        result = []
        for j in range(self.col):
            if mark_indexes[j] != -1:
                result.append([mark_indexes[j], j])
        self.result = result

    def calc_objective_function(self) -> int:
        sum = 0
        for k in range(len(self.result)):
            i = self.result[k][0]
            j = self.result[k][1]
            sum += self._matrix[i][j]
        return sum

if __name__ == "__main__":
    method = HungarianMethod()
    print("Введите количество вакансий(столбцы): ")
    method.set_col(int(input()))
    print("Введите количество кандидатов(строки): ")
    method.set_row(int(input()))
    print("Введите матрицу: ")
    method.set_matrix([list(map(int, input().split()))
                                     for i in range(method.get_row())])
    method.check_result()
    print("Матрица: ")
    method.get_matrix()
    print("Матрица после приведения по строкам и столбцам")
    method.getting_zeros()
    method.get_matrix()
