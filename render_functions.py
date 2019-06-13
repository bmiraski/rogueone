"""Render entities on the page."""

import tcod
import tcod.map


def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width,
               screen_height, colors):
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = fov_map.fov[y, x]
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        tcod.console_set_char_background(con, x, y,
                                                         colors.get('light_wall'))
                    else:
                        tcod.console_set_char_background(con, x, y,
                                                         colors.get('light_ground'))

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        tcod.console_set_char_background(con, x, y,
                                                         colors.get('dark_wall'))
                    else:
                        tcod.console_set_char_background(con, x, y,
                                                         colors.get('dark_ground'))

    # Draw all entities in the list
    for entity in entities:
        draw_entity(con, entity, fov_map)

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map):
    if fov_map.fov[entity.y, entity.x]:
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(con, entity.x, entity.y, entity.char,
                              tcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
