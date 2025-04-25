import pygame

class Player:
    def __init__(self, level_data,player_size):
        # Безопасный поиск стартовой платформы
        start_platform = next((obj for obj in level_data if obj["type"] == "platform"), None)
        if start_platform is None:
            print("Стартовая платформа не найдена! Игрок стартует в позиции по умолчанию (100, 100)")
            self.rect = pygame.Rect(100, 100, player_size, player_size)
        else:
            platform_rect = start_platform["rect"]
            self.rect = pygame.Rect(
                platform_rect.x + 50,
                platform_rect.y - 40,
                player_size, player_size
            )
        self.y_speed = 0
        self.x_speed = 0
        self.gravity = 0.7
        self.on_ground = False
        self.jump_count = 0  # счётчик прыжков
        self.distance = 0

    def update(self, objects, screen_height):
        self.y_speed += self.gravity

        self.rect.y += self.y_speed
        self.on_ground = False
        if self.rect.y > screen_height:
            self.y_speed = -30

        for obj in objects:
            rect = obj["rect"]
            if rect.colliderect(self.rect):
                if self.y_speed > 0:
                    self.rect.bottom = rect.top
                    self.on_ground = True
                    if self.jump_count != 0:
                        print("Landed, reset jump_count")
                    self.jump_count = 0  # сброс прыжков при касании земли
                elif self.y_speed < 0:
                    self.rect.top = rect.bottom
                self.y_speed = 0

        self.rect.x += self.x_speed
        for obj in objects:
            rect = obj["rect"]
            if rect.colliderect(self.rect):
                if self.x_speed > 0:
                    self.rect.right = rect.left
                elif self.x_speed < 0:
                    self.rect.left = rect.right
                self.x_speed = 0

        self.x_speed *= 0.8  # трение

    def set_attribute(self, attr_name, value):
        setattr(self, attr_name, value)
        print(f"Attribute '{attr_name}' set to {value}")

    def jump(self):
        if self.jump_count < 2:
            self.y_speed = -15  # сила прыжка увеличена для лучшего эффекта
            self.jump_count += 1
            print(f"Jump! Count: {self.jump_count}")

    def move_right(self):
        self.x_speed -= 5  # движение влево

    def move_left(self):
        self.x_speed += 5  # движение вправо
