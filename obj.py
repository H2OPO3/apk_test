# game_objects.py
def create_black_hole(screen_width, screen_height):
    center = (int(screen_width * 0.1), int(screen_height * 0.1))
    radius = 20
    return center, radius