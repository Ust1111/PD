
# Roguelike-игра на Python с использованием tcod

## Содержание

1. [Описание проекта](#описание-проекта)  
2. [Последовательность действий по исследованию](#последовательность-действий-по-исследованию)  
3. [Техническое руководство](#техническое-руководство)  
   - [Установка зависимостей](#установка-зависимостей)  
   - [Создание проекта](#создание-проекта)  
   - [Отрисовка карты и персонажа](#отрисовка-карты-и-персонажа)  
   - [Добавление монет и магазина](#добавление-монет-и-магазина)  
   - [Экран "Об игре"](#экран-об-игре)  
4. [Примеры кода](#примеры-кода)  
5. [Иллюстрации](#иллюстрации)  
6. [Результаты и Git-репозиторий](#результаты-и-git-репозиторий)

---

## Описание проекта

Это консольная roguelike-игра, реализованная на Python с использованием библиотеки `tcod`. Проект выполнен по обучающему курсу [https://rogueliketutorials.com/](https://rogueliketutorials.com/) с добавлением собственных механик:

- Сбор монет
- Экран магазина, где можно тратить монеты
- Экран "Об игре", вызываемый по клавише F1

Игра построена по канонам классических roguelike: сгенерированные подземелья, пошаговые действия, ASCII-графика.

---

## Последовательность действий по исследованию

1. Изучен жанр roguelike: особенности геймплея, генерации уровней, интерфейса.
2. Освоена библиотека [`tcod`](https://python-tcod.readthedocs.io/en/latest/) для создания ASCII-игр.
3. Пройден пошаговый туториал, реализующий базовую игру.
4. Внесены собственные улучшения:
   - игровая валюта (монеты),
   - магазин для покупки предметов,
   - информационный экран об игре.
5. Реализация функций была протестирована вручную.
6. Итоговый проект размещён в GitHub-репозитории.

---

## Техническое руководство

### Установка зависимостей

Установите необходимые библиотеки с помощью pip:

```bash
pip install tcod numpy
```

---

### Создание проекта

Создайте папку и структуру файлов:

```bash
mkdir roguelike-game
cd roguelike-game
```

Структура проекта:

```
roguelike-game/
├── engine.py
├── entity.py
├── game_map.py
├── input_handlers.py
├── main.py
├── render_functions.py
└── shop.py
```

---

### Отрисовка карты и персонажа

В `engine.py` добавим функцию отрисовки:

```python
def render(console, context, game_map, entities):
    game_map.render(console)
    for entity in entities:
        console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
    context.present(console)
```

---

### Добавление монет и магазина

Добавим переменную `coins` и функции покупки:

```python
# В классе игрока
self.coins = 0

# shop.py
def open_shop(player):
    print("Добро пожаловать в магазин!")
    if player.coins >= 5:
        player.coins -= 5
        print("Вы купили зелье!")
    else:
        print("Недостаточно монет!")
```

Монеты можно размещать на карте как отдельные объекты, и при контакте с игроком они добавляются в счёт.

---

### Экран "Об игре"

Создаём экран информации об игре, вызываемый по F1:

```python
# input_handlers.py
if event.sym == tcod.event.K_F1:
    return {"show_about": True}

# engine.py
def show_about_screen(console):
    console.clear()
    console.print(0, 0, "Roguelike-игра\nАвторы: Команда XYZ\nНажмите любую клавишу для выхода.")
    tcod.console_flush()
    tcod.event.wait()
```

---

## Примеры кода

### Игровая сущность

```python
# entity.py
class Entity:
    def __init__(self, x, y, char, color, name):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
```

### Обработка нажатий клавиш

```python
# input_handlers.py
def handle_keys(event):
    if event.sym == tcod.event.K_UP:
        return {'move': (0, -1)}
    elif event.sym == tcod.event.K_DOWN:
        return {'move': (0, 1)}
    elif event.sym == tcod.event.K_LEFT:
        return {'move': (-1, 0)}
    elif event.sym == tcod.event.K_RIGHT:
        return {'move': (1, 0)}
    elif event.sym == tcod.event.K_F1:
        return {'show_about': True}
```

---

## Иллюстрации

_(Вставьте изображения в папку `images/` и отредактируйте пути, если нужно)_

1. Карта уровня с монетами  
   ![Карта](images/map.png)

2. Персонаж в подземелье  
   ![Игрок](images/player.png)

3. Меню магазина  
   ![Магазин](images/shop.png)

4. Экран "Об игре"  
   ![Об игре](images/about.png)

5. Структура проекта  
   ![Структура](images/structure.png)

---

## Результаты и Git-репозиторий

Игра завершена и загружена в Git-репозиторий.

**Ссылка на репозиторий:**

🔗 [https://github.com/yourusername/roguelike-project](https://github.com/yourusername/roguelike-project)

Проект содержит:
- Полный исходный код
- README-файл
- Снимки экрана
- Инструкции по запуску

---
