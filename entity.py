import math
from render_functions import RenderOrder
import tcod.map
import tcod.path


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    def __init__(self, x, y, char, color, name, blocks=False,
                 render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 item=None, inventory=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

    def move(self, dx, dy):
        """Move the entity by the given amount."""
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def move_astar(self, target, entities, game_map):
        # This will create a new map for entity movement, but could be removed
        # once the game_map itself is refactored to use the Map class. :facepalm:
        move_map = tcod.map.Map(game_map.width, game_map.height)

        # Close out the non-walkable walls.
        for y in range(game_map.height):
            for x in range(game_map.width):
                move_map.transparent[y, x] = not game_map.tiles[x][y].block_sight
                move_map.walkable[y, x] = not game_map.tiles[x][y].blocked

        # Block out the squares occupied by blocking objects. This part will still
        # need to happen in the refactor.
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                move_map.walkable[entity.y, entity.x] = False

        # Use the new path functions to generate the path
        my_path = tcod.path.AStar(move_map.walkable, 1.41)
        my_path_route = my_path.get_path(self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths
        # (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from
        # running around the map if there's an alternative path really far away

        if len(my_path_route) != 0 and len(my_path_route) < 25:
            x, y = my_path_route[0]
            if x or y:
                self.x = x
                self.y = y

        else:
            # Keep the old move function as a backup so that if there are no paths
            # (for example another monster blocks a corridor)
            # it will still try to move towards the player
            # (closer to the corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
