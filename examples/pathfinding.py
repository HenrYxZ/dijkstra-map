""" Example of pathfinding for multiple entities to a target with Dijkstra Map.

This example shows how a Dijkstra Map can be used for path-finding, there is a
player represented by a blue circle and enemies represented by circles of other
colors that move towards the player every 2 seconds (update call).
On each update, a new Dijkstra Map is calculated with the player as the target.
The Enemy class has a chase method that moves the enemy grid position to the
surrounding position with lowest value in the map, if there is no obstacle.

Usage:

This example uses pyglet, to install it run:

    $ pip install pyglet

Then run this script.

The controls to move the player are the arrow keys.
"""


import numpy as np
import pyglet
from pyglet.window import key


from dijkstra_map import dijkstra_map


# Windows
WIDTH = 480

window = pyglet.window.Window(WIDTH, WIDTH, caption="Pathfinding")
batch = pyglet.graphics.Batch()

# Game
N = 10
WALL_CODE = 1
ENEMY_CODE = 2
ENEMY_COLORS = [
    (20, 120, 20),  # Green
    (100, 20, 100),     # Purple
    (20, 100, 100),     # cyan
    (180, 20, 20)   # red
]
PLAYER_COLOR = (20, 20, 150)
DIRECTIONS = [
    np.array([y, x]) for x in [-1, 0, 1] for y in [-1, 0, 1]
]
ENTITY_RADIUS = (WIDTH / N) * 0.4
UPDATE_TIME = 2
TILE_SIZE = WIDTH / N

walls = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
])


level_map = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 2, 1],
    [1, 1, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
])


wall_sprites = []
enemies = []
player_x = WIDTH / 2 - TILE_SIZE / 2
player_y = WIDTH / 2 + TILE_SIZE / 2
player = pyglet.shapes.Circle(
    player_x, player_y, ENTITY_RADIUS, color=PLAYER_COLOR, batch=batch
)
player_pos = np.array([N // 2 - 1, N // 2 - 1], dtype=int)


class Enemy(pyglet.shapes.Circle):
    """ Enemy in the game.

    This class represent an enemy inside the game, that has a position inside a
    grid, is visually represented by a circle and can chase the player.

    Attributes:
        grid_position (tuple): Position inside the game grid as a tuple of two
            integers.
    """
    def __init__(self, x, y, i, j, color_idx):
        super().__init__(
            x, y, ENTITY_RADIUS, color=ENEMY_COLORS[color_idx], batch=batch
        )
        self._grid_position = (j, i)

    @property
    def grid_position(self):
        return self._grid_position

    @grid_position.setter
    def grid_position(self, value):
        self._grid_position = value
        self.x = value[1] * TILE_SIZE + TILE_SIZE * 0.5
        self.y = WIDTH - TILE_SIZE - value[0] * TILE_SIZE + TILE_SIZE * 0.5

    def chase_player(self, d_map, obstacles):
        """
        Move to the nearby position closest to the player.

        Args:
            d_map (ndarray): The current dijkstra map
            obstacles (ndarray): 2D map where 1 means obstacle
        """
        # choose the direction with lower value
        lowest_value = N
        # If current value is good enough, don't move
        if d_map[self.grid_position] == 1:
            return
        lowest_pos = self.grid_position
        h, w = d_map.shape
        center = np.zeros(2)
        for direction in DIRECTIONS:
            if np.array_equal(direction, center):
                continue
            new_i = direction[1] + self.grid_position[1]
            new_j = direction[0] + self.grid_position[0]
            # Don't go outside the map
            if new_i < 0 or new_i >= w or new_j < 0 or new_j >= h:
                continue
            # Don't go over obstacles
            if obstacles[new_j, new_i]:
                continue

            new_value = d_map[new_j, new_i]
            if new_value < lowest_value:
                lowest_value = new_value
                lowest_pos = (new_j, new_i)
        if lowest_pos != self.grid_position:
            self.grid_position = lowest_pos


def update(_):
    input_map = np.ones([N, N], dtype=int)
    input_map[player_pos[0], player_pos[1]] = 0
    d_map = dijkstra_map(input_map, walls)

    obstacles = walls > 0
    obstacles[player_pos[0], player_pos[1]] = 1
    for enemy in enemies:
        obstacles[enemy.grid_position] = 1

    for enemy in enemies:
        obstacles[enemy.grid_position] = 0
        enemy.chase_player(d_map, obstacles)
        obstacles[enemy.grid_position] = 1


def init():
    # Create entities from the level map
    n = len(level_map)
    tile_size = WIDTH / n
    for j in range(n):
        for i in range(n):
            # Create walls
            if level_map[j, i] == WALL_CODE:
                x = i * tile_size
                y = WIDTH - tile_size - j * tile_size
                new_rect = pyglet.shapes.Rectangle(
                    x, y, tile_size - 1, tile_size - 1,
                    batch=batch
                )
                wall_sprites.append(new_rect)
            # Create enemies
            elif level_map[j, i] == ENEMY_CODE:
                x = i * tile_size + tile_size / 2
                y = WIDTH - tile_size - j * tile_size + tile_size / 2
                enemy_color_idx = len(enemies) % len(ENEMY_COLORS)
                new_enemy = Enemy(x, y, i, j, enemy_color_idx)
                enemies.append(new_enemy)


@window.event
def on_draw():
    window.clear()
    batch.draw()


def on_key_press(symbol, _):
    j, i = player_pos
    if symbol == key.LEFT:
        if player_pos[1] > 0 and not walls[j, i - 1]:
            player_pos[1] -= 1
            player.x -= TILE_SIZE
    elif symbol == key.RIGHT:
        if player_pos[1] < N - 1 and not walls[j, i + 1]:
            player_pos[1] += 1
            player.x += TILE_SIZE
    elif symbol == key.UP:
        if player_pos[0] > 0 and not walls[j - 1, i]:
            player_pos[0] -= 1
            player.y += TILE_SIZE
    elif symbol == key.DOWN:
        if player_pos[0] < N - 1 and not walls[j + 1, i]:
            player_pos[0] += 1
            player.y -= TILE_SIZE


def main():
    init()
    window.push_handlers(on_key_press=on_key_press)
    pyglet.clock.schedule_interval(update, UPDATE_TIME)
    pyglet.app.run()


if __name__ == '__main__':
    main()
