from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from components.base_component import BaseComponent
from exceptions import Impossible
import color
if TYPE_CHECKING:
    from entity import Actor, Item
    from game_map import GameMap


class Inventory(BaseComponent):
    parent: Actor  # Владелец инвентаря

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []
        self.gold: int = 0

    @property
    def engine(self):
        """Получает движок игры через родительский Actor."""
        return self.parent.gamemap.engine if self.parent and self.parent.gamemap else None

    def add_item(self, item: Item) -> None:
        """Добавляет предмет в инвентарь."""
        if len(self.items) >= self.capacity:
            raise Impossible("Your inventory is full.")

        item.parent = self  # Устанавливаем ссылку на инвентарь
        self.items.append(item)

        if self.engine:
            self.engine.message_log.add_message(f"You picked up {item.name}!")

    def remove_item(self, item: Item) -> None:
        """Удаляет предмет из инвентаря."""
        if item in self.items:
            item.parent = None
            self.items.remove(item)

    def add_gold(self, amount: int) -> None:
        """Добавляет золото в инвентарь."""
        self.gold += amount
        if self.engine:
            self.engine.message_log.add_message(f"You picked up {amount} gold.", color.gold)

    def remove_gold(self, amount: int) -> bool:
        """Удаляет золото, если его достаточно."""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def drop_item(self, item: Item) -> None:
        """Выбрасывает предмет на карту."""
        self.remove_item(item)
        item.place(self.parent.x, self.parent.y, self.parent.gamemap)
        if self.engine:
            self.engine.message_log.add_message(f"You dropped the {item.name}.")

    def buy_health_potion(self, cost: int = 10) -> bool:
        """Покупает зелье здоровья."""
        if not self.remove_gold(cost):
            raise Impossible("Not enough gold.")

        # Ищем существующее зелье в инвентаре
        potion = next((i for i in self.items if i.name == "Health Potion"), None)

        if potion:
            # Увеличиваем количество зарядов, если зелье уже есть
            if hasattr(potion.consumable, 'charges'):
                potion.consumable.charges += 1
        else:
            # Создаем новое зелье
            from entity_factories import health_potion
            self.add_item(health_potion())

        if self.engine:
            self.engine.message_log.add_message(f"You bought a Health Potion for {cost} gold!", color.gold)
        return True

    def use_item(self, item: Item) -> None:
        """Использует предмет."""
        if item not in self.items:
            raise Impossible("Item not in inventory!")

        if hasattr(item, 'consumable') and item.consumable:
            try:
                item.consumable.activate()
                # Удаляем предмет, если он одноразовый
                if not getattr(item.consumable, 'charges', 1) > 0:
                    self.remove_item(item)
            except Impossible as e:
                if self.engine:
                    self.engine.message_log.add_message(str(e), color.impossible)