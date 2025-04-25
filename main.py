import pygame
import sys
import math
import os
from import_from import *  # Импортируем все необходимые классы и функции

pygame.init()

infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h

screen = pygame.display.set_mode((1600, 1600), pygame.FULLSCREEN)
pygame.display.set_caption("Платформер с уровнем из блока и камерой")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Класс камеры с плавной слежкой
class Camera:
    def __init__(self, level_width, level_height, screen_width, screen_height):
        self.level_width = level_width
        self.level_height = level_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.target_offset_x = 0.0
        self.target_offset_y = 0.0

    def update(self, target_rect, lerp_factor=0.15):
        self.target_offset_x = target_rect.centerx - self.screen_width // 2
        self.target_offset_y = target_rect.centery - self.screen_height // 2

        self.target_offset_x = max(0, min(self.target_offset_x, self.level_width - self.screen_width))
        self.target_offset_y = max(0, min(self.target_offset_y, self.level_height - self.screen_height))

        self.offset_x += (self.target_offset_x - self.offset_x) * lerp_factor
        self.offset_y += (self.target_offset_y - self.offset_y) * lerp_factor

    def apply(self, rect):
        return rect.move(-int(self.offset_x), -int(self.offset_y))

# Функция для загрузки уровня и вычисления размеров
def load_level(level_blocks):
    level_data = parse_level_from_blocks(level_blocks, block_size=SCREEN_WIDTH/6)
    level_width = max(obj["rect"].right for obj in level_data) if level_data else SCREEN_WIDTH
    level_height = max(obj["rect"].bottom for obj in level_data) if level_data else SCREEN_HEIGHT
    return level_data, level_width, level_height

# Список уровней (пример)
levels = [
    [
        "####________________########_#_N",
        "___P_____#",
        "###N###N##"
    ],
    [
        "#  ___N_____",
        "###___###__",
        "###########"
    ],
    [
        "N__________",
        "####_#####_",
        "#__#_______"
    ]
]

current_level_index = 0  # Начинаем с первого уровня

# Функция вычисления расстояния между двумя точками
def distance_between_points(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Загружаем текстуры
textures = load_textures()

# Инициализация первого уровня
level_data, level_width, level_height = load_level(levels[current_level_index])
player = Player(level_data,block_scale)
controls = Controls(SCREEN_WIDTH, SCREEN_HEIGHT)
hud = HUD(font_size=36, font_color=WHITE)

black_hole_center, black_hole_radius = create_black_hole(SCREEN_WIDTH, SCREEN_HEIGHT)

font = pygame.font.SysFont(None, 36)
font_40 = pygame.font.SysFont(None, 40)

# --- Загрузка кадров анимации черной дыры ---
BLACK_HOLE_FRAMES_PATH = "blackhole_frames"  # Папка с кадрами анимации (png)

blackhole_frames = []
for filename in sorted(os.listdir(BLACK_HOLE_FRAMES_PATH)):
    if filename.endswith(".png"):
        path = os.path.join(BLACK_HOLE_FRAMES_PATH, filename)
        img = pygame.image.load(path).convert_alpha()
        blackhole_frames.append(img)

if not blackhole_frames:
    print("Ошибка: не найдены кадры анимации черной дыры в папке 'blackhole_frames'")
    sys.exit()

blackhole_frame_index = 0
blackhole_animation_speed = 0.15  # скорость смены кадров в секундах
blackhole_animation_timer = 0.0

def draw_text_with_camera(screen, text, world_pos, font, color, camera):
    screen_pos = (world_pos[0] - int(camera.offset_x), world_pos[1] - int(camera.offset_y))
    rendered = font.render(text, True, color)
    screen.blit(rendered, screen_pos)

camera = Camera(level_width, level_height, SCREEN_WIDTH, SCREEN_HEIGHT)

clock = pygame.time.Clock()
running = True

mod = False  # или True для отображения HUD

while running:
    dt = clock.tick(60) / 1000.0  # Время в секундах с прошлого кадра

    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    user_control_x = controls.handle_input(player)

    # Обновляем дистанцию игрока до черной дыры
    player.distance = distance_between_points(player.rect.center, black_hole_center)

    # Притяжение черной дыры действует только на уровне 0
    if current_level_index == 0:
        delta_speed_x, delta_speed_y = move_player_towards_black_hole(
            player, black_hole_center, black_hole_radius,
            base_speed=30000,
            threshold=70,
            max_distance=500,
            epsilon=1
        )
    else:
        delta_speed_x, delta_speed_y = 0, 0

    player.x_speed += delta_speed_x
    player.y_speed += delta_speed_y

    player.update(level_data, SCREEN_HEIGHT)

    # --- Проверяем дистанцию до блока "next" для перехода на следующий уровень ---
    level_changed = False
    distance_threshold = 50  # Порог в пикселях для переключения уровня

    for obj in level_data:
        if obj["type"] == "next":
            player_center = player.rect.center
            next_center = obj["rect"].center
            dist = distance_between_points(player_center, next_center)

            # Для отладки можно раскомментировать:
            # print(f"Distance to next block: {dist}")

            if dist <= distance_threshold:
                current_level_index += 1
                if current_level_index >= len(levels):
                    print("Все уровни пройдены!")
                    running = False
                    break
                # Загружаем следующий уровень
                level_data, level_width, level_height = load_level(levels[current_level_index])
                player = Player(level_data)
                camera = Camera(level_width, level_height, SCREEN_WIDTH, SCREEN_HEIGHT)
                level_changed = True
                break

    if level_changed:
        continue  # Пропускаем отрисовку в этом кадре, чтобы обновить состояние

    # Обновляем камеру по позиции игрока с плавностью
    camera.update(player.rect, lerp_factor=0.15)

    controls.draw_buttons(screen)

    # --- Обновляем анимацию черной дыры ---
    blackhole_animation_timer += dt
    if blackhole_animation_timer >= blackhole_animation_speed:
        blackhole_animation_timer -= blackhole_animation_speed
        blackhole_frame_index = (blackhole_frame_index + 1) % len(blackhole_frames)

    # Рисуем черную дыру только на уровне 0
    if current_level_index == 0:
        black_hole_pos = (int(black_hole_center[0] - camera.offset_x), int(black_hole_center[1] - camera.offset_y))
        frame = blackhole_frames[blackhole_frame_index]
        frame_scaled = pygame.transform.smoothscale(frame, (black_hole_radius*2, black_hole_radius*2))
        rect = frame_scaled.get_rect(center=black_hole_pos)
        screen.blit(frame_scaled, rect)

    # Рисуем игрока с учётом камеры
    player_rect = camera.apply(player.rect)
    pygame.draw.rect(screen, BLUE, player_rect)

    # Рисуем объекты уровня с текстурами и камерой
    for obj in level_data:
        rect = camera.apply(obj["rect"])
        texture = textures.get(obj["type"], None)

        if texture:
            texture_scaled = pygame.transform.scale(texture, (rect.width, rect.height))
            screen.blit(texture_scaled, (rect.x, rect.y))
        else:
            pygame.draw.rect(screen, WHITE, rect)

    # Рисуем текст с учётом камеры
    draw_text_with_camera(screen, "12992918189112", (50, 50), font_40, (255, 255, 255), camera)

    if mod:
        hud.draw_player_info(screen, player, delta_speed_x, delta_speed_y, show=mod)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
