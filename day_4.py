"""
--- Day 4: Printing Department ---
You ride the escalator down to the printing department. They're clearly getting ready for Christmas; they have lots of large rolls of paper everywhere, and there's even a massive printer in the corner (to handle the really big print jobs).

Decorating here will be easy: they can make their own decorations. What you really need is a way to get further into the North Pole base while the elevators are offline.

"Actually, maybe we can help with that," one of the Elves replies when you ask for help. "We're pretty sure there's a cafeteria on the other side of the back wall. If we could break through the wall, you'd be able to keep moving. It's too bad all of our forklifts are so busy moving those big rolls of paper around."

If you can optimize the work the forklifts are doing, maybe they would have time to spare to break through the wall.

The rolls of paper (@) are arranged on a large grid; the Elves even have a helpful diagram (your puzzle input) indicating where everything is located.

For example:

..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
The forklifts can only access a roll of paper if there are fewer than four rolls of paper in the eight adjacent positions. If you can figure out which rolls of paper the forklifts can access, they'll spend less time looking and more time breaking down the wall to the cafeteria.

In this example, there are 13 rolls of paper that can be accessed by a forklift (marked with x):

..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.
Consider your complete diagram of the paper roll locations. How many rolls of paper can be accessed by a forklift?
"""
import numpy as np

def create_grid(grid_string, symb="@"):
    grid_line_strings = grid_string.strip().split("\n")
    grid = [ [1 if i == symb else 0 for i in line] for line in grid_line_strings]
    return np.array(grid)


def convolve2D(grid, kernel):
    if kernel.shape[0] % 2 == 0:
        raise NotImplementedError("Kernel size cannot be an even number")
    hk = kernel.shape[0] // 2

    grid_larger = np.zeros((grid.shape[0] + hk*2, grid.shape[1] + hk*2))
    grid_larger[hk:-hk, hk:-hk] = grid

    out = np.zeros_like(grid)

    for i in range(hk, grid.shape[0]+1):
        for j in range(hk, grid.shape[1]+1):
            out[i-hk, j-hk] = np.sum(grid_larger[i-hk:i+hk+1, j-hk:j+hk+1] * kernel)

    return out



def find_free_slots(grid:np.ndarray):
    #Find all the slots that have less than 4 neighbours
    kernel = np.ones((3,3))
    kernel[1,1] = 0

    conv_grid = convolve2D(grid, kernel)

    accesible_grid = np.where(conv_grid < 4, 1, 0)
    accesible_grid *= grid #This ensures that we only could areas where there are rolls

    return accesible_grid, np.sum(accesible_grid)

def main_test_1():
    test_data = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

    expected_data = """
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x."""


    grid = create_grid(test_data)

    expected_grid_out = create_grid(expected_data, "x")

    grid_out, s = find_free_slots(grid)

    expected_grid_out = expected_grid_out.astype(int)
    grid_out = grid_out.astype(int)

    grid_out_diff = (expected_grid_out - grid_out).astype(int)

    assert np.allclose(grid_out, expected_grid_out)
    assert s == 13

def main_1():
    with open("day_4.txt", "r") as f:
        data = f.read()

    grid = create_grid(data)
    grid_out, s = find_free_slots(grid)

    print(s)

"""
--- Part Two ---
Now, the Elves just need help accessing as much of the paper as they can.

Once a roll of paper can be accessed by a forklift, it can be removed. Once a roll of paper is removed, the forklifts might be able to access more rolls of paper, which they might also be able to remove. How many total rolls of paper could the Elves remove if they keep repeating this process?

Starting with the same example as above, here is one way you could remove as many rolls of paper as possible, using highlighted @ to indicate that a roll of paper is about to be removed, and using x to indicate that a roll of paper was just removed:

Initial state:
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.

Remove 13 rolls of paper:
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.

Remove 12 rolls of paper:
.......x..
.@@.x.x.@x
x@@@@...@@
x.@@@@..x.
.@.@@@@.x.
.x@@@@@@.x
.x.@.@.@@@
..@@@.@@@@
.x@@@@@@@.
....@@@...

Remove 7 rolls of paper:
..........
.x@.....x.
.@@@@...xx
..@@@@....
.x.@@@@...
..@@@@@@..
...@.@.@@x
..@@@.@@@@
..x@@@@@@.
....@@@...

Remove 5 rolls of paper:
..........
..x.......
.x@@@.....
..@@@@....
...@@@@...
..x@@@@@..
...@.@.@@.
..x@@.@@@x
...@@@@@@.
....@@@...

Remove 2 rolls of paper:
..........
..........
..x@@.....
..@@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@x.
....@@@...

Remove 1 roll of paper:
..........
..........
...@@.....
..x@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
...x@.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
....x.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
..........
...x@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...
Stop once no more rolls of paper are accessible by a forklift. In this example, a total of 43 rolls of paper can be removed.

Start with your original diagram. How many rolls of paper in total can be removed by the Elves and their forklifts?
"""


def find_and_replace_free_slots(grid):

    grid_out, s = find_free_slots(grid)
    total_removed = s
    while s > 0:
        grid = grid - grid_out
        assert np.all(np.abs(grid) == grid) #check for negatives
        grid_out, s = find_free_slots(grid)
        total_removed += s

    return grid_out, total_removed


def main_test_2():
    test_data = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

    expected_data = """
..........
..........
..........
...x@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@..."""


    grid = create_grid(test_data)

    expected_grid_out = create_grid(expected_data, "x")

    grid_out, s = find_and_replace_free_slots(grid)

    expected_grid_out = expected_grid_out.astype(int)
    grid_out = grid_out.astype(int)

    grid_out_diff = (expected_grid_out - grid_out).astype(int)

    #assert np.allclose(grid_out, expected_grid_out)
    assert s == 43



def main_2():
    with open("day_4.txt", "r") as f:
        data = f.read()

    grid = create_grid(data)
    grid_out, s = find_and_replace_free_slots(grid)

    print(s)


if __name__ == '__main__':
    #main_test_1()
    #main_1()

    main_test_2()
    main_2()
