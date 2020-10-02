class NorthwestCornerMethod:  # класс, описывающий метод северо западного угла
    def __init__(self) -> None:
        self.count_point_of_departure: int = 0  # количество точек отправления груза
        self.count_destination: int = 0  # количество пунктов назначения
        self.value_point_of_departure: [int] = []  # количество груза на каждой точке отправления (потребности)
        self.value_destination: int = 0  # количество необходимого груза на каждом пункте назначения (запасы)
        self.transportation_rates: int = 0  # тарифы перевозок

    def set_count_point_of_departure(self, count_point_of_departure:int) -> None:
        self.count_point_of_departure = count_point_of_departure

    def set_count_destination(self, count_destination:int) -> None:
        self.count_destination = count_destination

    def set_value_point_of_departure(self, values_point_of_departure: [int]) -> None:
        self.value_point_of_departure = values_point_of_departure

    def set_value_destination(self, values_destination: [int]) -> None:
        self.value_destination = values_destination

    def set_transportation_rates(self, transportation_rates: [int]) -> None:
        self.transportation_rates = transportation_rates


if __name__ == '__main__':
    pass
