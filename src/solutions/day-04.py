"""
--- Day 4: Giant Squid ---

You're already almost 1.5km (almost a mile) below the surface of the ocean, 
already so deep that you can't see any sunlight. What you can see, however, is a
giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. 
Numbers are chosen at random, and the chosen number is marked on all boards on 
which it appears. (Numbers may not appear on all boards.) If all numbers in any 
row or any column of a board are marked, that board wins. (Diagonals don't 
count.)

The submarine has a bingo subsystem to help passengers (currently, you and the 
giant squid) pass the time. It automatically generates a random order in which 
to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no 
winners, but the boards are marked as follows (shown here adjacent to each other 
to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still 
no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

At this point, the third board wins because it has at least one complete row or 
column of marked numbers (in this case, the entire top row is 
marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum 
of all unmarked numbers on that board; in this case, the sum is 188. Then, 
multiply that sum by the number that was just called when the board won, 24, to 
get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win 
first. What will your final score be if you choose that board?
"""

# import os
from copy import deepcopy
import re
from itertools import product
from aoc2021 import aoc2021

raw_data = aoc2021.import_data(day=4)

class Board:
    size = 5
    def __init__(self, grid_values):
        self._raw_grid = grid_values
        self.values = {v: (i, j) for i, row in enumerate(self._raw_grid) 
                                for j, v in enumerate(row)}
        self.grid = {v: k for k, v in self.values.items()}
        self.marks = {k: False for k in list(product(*[range(self.size)]*2))}
        self.score = 0

    def __repr__(self):
        return f'Board({self._raw_grid})'

    def mark_board(self, n):
        bingo = False
        if n in self.values:            
            idx = self.values[n]
            self.marks[idx] = True
            bingo = self._check_bingo(idx)
        
        if bingo:
            self._score_board(n)
        return bingo
    
    def _check_bingo(self, idx):
        i = idx[0]
        bingo = all([self.marks[i,j] for j in range(self.size)])
        j = idx[1]
        bingo = bingo or all([self.marks[i,j] for i in range(self.size)])
        return bingo

    def _score_board(self, n):
        for k, v in self.marks.items():
            if not v:
                self.score += self.grid[k]
        self.score *= n
        return self.score




def process_data(raw_data):
    def str_to_list_of_int(l):
        return [int(v) for v in re.split(" |,", l) if len(v) > 0]
    numbers_drawn = str_to_list_of_int(raw_data[0])

    board_size = 5
    board_start = 2

    boards = []
    current_board = []    
    for l in raw_data[board_start:]:
        if len(l) > 0:
            current_board.append(str_to_list_of_int(l))
        else:   
            boards.append(Board(current_board))
            current_board = []

    return numbers_drawn, boards

# print(boards[0])
# print([boards[0].mark_board(n) for n in [37, 72, 60, 35, 89]])
# print([boards[0].mark_board(n) for n in [37, 32, 30, 29, 48]])
def draw_numbers(numbers_drawn, boards):
    for i, n in enumerate(number_drawn):
        for b in boards:
            bingo = b.mark_board(n)
            if bingo:
                print("Round:", i, "Last number drawn:", n)
                print("Winning board:", b)
                print("Winning score:", b.score)
                return b.score

number_drawn, boards = process_data(raw_data)
winning_score = draw_numbers(number_drawn, boards)
