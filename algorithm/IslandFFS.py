import numpy as np

from algorithm.FSS import FSS


class IslandFSS(FSS):
    def __init__(self, schedule, num_islands=5,
                 migration_interval=10, num_fish=30, max_iter=100,
                 step_size=0.1, chaos_step_size=5):
        super().__init__(schedule, num_fish, max_iter, step_size, chaos_step_size)
        self.num_islands = num_islands
        self.migration_interval = migration_interval
        self.islands = [FSS(schedule, num_fish, max_iter // num_islands, step_size, chaos_step_size) for _ in
                        range(num_islands)]

    def optimize(self):
        # Оптимизация на основе островной модели
        for iteration in range(self.max_iter):
            scores = []
            for island in self.islands:
                island.optimize()
                if island.best_score < self.best_score:
                    self.best_solution = island.best_solution
                    self.best_score = island.best_score
                scores.extend(island.history)
            self.history.append(self.best_score)
            self.avg_history.append(np.mean(scores))
            self.std_dev_history.append(np.std(scores))
            if iteration % self.migration_interval == 0:
                self.migrate()

    def migrate(self):
        # Миграция лучших решений между островами
        for i in range(self.num_islands):
            next_island = (i + 1) % self.num_islands
            best_solution = self.islands[i].best_solution
            best_score = self.islands[i].best_score
            self.islands[next_island].best_solution = best_solution
            self.islands[next_island].best_score = best_score
