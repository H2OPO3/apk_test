# level_manager.py
from player import Player
from function import load_level
from obj import create_black_hole  # если есть

levels = ['level1.json', 'level2.json', 'level3.json']
current_level_index = 0

def load_level_by_index(index):
    """
    Загружает уровень по индексу и создаёт игрока.
    Возвращает кортеж (level_data, player).
    """
    level_path = levels[index]
    level_data = load_level(level_path)
    player = Player(level_data)
    return level_data, player

def go_to_next_level():
    """
    Переходит на следующий уровень, если он есть.
    Возвращает (level_data, player) или None, если уровни закончились.
    """
    global current_level_index
    if current_level_index + 1 < len(levels):
        current_level_index += 1
        return load_level_by_index(current_level_index)
    return None

def go_to_previous_level():
    """
    Переходит на предыдущий уровень, если он есть.
    Возвращает (level_data, player) или None, если это первый уровень.
    """
    global current_level_index
    if current_level_index - 1 >= 0:
        current_level_index -= 1
        return load_level_by_index(current_level_index)
    return None
