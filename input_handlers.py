"""Handle inputs from user for roguelike game."""

import tcod


# Move keys:
# y u i
# h j k
# n m ,

def handle_keys(key):
    key_char = chr(key.c)
    # Movement keys
    if key.vk == tcod.KEY_UP or key_char == 'u':
        return {'move': (0, -1)}
    elif key.vk == tcod.KEY_DOWN or key_char == 'm':
        return {'move': (0, 1)}
    elif key.vk == tcod.KEY_LEFT or key_char == 'h':
        return {'move': (-1, 0)}
    elif key.vk == tcod.KEY_RIGHT or key_char == 'k':
        return {'move': (1, 0)}
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'i':
        return {'move': (1, -1)}
    elif key_char == 'n':
        return {'move': (-1, 1)}
    elif key_char == ',':
        return {'move': (1, 1)}

    if key_char == 'g':
        return {'pickup': True}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}
