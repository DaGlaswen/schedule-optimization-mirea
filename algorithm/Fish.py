import random

class Fish:
    def __init__(self, x, y, speed = 1.0, weight= 1.0):
        self.x = x
        self.y = y
        self.speed = speed
        self.weight = weight

    def move_chaotically(self, step_size):
        # Перемещение рыбы хаотичным образом в пределах заданного шага
        self.x += random.uniform(-step_size, step_size)
        self.y += random.uniform(-step_size, step_size)

    def update_weight(self, delta_fitness):
        # Обновление веса рыбы на основе изменения показателя приспособленности
        self.weight += delta_fitness / max(1, abs(delta_fitness))
