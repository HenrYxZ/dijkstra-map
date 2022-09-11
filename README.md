# dijkstra-map

Python implementation to create a Dijkstra map (distance map)

## Usage

Just import the flood function from the flood module. To use it the first 
parameter is an input 2D array that will have 0's in the
start positions where you want the flooding to begin, the other elements can
have any other value. Optionally, you can give another map with walls, and it
has to be of the same size and a binary 2D array where True means walls; you
can also give a limit, if you have something like a maximum distance (for
example if you want to convert to an image you can set limit to 255 and the 
elements that are further than that will be set to 255).

Example:

```python
import numpy as np
from dijkstra_map import dijkstra_map

input_map = np.array(
    [
        [1, 1, 1, 0],
        [1, 0, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 1, 1]
    ],
    dtype=int
)

walls_map = np.array(
    [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ],
    dtype=int
)

output_map = dijkstra_map(input_map, walls_map)
print(output_map)
```

That would print:

```
[[1 1 1 0]
 [1 0 1 1]
 [1 0 0 2]
 [1 1 0 3]]
```

Note that wall elements are set to 0 when limit is not given. If we use a limit,
they will take that value, for example:

```python
import numpy as np
from dijkstra_map import dijkstra_map

input_map = np.array(
    [
        [1, 1, 1, 0],
        [1, 0, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 1, 1]
    ],
    dtype=int
)

walls_map = np.array(
    [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ],
    dtype=int
)

output_map = dijkstra_map(input_map, walls_map, limit=2)
print(output_map)
```

Will give:

```
[[1 1 1 0]
 [1 0 1 1]
 [1 0 2 2]
 [1 1 2 2]]
```

## Dependencies

This project works with Python and the external library _numpy_.
To install it run:

`python -m pip install -r requirements.txt`

## Testing

To run the tests use unittest in this way:

`python -m unittest -v tests`

This will run every test in the _tests_ module, if you add new tests make sure
to import them into the _\_\_init\_\_.py_ file inside the _tests_ folder.