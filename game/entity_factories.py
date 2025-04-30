from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

# Функция для создания игрока
def player() -> Actor:
    return Actor(
        char="@",
        color=(255, 255, 255),
        name="Player",
        ai_cls=HostileEnemy,
        equipment=Equipment(),
        fighter=Fighter(hp=30, base_defense=1, base_power=2),
        inventory=Inventory(capacity=26),
        level=Level(level_up_base=200),
    )

# Фабрика для создания орков
def orc() -> Actor:
    return Actor(
        char="o",
        color=(63, 127, 63),
        name="Orc",
        ai_cls=HostileEnemy,
        equipment=Equipment(),
        fighter=Fighter(hp=10, base_defense=0, base_power=3),
        inventory=Inventory(capacity=0),
        level=Level(xp_given=35),
    )

# Фабрика для создания троллей
def troll() -> Actor:
    return Actor(
        char="T",
        color=(0, 127, 0),
        name="Troll",
        ai_cls=HostileEnemy,
        equipment=Equipment(),
        fighter=Fighter(hp=16, base_defense=1, base_power=4),
        inventory=Inventory(capacity=0),
        level=Level(xp_given=100),
    )

# Фабрика для создания золота
def gold_pile() -> Item:
    return Item(
        char="$",
        color=(255, 165, 0),  # Золотой цвет
        name="Gold",
        consumable=consumable.GoldConsumable(amount=1)  # Значение по умолчанию
    )

# Фабрика для создания свитка замешательства
def confusion_scroll() -> Item:
    return Item(
        char="~",
        color=(207, 63, 255),
        name="Confusion Scroll",
        consumable=consumable.ConfusionConsumable(number_of_turns=10),
    )

# Фабрика для создания свитка огненного шара
def fireball_scroll() -> Item:
    return Item(
        char="~",
        color=(255, 0, 0),
        name="Fireball Scroll",
        consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
    )

# Фабрика для создания свитка молнии
def lightning_scroll() -> Item:
    return Item(
        char="~",
        color=(255, 255, 0),
        name="Lightning Scroll",
        consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
    )

# Фабрика для создания кинжала
def dagger() -> Item:
    return Item(
        char="/",
        color=(0, 191, 255),
        name="Dagger",
        equippable=equippable.Dagger()
    )

# Фабрика для создания меча
def sword() -> Item:
    return Item(char="/", color=(0, 191, 255), name="Sword", equippable=equippable.Sword())

# Фабрика для создания кожаной брони
def leather_armor() -> Item:
    return Item(
        char="[",
        color=(139, 69, 19),
        name="Leather Armor",
        equippable=equippable.LeatherArmor(),
    )

# Фабрика для создания кольчуги
def chain_mail() -> Item:
    return Item(
        char="[",
        color=(139, 69, 19),
        name="Chain Mail",
        equippable=equippable.ChainMail()
    )

# Фабрика для создания зелья здоровья
def health_potion() -> Item:
    return Item(
        char="!",
        color=(127, 0, 255),
        name="Health Potion",
        consumable=consumable.HealingConsumable(amount=4),
    )
