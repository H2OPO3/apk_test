import pygame

class Controls:
    def __init__(self, screen_width, screen_height):
        self.BUTTON_SIZE_X = int(screen_width * 0.1)
        self.BUTTON_SIZE_Y = int(screen_height * 0.05)

        self.jump_button = pygame.Rect(int(screen_width * 0.45), int(screen_height * 0.4), self.BUTTON_SIZE_X, self.BUTTON_SIZE_Y)
        self.move_left_button = pygame.Rect(int(screen_width * 0.6), int(screen_height * 0.45), self.BUTTON_SIZE_X, self.BUTTON_SIZE_Y)
        self.move_right_button = pygame.Rect(int(screen_width * 0.3), int(screen_height * 0.45), self.BUTTON_SIZE_X, self.BUTTON_SIZE_Y)

    def handle_input(self, player):
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        user_control_x = 0
        if keys[pygame.K_w] or (self.jump_button.collidepoint(mouse_pos) and mouse_pressed):
            player.jump()
        if keys[pygame.K_a] or (self.move_left_button.collidepoint(mouse_pos) and mouse_pressed):
            player.move_left()
            user_control_x = -1
        if keys[pygame.K_d] or (self.move_right_button.collidepoint(mouse_pos) and mouse_pressed):
            player.move_right()
            user_control_x = 1

        return user_control_x

    def draw_buttons(self, screen):
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)

        pygame.draw.rect(screen, GREEN, self.jump_button)
        pygame.draw.rect(screen, BLUE, self.move_left_button)
        pygame.draw.rect(screen, BLUE, self.move_right_button)
