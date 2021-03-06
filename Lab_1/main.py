import sys
from math import *


class NorthwestCornerMethod:
    def __init__(self) -> None:
        self.matrix_base_plan = None  # опорный план
        self.missing_rows = []  # строки, которые пропускаем
        self.missing_columns = []  # столбцы, которые пропускаем
        self.potential = []
        self.u_i = []  # потенциал поставщиков
        self.v_j = []  # потенциал потребителей
        self.mask = []
        self.differences = []
        self.matrix_for_calculating_potentials = []
        self.mask_transportation_rates = []  # маска для тарифов перевозок
        self.count_value_point_of_departure: int = 0  # количество поставщиков
        self.count_value_destination: int = 0  # количество потребителей
        self.find_min_elements = []  # список всех найденных минимальных тарифов
        self.value_point_of_departure: [int] = []  # количество груза на каждой точке отправления (Запасы)
        self.value_destination: [int] = []  # количество необходимого груза на каждом пункте назначения (Потребности)
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

    def _generate_mask(self):
        self.mask_transportation_rates = [[0 for i in range(self.count_value_destination)]
                                          for j in range(self.count_value_point_of_departure)]

    def _set_min_value(self, row_index, column_index):
        self.matrix_base_plan[row_index][column_index] = min(self.value_point_of_departure[row_index],
                                                             self.value_destination[column_index])

    def _search_min_value_transportation_rates(self):  # поиск минимального тарифного плана
        temp_min = sys.maxsize
        temp_min_row_index = 0
        temp_min_column_index = 0
        for i in range(self.count_value_point_of_departure):
            for j in range(self.count_value_destination):
                if self.transportation_rates[i][j] < temp_min and self.mask_transportation_rates[i][j] != 1:
                    if not (i in self.missing_rows) and not (j in self.missing_columns):
                        temp_min = self.transportation_rates[i][j]
                        temp_min_row_index = i
                        temp_min_column_index = j

        self.mask_transportation_rates[temp_min_row_index][temp_min_column_index] = 1
        return temp_min_row_index, temp_min_column_index

    def _set_value_if_less(self, row_index, column_index):
        self._set_min_value(row_index, column_index)
        self.value_destination[column_index] = self.value_destination[column_index] - self.value_point_of_departure[
            row_index]
        self.value_point_of_departure[row_index] = 0
        self.missing_rows.append(row_index)

    def _set_value_if_greater(self, row_index, column_index):
        self._set_min_value(row_index, column_index)
        self.value_point_of_departure[row_index] = self.value_point_of_departure[row_index] - self.value_destination[
            column_index]
        self.value_destination[column_index] = 0
        self.missing_columns.append(column_index)

    def _set_value_if_equally(self, row_index, column_index):
        self.matrix_base_plan[row_index][column_index] = min(self.value_point_of_departure[row_index],
                                                             self.value_destination[column_index])
        self.value_point_of_departure[row_index] = 0
        self.value_destination[column_index] = 0
        self.missing_rows.append(row_index)
        self.missing_columns.append(column_index)

    def _set_value_if_equally_0(self):
        index_i = 0
        index_j = 0
        for i in range(self.count_value_point_of_departure):
            if self.value_point_of_departure[i] != 0:
                index_i = self.value_point_of_departure.index(self.value_point_of_departure[i])

        for j in range(self.count_value_destination):
            if self.value_destination[j] != 0:
                index_j = self.value_destination.index(self.value_destination[j])

        self.matrix_base_plan[index_i][index_j] = min(self.value_point_of_departure[index_i],
                                                      self.value_destination[index_j])
        self.value_point_of_departure[index_i] = 0
        self.value_destination[index_j] = 0

    def _calc_value_element_matrix_base_plan(self, row_index, column_index):
        if row_index == 0 and column_index == 0:
            self._set_value_if_equally_0()
        elif self.value_point_of_departure[row_index] > self.value_destination[column_index]:
            self._set_value_if_greater(row_index, column_index)
            i_temp, j_temp = self._search_min_value_transportation_rates()
            self._calc_value_element_matrix_base_plan(i_temp, j_temp)
        elif self.value_point_of_departure[row_index] < self.value_destination[column_index]:
            self._set_value_if_less(row_index, column_index)
            i_temp, j_temp = self._search_min_value_transportation_rates()
            self._calc_value_element_matrix_base_plan(i_temp, j_temp)
        elif self.value_point_of_departure[row_index] == self.value_destination[column_index]:
            self._set_value_if_equally(row_index, column_index)
            i_temp, j_temp = self._search_min_value_transportation_rates()
            self._calc_value_element_matrix_base_plan(i_temp, j_temp)

    def create_base_plan(self):
        self._generate_mask()
        self.matrix_base_plan = [[0 for i in range(self.count_value_destination)]
                                 for j in range(self.count_value_point_of_departure)]

        i_temp, j_temp = self._search_min_value_transportation_rates()
        self._calc_value_element_matrix_base_plan(i_temp, j_temp)

    def calc_value_objective_function(self):  # расчет значения опорного плана
        result = 0
        for i in range(self.count_value_point_of_departure):
            for j in range(self.count_value_destination):
                if self.matrix_base_plan[i][j] != 0:
                    result += int(self.transportation_rates[i][j]) * int(self.matrix_base_plan[i][j])
                    "Из {} склада необходимо груз направить в {} магазин ({} единиц)".format(i,j, self.matrix_base_plan[i][j])

        return result

    def _generate_mask_for_transportation_rates(
            self):  # для обозначения строк и столбцов среди которых ищем минимальное значение
        self.mask = [[False for i in range(self.count_value_destination)]
                     for j in range(self.count_value_point_of_departure)]

        for i in range(self.count_value_point_of_departure):
            for j in range(self.count_value_destination):
                if self.matrix_base_plan[i][j] == 0:
                    self.mask[i][j] = True

    def _zero_delivery_placement(self, row_index, column_index):  # размещение нулевой поставки (u_i == v_j == 0)
        temp_min = sys.maxsize
        min_row_index = 0
        min_column_index = 0
        for i in range(self.count_value_point_of_departure):
            for j in range(self.count_value_destination):
                if i != row_index:
                    if self.mask[i][j] and j == column_index and self.transportation_rates[i][j] < temp_min:
                        temp_min = self.transportation_rates[i][j]
                        min_row_index = i
                        min_column_index = j
                elif i == row_index:
                    if self.mask[i][j] and self.transportation_rates[i][j] < temp_min:
                        temp_min = self.transportation_rates[i][j]
                        min_row_index = i
                        min_column_index = j

        return min_row_index, min_column_index

    @staticmethod
    def _replace_with_null(list_values: [int]) -> None:
        for i in range(len(list_values)):
            if list_values[i] == (-sys.maxsize):
                list_values[i] = 0

    @staticmethod
    def _check(potentials: [int]):
        for i in range(len(potentials)):
            if potentials[i] == (-sys.maxsize):
                return False
        return True

    def _first_pass(self):  # метод для генерации матрицы для вычисления потенциалов поставщиков и потребителей
        self.matrix_for_calculating_potentials = [[0 for i in range(self.count_value_destination)]
                                                  for j in range(self.count_value_point_of_departure)]
        self.u_i[0] = 0
        for i in range(self.count_value_point_of_departure):
            for j in range(self.count_value_destination):
                if self.matrix_base_plan[i][j] != 0:
                    if self.u_i[i] != (-sys.maxsize) and self.v_j[j] == (-sys.maxsize):
                        self.v_j[j] = self.transportation_rates[i][j] - self.u_i[i]
                    elif self.v_j[j] != (-sys.maxsize) and self.u_i[i] == (-sys.maxsize):
                        self.u_i[i] = self.transportation_rates[i][j] - self.v_j[j]

    def _first_back_pass(self):
        i_p = 0
        j_p = 0
        for i in range(self.count_value_point_of_departure - 1, -1, -1):
            for j in range(self.count_value_destination - 1, -1, -1):
                if self.matrix_base_plan[i][j] != 0:
                    if self.u_i[i] != (-sys.maxsize) and self.v_j[j] == (-sys.maxsize):
                        self.v_j[j] = self.transportation_rates[i][j] - self.u_i[i]
                    elif self.v_j[j] != (-sys.maxsize) and self.u_i[i] == (-sys.maxsize):
                        self.u_i[i] = self.transportation_rates[i][j] - self.v_j[j]
                    elif self.u_i[i] == (-sys.maxsize) and self.v_j[j] == (-sys.maxsize):
                        i_p, j_p = self._zero_delivery_placement(i, j)
                        if self.u_i[i_p] != (-sys.maxsize):
                            self.v_j[j_p] = self.transportation_rates[i_p][j_p] - self.u_i[i_p]
                            self.u_i[i_p] = self.transportation_rates[i_p][j_p] - self.v_j[j_p]
                            if self.u_i[i] != (-sys.maxsize) and self.v_j[j] == (-sys.maxsize):
                                self.v_j[j] = self.transportation_rates[i][j] - self.u_i[i]
                            elif self.v_j[j] != (-sys.maxsize) and self.u_i[i] == (-sys.maxsize):
                                self.u_i[i] = self.transportation_rates[i][j] - self.v_j[j]
                        else:
                            self.u_i[i_p] = self.transportation_rates[i_p][j_p] - self.v_j[j_p]
                            self.v_j[j_p] = self.transportation_rates[i_p][j_p] - self.u_i[i_p]
                            if self.u_i[i] != (-sys.maxsize) and self.v_j[j] == (-sys.maxsize):
                                self.v_j[j] = self.transportation_rates[i][j] - self.u_i[i]
                            elif self.v_j[j] != (-sys.maxsize) and self.u_i[i] == (-sys.maxsize):
                                self.u_i[i] = self.transportation_rates[i][j] - self.v_j[j]

    def improvement_transportation_plan(self):  # нахлждение потенциалов для опорного плана
        self._generate_mask_for_transportation_rates()

        self.potential = [[0 for i in range(self.count_value_destination + 1)]
                          for j in range(self.count_value_point_of_departure + 1)]

        self.u_i = [(-sys.maxsize) for i in range(self.count_value_point_of_departure)]
        self.v_j = [(-sys.maxsize) for j in range(self.count_value_destination)]

        self._first_pass()
        self._first_back_pass()

        self._replace_with_null(self.v_j)
        self._replace_with_null(self.u_i)

    def calc_difference_free_cells(self):
        self.differences = [[sys.maxsize for i in range(self.count_value_destination)]
                            for j in range(self.count_value_point_of_departure)]
        for i in range(self.count_value_point_of_departure):
            for j in range(self.count_value_destination):
                if self.matrix_base_plan[i][j] == 0:
                    self.differences[i][j] = self.transportation_rates[i][j] - (self.u_i[i] + self.v_j[j])

    def check_optimality(self):
        for i in range(self.count_value_point_of_departure):
            for j in range(self.count_value_destination):
                if self.differences[i][j] < 0:
                    return False
        return True

    def print_res(self):
        for i in range(self.count_value_point_of_departure):
            for j in range(self.count_value_destination):
                if self.matrix_base_plan[i][j] != 0:
                    print('Из {} склада необходимо груз направить в {} магазин ({} единиц)'.format(i + 1, j + 1, self.matrix_base_plan[i][j]))


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
    print("Значение целевой функции равно: {0}".format(method.calc_value_objective_function()))
    method.improvement_transportation_plan()
    print(method.u_i)
    print(method.v_j)
    print("Определенные разности для свободных клеток: ")
    method.calc_difference_free_cells()
    print(method.differences)
    if method.check_optimality():
        print("Данный план является оптимальным, тк все оценки свободных клеток удовлетворяют условию"
              "u_i + v_j <= c_ij")
        method.print_res()
    else:
        print("Данный план не оптимальный производим улучшение плана")