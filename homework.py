from dataclasses import dataclass, asdict


@dataclass()
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    training_type: str
    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self):
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    M_IN_KM: int = 1000
    MINUTES_IN_HOUR = 60
    LEN_STEP: float = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def get_duration_in_minutes(self) -> float:
        """Перевести часы тренировки в минуты."""

        return self.duration * self.MINUTES_IN_HOUR

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        info = InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )
        return info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_HEIGHT_FACTOR: float = 18
    CALORIES_AGE_FACTOR: float = 20

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        basal_metabolic_rate = (
            self.CALORIES_HEIGHT_FACTOR
            * self.get_mean_speed()
            - self.CALORIES_AGE_FACTOR
        )
        minutes = self.get_duration_in_minutes()
        spent_calories = (
            basal_metabolic_rate
            * self.weight
            / self.M_IN_KM * minutes
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    ADJUSTED_FOR_MEN: float = 0.035
    SPORTSWALKING_EXERCISE_MODIFIER: float = 0.029

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        adjusted_weight = self.ADJUSTED_FOR_MEN * self.weight
        speed_square = self.get_mean_speed()**2
        time = self.get_duration_in_minutes()
        spent_calories = (
            (adjusted_weight + speed_square // self.height
             * self.SPORTSWALKING_EXERCISE_MODIFIER
             * self.weight) * time
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    EXERCISE_INTENSITY: float = 1.1
    SWIMMING_EXERCISE_MODIFIER: float = 2

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Вычислить среднюю скорость."""

        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        spent_calories = (
            (Swimming.get_mean_speed(self) + self.EXERCISE_INTENSITY)
            * self.SWIMMING_EXERCISE_MODIFIER * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_cypher = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    if workout_type not in training_cypher:
        raise ValueError(f'This key is not found: {workout_type}')
    return training_cypher[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info().get_message()
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
