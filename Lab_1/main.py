class NorthwestCornerMethod:  # класс, описывающий метод северо западного угла
    def __init__(self) -> None:
        self.missing_columns_index = []  # массив пропущенных столбцов (содержит индексы столюцов)
        self.missing_rows_index = []  # массив пропущеннвх строк (содержит индексы строк)
        self.find_min_values = []
        self.matrix_base_plan = None  # опорный план
        self.count_value_point_of_departure: int = 0
        self.count_value_destination: int = 0
        self.value_point_of_departure: [int] = []  # количество груза на каждой точке отправления (Запасы)
        self.value_destination: int = 0  # количество необходимого груза на каждом пункте назначения (Потребности)
        self.transportation_rates = None  # тарифы перевозок

    def set_value_point_of_departure(self, values_point_of_departure: [int]) -> None:
        self.value_point_of_departure = values_point_of_departure
        self.count_value_point_of_departure = len(values_point_of_departure)

    def set_value_destination(self, values_destination: [int]) -> None:
        self.value_destination = values_destination
        self.count_value_destination = len(values_destination)

    def set_transportation_rates(self, transportation_rates: [int]) -> None:
        self.transportation_rates = transportation_rates

    def get_value_point_of_departure(self) -> [int]:
        return self.value_point_of_departure

    def get_value_destination(self) -> [int]:
        return self.value_destination

    def get_value_transportation_rates(self) -> [int]:
        return self.transportation_rates

    def _search_min_value_transportation_rates(self):  # поиск минимального тарифного плана
        temp_min = self.transportation_rates[0][0]
        temp_min_row_index = self.transportation_rates[0]
        temp_min_column_index = self.transportation_rates[0]
        for i in range(self.count_value_point_of_departure):
            for j in range(self.count_value_destination):
                if self.transportation_rates[i][j] < temp_min and not(self.transportation_rates[i][j] in self.find_min_values):
                    temp_min = self.transportation_rates[i][j]
                    temp_min_row_index = i
                    temp_min_column_index = j

        self.find_min_values.append(temp_min)
        return temp_min_row_index, temp_min_column_index

    def _calc_value_element_matrix_base_plan(self, row_index, column_index):
        if self.value_point_of_departure[row_index] > self.value_destination[column_index]:
            self.matrix_base_plan[row_index][column_index] = min(self.value_point_of_departure[row_index], self.value_destination[column_index])
            self.value_point_of_departure = self.value_point_of_departure[row_index] - self.value_destination[column_index]
            self.value_destination = 0
        elif self.value_point_of_departure[row_index] < self.value_destination[column_index]:
            self.matrix_base_plan[row_index][column_index] = min(self.value_point_of_departure[row_index], self.value_destination[column_index])
            self.value_point_of_departure = 0
            self.value_destination = self.value_destination[column_index] - self.value_point_of_departure[row_index]

    def create_base_plan(self):
        self.matrix_base_plan = [[0 for i in range(self.count_value_destination)]
                                 for j in range(self.count_value_point_of_departure)]

        for i in range(self.count_value_point_of_departure):
            for j in range(self.count_value_destination):
                row_index, column_index = self._search_min_value_transportation_rates()
                if self.value_point_of_departure[row_index] != 0:
                    self._calc_value_element_matrix_base_plan(row_index, column_index)
                else:
                    self._calc_value_element_matrix_base_plan(row_index + 1, column_index)


if __name__ == '__main__':
    method = NorthwestCornerMethod()
    print("Введите количество груза на каждой точке отправления: ")
    method.set_value_point_of_departure(list(map(int, input().split())))
    print("Введите количество необходимого груза на каждой точке получения: ")
    method.set_value_destination(list(map(int, input().split())))

    print("Введите матрицу тарифов перевозок: ")
    method.set_transportation_rates([list(map(int, input().split()))
                                     for i in range(method.count_value_point_of_departure)])
    print(method.get_value_transportation_rates())

    method.create_base_plan()
    print(method.matrix_base_plan)

