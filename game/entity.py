from __future__ import annotations

import copy
import math
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union

from render_order import RenderOrder

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.consumable import Consumable
    from components.equipment import Equipment
    from components.equippable import Equippable
    from components.fighter import Fighter
    from components.inventory import Inventory
    from components.level import Level
    from game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    parent: Union[GameMap, Inventory]

    def __init__(
            self,
            parent: Optional[GameMap] = None,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            blocks_movement: bool = False,
            render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            self.parent = parent
            if hasattr(parent, 'entities'):
                parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        """Возвращает текущую игровую карту."""
        from game_map import GameMap  # Ленивый импорт для избежания циклических зависимостей

        if isinstance(self.parent, GameMap):
            return self.parent
        elif hasattr(self.parent, 'parent'):
            return self.parent.parent.gamemap
        raise RuntimeError("Entity is not placed on a GameMap")

    @property
    def engine(self):
        """Возвращает движок игры через родительскую связь."""
        return self.gamemap.engine if hasattr(self.gamemap, 'engine') else None

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Создает копию этого объекта в указанном месте."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """Помещает объект в новое место, обрабатывая переход между картами."""
        from game_map import GameMap  # Ленивый импорт

        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "parent"):
                if isinstance(self.parent, GameMap):
                    self.parent.entities.remove(self)
                elif hasattr(self.parent, 'items') and self in self.parent.items:
                    self.parent.items.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)

    def distance(self, x: int, y: int) -> float:
        """Вычисляет расстояние до указанных координат."""
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to(self, other: Entity) -> float:
        """Вычисляет расстояние до другого объекта."""
        return self.distance(other.x, other.y)

    def move(self, dx: int, dy: int) -> None:
        """Перемещает объект на указанное смещение."""
        self.x += dx
        self.y += dy


class Actor(Entity):
    """Класс для всех живых существ: игрока, NPC, монстров."""

    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            ai_cls: Type[BaseAI],
            equipment: Equipment,
            fighter: Fighter,
            inventory: Inventory,
            level: Level,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        self.ai: Optional[BaseAI] = ai_cls(self)
        self.equipment: Equipment = equipment
        self.fighter: Fighter = fighter
        self.inventory: Inventory = inventory
        self.level: Level = level

        # Устанавливаем ссылки на родителя для всех компонентов
        for component in (self.equipment, self.fighter, self.inventory, self.level):
            component.parent = self

    @property
    def is_alive(self) -> bool:
        """Проверяет, живо ли существо."""
        return bool(self.ai)


class Item(Entity):
    """Класс для всех предметов: оружия, зелий, свитков и т.д."""

    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            consumable: Optional[Consumable] = None,
            equippable: Optional[Equippable] = None,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )

        self.consumable = consumable
        self.equippable = equippable

        # Устанавливаем ссылки на родителя для компонентов
        if self.consumable:
            self.consumable.parent = self
        if self.equippable:
            self.equippable.parent = self