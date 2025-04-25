import pygame
level_block= [
    "####________________#########################_#_N",
    "___P_____#",
    "###_###_##",
    "_P_",
    "_P_",
    "PPP",
    "###################NP"
]
level_block1=[
    "#########N"
]
levels = [level_block, level_block1]
current_level_index = 0

def pars1e_level_from_blocks(blocks, block_size=50):
    level_data = []
    for row_index, row in enumerate(blocks):
        for col_index, char in enumerate(row):
            if char == '_':
                continue  # пустой блок
            block_type = None
            if char == '#':
                block_type = "wall"
            elif char == 'P':
                block_type = "platform"
            elif char == 'N':
                block_type = "next"
            else:
                continue
            rect = pygame.Rect(col_index * block_size, row_index * block_size, block_size, block_size)
            level_data.append({"type": block_type, "rect": rect})
    return level_data

def load_textures():
    """
    Загружает и возвращает словарь с текстурами.
    Предполагается, что файлы wall.png, platform.png, next.png лежат в той же папке.
    """
    wall_texture = pygame.image.load("wall.png").convert_alpha()
    platform_texture = pygame.image.load("platform.png").convert_alpha()
    next_texture = pygame.image.load("next.png").convert_alpha()

    return {
        "wall": wall_texture,
        "platform": platform_texture,
        "next": next_texture
    }
