import random
import numpy as np

from algorithm.Fish import Fish


class FSS:
    def __init__(self, schedule, num_fish = 30,
                 max_iter = 100, step_size = 0.1, chaos_step_size = 5):
        # Инициализация алгоритма оптимизации
        self.schedule = schedule # TODO поменять контейнеры на расписание
        self.num_fish = num_fish
        self.max_iter = max_iter
        self.step_size = step_size
        self.chaos_step_size = chaos_step_size
        self.population = [self.initialize_solution() for _ in range(num_fish)]
        self.best_solution = None
        self.best_score = float('inf')
        self.history = []  # История лучших результатов
        self.avg_history = []  # Среднее значение оценок
        self.std_dev_history = []  # Стандартное отклонение оценок
        self.fish_swarm = [Fish(random.uniform(0, 100), random.uniform(0, 100), weight=2) for _ in range(num_fish)]  # Инициализация веса

    def initialize_solution(self):
        # Инициализация начального решения
        solution = [[] for _ in self.containers]
        for item in self.items:
            chosen_container = random.choice(range(len(self.containers)))
            solution[chosen_container].append(item)
        return solution

    def evaluate(self, solution) :
        # Оценка решения на основе нарушений ограничений
        penalty = 0
        for i, schedule in enumerate(self.containers):
            container.items = solution[i]
            container.current_volume = sum(item.volume for item in solution[i])
            container.current_weight = sum(item.weight for item in solution[i])

            if container.current_volume > container.max_volume:
                penalty += (container.current_volume - container.max_volume) * 10
            if container.current_weight > container.max_weight:
                penalty += (container.current_weight - container.max_weight) * 10

            for item in container.items:
                if item.fragile and container.items.index(item) != 0:
                    penalty += 100

            for item in container.items:
                for incompatible_id in item.incompatible_items:
                    if any(incompatible_id == i.id for i in container.items):
                        penalty += 40

            for i, item in enumerate(container.items):
                if item.priority == 1 and i != 0:
                    penalty += 20
                if item.priority > 1:
                    prev_item = container.items[i - 1]
                    if prev_item.priority > item.priority:
                        penalty += 80

        total_unused_volume = sum(container.get_unused_volume() for container in self.containers)
        return penalty

    def optimize(self):
        # Оптимизация решения
        for iteration in range(self.max_iter):
            scores = []
            for i in range(self.num_fish):
                self.fish_swarm[i].move_chaotically(self.chaos_step_size)
                schedule.
                new_solution = self.perturb_solution(self.population[i])
                new_score = self.evaluate(new_solution)
                scores.append(new_score)
                if new_score < self.best_score:
                    self.best_solution = new_solution
                    self.best_score = new_score
                delta_fitness = new_score - self.evaluate(self.population[i])
                self.fish_swarm[i].update_weight(delta_fitness)
                self.population[i] = new_solution
            self.history.append(self.best_score)
            self.avg_history.append(np.mean(scores))
            self.std_dev_history.append(np.std(scores))

    def perturb_solution(self, solution):
        # Внесение изменений в решение, перемещая случайные предметы между двумя контейнерами
        new_solution = [container[:] for container in solution]  # Создание копии решения
        container1, container2 = random.sample(range(len(new_solution)), 2)  # Выбор двух случайных контейнеров
        if new_solution[container1] and new_solution[container2]:  # Проверка наличия предметов в обоих контейнерах
            item1, item2 = random.choice(new_solution[container1]), random.choice(new_solution[container2])  # Выбор двух случайных предметов
            new_solution[container1].remove(item1)  # Удаление первого предмета из первого контейнера
            new_solution[container2].remove(item2)  # Удаление второго предмета из второго контейнера
            new_solution[container1].append(item2)  # Добавление второго предмета в первый контейнер
            new_solution[container2].append(item1)  # Добавление первого предмета во второй контейнер
        return new_solution

    def print_solution(self, solution):
        # Вывод решения на экран
        for i, container in enumerate(solution):
            print(f"Контейнер {i + 1} предмет:")
            for j, item in enumerate(container):
                print(f"- Предмет {item.id}, Позиция {j + 1}")
