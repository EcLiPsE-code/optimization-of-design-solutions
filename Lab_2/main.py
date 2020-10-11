import sys

class HungarianMethod:
    def __init__(self) -> None:
        self.matrix_base_plan = []  # первоначальный опорный план
        self.transportation_rates = None  # матрица таррифов
        self.mechanisms = []  # механизмы, которые используются для выполнения работы
        self.objects = []  # объекты, работу над которыми необходимо выполнить
        self.count_mechanisms: int = None  # количество механизмов
        self.count_objects: int = None # количество объектов, работу над которыми необходимо выполнить

    def set_count_mechanisms(self, count) -> None:
        self.count_mechanisms = count

    def set_count_objects(self, count) -> None:
        self.count_objects = count

    def set_transportation_rates(self, transportation_rates: [int]) -> None:
        self.transportation_rates = transportation_rates

    def get_count_mechanisms(self) -> int:
        return self.count_mechanisms

    def get_count_objects(self) -> int:
        return self.count_objects

    def get_transportation_rates(self) -> [int]:
        return self.transportation_rates

    def line_casting(self): # приведение по строкам
        lines_casting = []
        for i in range(self.get_count_mechanisms()):
            temp_min = -sys.maxsize
            for j in range(self.get_count_objects()):
                if self.transportation_rates[i][j] < temp_min:
                    temp_min = self.transportation_rates[i][j]
            lines_casting.append(temp_min)

    def column_cast(self): # приведение по столбцам
        pass

if __name__ == "__main__":
    method = HungarianMethod()
    print("Количество механизмов, которые используются для выполнения работы на объектах")
    method.set_count_mechanisms(int(input()))
    print("Количество объектов, над которыми необходимо выполнить работу")
    method.set_count_objects(int(input()))
    print("Введите матрицу тарифов")
    method.set_transportation_rates([list(map(int, input().split()))
                                     for i in range(method.get_count_mechanisms())])
    print(method.get_transportation_rates())
