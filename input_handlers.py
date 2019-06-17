"""Handle inputs from user for roguelike game."""

from game_states import GameStates

import tcod


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)

    return {}


# Move keys:
# y u i
# h j k
# n m ,

def handle_player_turn_keys(key):
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

    elif key_char == 'p':
        return {'show_inventory': True}

    elif key_char == 'd':
        return {'drop_inventory': True}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}


def handle_targeting_keys(key):
    if key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_player_dead_keys(key):
    key_char = chr(key.c)
    if key_char == 'p':
        return {'show_inventory': True}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'full_screen': True}
    elif key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_inventory_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'full_screen': True}
    elif key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}
