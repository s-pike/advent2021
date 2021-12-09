"""
--- Day 5: Hydrothermal Venture ---

You come across a field of hydrothermal vents on the ocean floor! These vents 
constantly produce large, opaque clouds, so it would be best to avoid them if 
possible.

They tend to form in lines; the submarine helpfully produces a list of nearby 
lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2

Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where
x1,y1 are the coordinates of one end the line segment and x2,y2 are the 
coordinates of the other end. These line segments include the points at both 
ends. In other words:

    An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

For now, only consider horizontal and vertical lines: lines where either x1 = x2 
or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the 
following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....

In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. 
Each position is shown as the number of lines which cover that point or . if no 
line covers that point. The top-left pair of 1s, for example, comes from 
2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 
and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points 
where at least two lines overlap. In the above example, this is anywhere in the 
diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two 
lines overlap?

--- Part Two ---

Unfortunately, considering only horizontal and vertical lines doesn't give you 
the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your 
list will only ever be horizontal, vertical, or a diagonal line at exactly 
45 degrees. In other words:

    An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
    An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.

Considering all lines from the above example would now produce the following 
diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....

You still need to determine the number of points where at least two lines 
overlap. In the above example, this is still anywhere in the diagram with a 2 or
larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?
"""

from aoc2021 import aoc2021
from math import copysign
from collections import defaultdict

class Coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Coord({self.x}, {self.y})'

    def values(self):
        return self.x, self.y

class Line():

    class Dim():
        def __init__(self, start, end):
            self.vector = end - start
            self.length = abs(self.vector)
            self.step = int(copysign(1, self.vector))
            self.dim_range = range(start, end + self.step, self.step)


    def __init__(self, input):
        self.start, self.end = self._parse_input(input)
        assert self.start != self.end, "start should be different to end"        
        self.x_dim = self.Dim(self.start.x, self.end.x)
        self.y_dim = self.Dim(self.start.y, self.end.y)        
        self.max_dim = max([self.x_dim.length, self.y_dim.length])
        self.orientation = self._get_orientation()
        self.coords = self._get_coords()

    def _parse_input(self, input):
        def coord_from_string(coord_string):
            return Coord(*[int(i) for i in coord_string.split(',')])

        start, end = [coord_from_string(c) for c in input.split(' -> ')]        
        return start, end

    def _get_orientation(self):
        if self.x_dim.length == 0:
            orientation = "v"
        elif self.y_dim.length == 0:
            orientation = "h"
        else:
            orientation = "d"
        
        return orientation

    def _get_coords(self):
        if self.orientation == 'v':
            return [Coord(self.start.x, y) for y in self.y_dim.dim_range]
        elif self.orientation == 'h':
            return [Coord(x, self.start.y) for x in self.x_dim.dim_range]            
        elif self.orientation == 'd':
            return [Coord(x, y) for x, y 
                        in zip(self.x_dim.dim_range, self.y_dim.dim_range)]
        else:
            ValueError(f'Invalid orientation, {self.orientation} given')
        

def test_classes():
    my_coords = [Coord(1,y) for y in range(1,3)]
    my_v_line = Line('1,1 -> 1,10')
    my_h_line = Line('1,1 -> 10,1')
    my_neg_h_line = Line('10,1 -> 1,1')
    my_d_line = Line('1,1 -> 10,10')    
    print(*my_coords)
    print(my_v_line.start)
    print(my_v_line.end.y)
    print(*my_v_line.coords)
    print(*my_h_line.coords)
    print(*my_neg_h_line.coords)
    print(*my_d_line.coords)

def load_test_data():
    test_data =  [            
        "0,9 -> 5,9",
        "8,0 -> 0,8",
        "9,4 -> 3,4",
        "2,2 -> 2,1",
        "7,0 -> 7,4",
        "6,4 -> 2,0",
        "0,9 -> 2,9",
        "3,4 -> 1,4",
        "0,0 -> 8,8",
        "5,5 -> 8,2",
    ]
    return test_data


def map_seafloor(data, orientations):
    seafloor = defaultdict(lambda: 0)
    for l in data:
        vent_line = Line(l)
        if vent_line.orientation in orientations:
            for c in vent_line.coords:            
                seafloor[c.values()] += 1            
    return seafloor

def count_danger_points(seafloor):
    return len([v for v in seafloor.values() if v > 1])

def solve_puzzle(data, orientations):        
    seafloor = map_seafloor(data, orientations)
    danger_points = count_danger_points(seafloor)
    return danger_points

def test_puzzle_1():
    data = load_test_data()
    danger_points = solve_puzzle(data, ['h', 'v'])
    assert danger_points == 5

def solution_1():
    data = aoc2021.import_data(day=5)
    danger_points = solve_puzzle(data, ['h', 'v'])
    print('Danger points', danger_points)

def test_puzzle_2():
    data = load_test_data()
    danger_points = solve_puzzle(data, ['h', 'v', 'd'])
    assert danger_points == 12

def solution_2():
    data = aoc2021.import_data(day=5)
    danger_points = solve_puzzle(data, ['h', 'v', 'd'])
    print('Danger points', danger_points)

# test_classes()
test_puzzle_1()
test_puzzle_2()
solution_1()
solution_2()


