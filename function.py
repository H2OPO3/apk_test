import pygame
import math
import sys
import json
def dist(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def load_level(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        for obj in data['objects']:
            obj["rect"] = pygame.Rect(*obj["rect"])
        return data['objects']
    except FileNotFoundError:
        print(f'Файл {file_path} не найден.')
        exit()
        
def move_player_towards_black_hole(player, black_hole_center, black_hole_radius, base_speed=5000, threshold=100, max_distance=500, epsilon=1):
    player_x, player_y = player.rect.center
    black_hole_x, black_hole_y = black_hole_center

    diff_x = black_hole_x - player_x
    diff_y = black_hole_y - player_y

    distance = (diff_x ** 2 + diff_y ** 2) ** 0.5

    # Корректируем расстояние с учётом радиуса черной дыры,
    # чтобы притяжение начиналось от края круга, а не от центра
    adjusted_distance = max(distance - black_hole_radius, 0)

    if adjusted_distance < threshold or adjusted_distance > max_distance:
        return 0.0, 0.0

    # Сила притяжения обратно пропорциональна квадрату расстояния от края круга
    force = base_speed / ((adjusted_distance + epsilon) ** 2)

    direction_x = diff_x / distance if distance != 0 else 0
    direction_y = diff_y / distance if distance != 0 else 0

    delta_speed_x = direction_x * force
    delta_speed_y = direction_y * force

    player.x_speed += delta_speed_x
    player.y_speed += delta_speed_y

    MAX_SPEED = 20
    player.x_speed = max(-MAX_SPEED, min(player.x_speed, MAX_SPEED))
    player.y_speed = max(-MAX_SPEED, min(player.y_speed, MAX_SPEED))

    return delta_speed_x, delta_speed_y
    
    
