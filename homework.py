class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(
            self,
            training_type: str,
            duration: float,
            distance: float,
            speed: float,
            calories: float
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Создать строку сообщения, которое распечатается в консоль."""

        message = ''.join((
            f'Тип тренировки: {self.training_type}; ',
            f'Длительность: {self.duration:.3f} ч.; ',
            f'Дистанция: {self.distance:.3f} км; ',
            f'Ср. скорость: {self.speed:.3f} км/ч; ',
            f'Потрачено ккал: {self.calories:.3f}.'))
        return message


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_type = type(self).__name__

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MINUTES_IN_HOUR = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def get_duration_in_minutes(self) -> float:
        """Перевести часы тренировки в минуты."""

        minutes = self.duration * self.MINUTES_IN_HOUR
        return minutes

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        info = InfoMessage(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )
        return info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_RATIO_1: int = 18
    CALORIES_RATIO_2: int = 20
    M_IN_KM: int = 1000

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        spent_calories = ((self.CALORIES_RATIO_1 *
                           self.get_mean_speed()
                           - self.CALORIES_RATIO_2) * self.weight
                          / self.M_IN_KM * self.get_duration_in_minutes()
                          )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_RATIO_1: float = 0.035
    CALORIES_RATIO_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        first_part = self.CALORIES_RATIO_1 * self.weight
        second_part = self.get_mean_speed()**2 // self.height
        third_part = self.CALORIES_RATIO_2 * self.weight
        last_part = self.get_duration_in_minutes()
        spent_calories = (first_part + second_part * third_part) * last_part
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_RATIO_1: float = 1.1
    CALORIES_RATIO_2: int = 2

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Вычислить среднюю скорость."""

        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        mean_speed = Swimming.get_mean_speed(self)
        spent_calories = ((mean_speed + self.CALORIES_RATIO_1)
                          * self.CALORIES_RATIO_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    dictionary_to_read = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type in dictionary_to_read:
        my_instance = dictionary_to_read[workout_type](*data)
        return my_instance


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    info = info.get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
