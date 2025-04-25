import pygame

class HUD:
    def __init__(self, font_size=36, font_color=(255, 255, 255)):
        self.font = pygame.font.SysFont(None, font_size)
        self.color = font_color

    def draw_text(self, screen, text, pos, camera=None):
        pos = (pos[0] - int(camera.offset_x), pos[1] - int(camera.offset_y))
        rendered = self.font.render(text, True, self.color)
        screen.blit(rendered, pos)

    def draw_player_info(self, screen, player, delta_speed_x, delta_speed_y, show=True):
        if not show:
            return
        self.draw_text(screen, f"Distance to black hole: {int(player.distance)}", (20, 20))
        self.draw_text(screen, f"Speed X: {player.x_speed:.2f}, Speed Y: {player.y_speed:.2f}", (20, 60))
        self.draw_text(screen, f"Delta speed X: {delta_speed_x:.2f}, Delta speed Y: {delta_speed_y:.2f}", (20, 100))
