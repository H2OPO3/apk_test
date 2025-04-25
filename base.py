import pygame
import json
import sys

pygame.init()

# Основные настройки окна игры
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Платформер с уровнем из файла")

# Цветовые константы
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 40, 40)
        self.y_speed = 0
        self.x_speed = 0
        self.gravity = 0.5
        self.on_ground = False
        self.jump_request = False  # Флаг запроса прыжка

    def update(self, objects):
        # Гравитация
        self.y_speed += self.gravity
        
        # Обработка вертикального движения и столкновений
        self.rect.y += self.y_speed
        for obj in objects:
            if self.rect.colliderect(obj["rect"]):
                if self.y_speed > 0:  # Столкновение снизу вверх (приземление)
                    self.rect.bottom = obj["rect"].top
                    self.y_speed = 0
                    self.on_ground = True
                    if self.jump_request:  # Выполняем прыжок сразу после приземления
                        self.jump()
                        self.jump_request = False
                elif self.y_speed < 0:  # Столкновение сверху вниз (потолок)
                    self.rect.top = obj["rect"].bottom
                    self.y_speed = 0
            
        # Горизонтальное движение и проверка столкновений
        self.rect.x += self.x_speed
        for obj in objects:
            if self.rect.colliderect(obj["rect"]):
                if self.x_speed > 0:  # Столкновение справа от стенки
                    self.rect.right = obj["rect"].left
                elif self.x_speed < 0:  # Столкновение слева от стенки
                    self.rect.left = obj["rect"].right
                    
        # Замедляем скорость перемещения
        self.x_speed *= 0.8

    def jump(self):
        if self.on_ground:
            self.y_speed = -12

    def move_left(self):
        self.x_speed -= 5

    def move_right(self):
        self.x_speed += 5

# Загрузка данных уровней из внешнего файла
def load_level(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['objects']

# Игрок
player = Player()

# Загружаем уровень из файла level.json
level_data = load_level('level.json')

# Кнопки управления
jump_button = pygame.Rect(20, 20, 100, 50)
move_left_button = pygame.Rect(200, 20, 100, 50)
move_right_button = pygame.Rect(380, 20, 100, 50)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Получение состояния мыши и клавиш клавиатуры
    mouse_pressed = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    
    # Запрашиваем прыжок при нажатии клавиши W или кнопки прыжка
    if keys[pygame.K_w] or (jump_button.collidepoint(mouse_pos) and mouse_pressed):
        player.jump_request = True
    
    # Движение влево/вправо
    if keys[pygame.K_a] or (move_left_button.collidepoint(mouse_pos) and mouse_pressed):
        player.move_left()
    if keys[pygame.K_d] or (move_right_button.collidepoint(mouse_pos) and mouse_pressed):
        player.move_right()
    
    # Обновляем состояние игрока
    player.update(level_data)
    
    # Рисуем элементы
    pygame.draw.rect(screen, GREEN, jump_button)
    pygame.draw.rect(screen, BLUE, move_left_button)
    pygame.draw.rect(screen, BLUE, move_right_button)
    pygame.draw.rect(screen, BLUE, player.rect)
    for obj in level_data:
        pygame.draw.rect(screen, WHITE, obj["rect"])
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()