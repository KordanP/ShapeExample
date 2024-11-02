import mesa
from mesa.space import MultiGrid
import random

# Клас для стін, які створюватимуться на позиціях агентів при певних умовах
class Wall(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

# Змінив клас Walker, бо в оригіналі він нічого не робив,
# а тепер ходить стикається з іншими агентами і будує стіни
class Walker(mesa.Agent):
    def __init__(self, unique_id, model, heading=(1, 0)):
        super().__init__(unique_id, model)
        # Ініціалізація напрямку руху агента
        self.heading = heading
        # Можливі напрямки, куди агент може рухатися
        self.headings = {(1, 0), (0, 1), (-1, 0), (0, -1)}

    def step(self):
        # Виведення поточної позиції агента для налагодження
        print(self.pos)
        # Вибір нового напрямку випадковим чином
        self.heading = random.choice(list(self.headings))
        # Обчислення нової позиції агента на основі напрямку руху
        new_position = (self.pos[0] + self.heading[0], self.pos[1] + self.heading[1])

        # Перевірка, чи нова позиція знаходиться в межах сітки
        if not self.model.grid.out_of_bounds(new_position):
            # Отримання агентів у новій клітинці
            next_cell_contents = self.model.grid.get_cell_list_contents([new_position])
            # Якщо попереду є інший агент типу Walker
            if any(isinstance(agent, Walker) for agent in next_cell_contents):
                # Створення стіни на поточній позиції, якщо попереду інший Walker
                wall = Wall(self.model.next_id(), self.model)
                self.model.grid.place_agent(wall, self.pos)

                # Обчислення позиції назад
                back_position = (self.pos[0] - self.heading[0], self.pos[1] - self.heading[1])

                # Перевірка, чи можливо відступити назад
                if not self.model.grid.out_of_bounds(back_position):
                    back_cell_contents = self.model.grid.get_cell_list_contents([back_position])
                    if len(back_cell_contents) == 0:
                        # Якщо клітинка позаду порожня, агент переміщується назад
                        self.model.grid.move_agent(self, back_position)
                    else:
                        # Якщо назад немає місця, видаляємо агента з моделі
                        self.model.grid.remove_agent(self)
                        self.model.agents.remove(self)
                else:
                    # Якщо вихід назад за межами сітки, агент також видаляється
                    self.model.grid.remove_agent(self)
                    self.model.agents.remove(self)
            elif any(isinstance(agent, Wall) for agent in next_cell_contents):
                # Якщо в новій позиції є стіна, агент пропускає рух
                pass
            else:
                # Якщо попереду немає агентів або стін, агент рухається вперед
                self.model.grid.move_agent(self, new_position)


# Основний клас моделі, що створює агентів і керує ними
class ShapeExample(mesa.Model):
    def __init__(self, N=2, width=20, height=10):
        super().__init__()
        # Кількість агентів
        self.N = N
        # Доступні напрямки для агентів
        self.headings = ((1, 0), (0, 1), (-1, 0), (0, -1))
        # Змінив тип сітки, бо та що була не була сумісною з вбудовиними методами mesa
        self.grid = MultiGrid(width, height, torus=True)

        # Створення агентів Walker
        self.make_walker_agents()


    def make_walker_agents(self):
        for i in range(self.N):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            cell = self.grid[(x, y)]
            heading = self.random.choice(self.headings)

            a = Walker(i, self, heading)
            a.cell = cell
            # Добавив малювання агенту на сітку
            self.agents.add(a)
            self.grid.place_agent(a, (x, y))

    def step(self):
        # Виконання кроку для всіх агентів, які залишилися в моделі
        self.agents.shuffle_do("step")
