from game_states import GameStates
from render_functions import RenderOrder

import tcod


DEATH_COLOR = tcod.dark_red


def kill_player(player):
    player.char = '%'
    player.color = DEATH_COLOR

    return 'You died!', GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = f'{monster.name.capitalize()} is dead!'

    monster.char = '%'
    monster.color = DEATH_COLOR
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = f'remains of {monster.name}'
    monster.render_order = RenderOrder.CORPSE

    return death_message
