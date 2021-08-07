import numpy as np


def add_neighbors(closed, j, i):
    """
    Add neighbor pixels that are not in the closed map.
    Args:
        closed(ndarray): 2D binary array where true means being closed
        j(int): index of row for the pixel
        i(int): index of column for the pixel

    Returns:
        list: list of tuples with indices for the neighbor pixels not in closed
    """
    h, w = closed.shape
    rows = [j - 1, j, j + 1]
    cols = [i - 1, i, i + 1]
    neighbors = []
    for row in rows:
        for col in cols:
            if 0 <= row < h and 0 <= col < w and not closed[row][col]:
                closed[row][col] = True
                neighbors.append((row, col))
    return neighbors


def flood(input_map, walls_map=None, limit=0):
    """
    Create a Dijkstra map flood filling a given 2D map
    Args:
        input_map(ndarray): input 2D array
        walls_map(ndarray): a binary 2D array where true means a wall
        limit(int): after this limit it will stop flooding, is like max distance

    Returns:
        ndarray: 2D array with distances
    """
    h, w = input_map.shape
    # Initialize the new array with every pixel at limit distance
    new_arr = np.ones([h, w], dtype=int) * limit
    if walls_map is not None:
        closed = np.copy(walls_map)
    else:
        closed = np.zeros([h, w], dtype=bool)
    starting_pixels = []
    open_pixels = []
    total_pixels = h * w
    if not limit:
        limit = total_pixels
    # First pass: Add starting pixels and put them in closed
    for counter in range(h * w):
        i = counter % w
        j = counter // w
        if input_map[j][i] == 0:
            new_arr[j][i] = 0
            closed[j][i] = True
            starting_pixels.append((j, i))

    # Second pass: Add border to open
    for j, i in starting_pixels:
        open_pixels += add_neighbors(closed, j, i)
    # Third pass: Iterate filling in the open list
    counter = 1
    while counter < limit and open_pixels:
        next_open = []
        for j, i in open_pixels:
            new_arr[j][i] = counter
            next_open += add_neighbors(closed, j, i)
        open_pixels = next_open
        counter += 1
    # Last pass: flood last pixels
    for j, i in open_pixels:
        new_arr[j][i] = counter
    return new_arr
