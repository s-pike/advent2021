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

--- Part Two ---

On the other hand, it might be wise to try a different strategy: let the giant 
squid win.

You aren't sure how many bingo boards a giant squid could play at once, so 
rather than waste time counting its arms, the safe thing to do is to figure out 
which board will win last and choose that one. That way, no matter which boards 
it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 
13 is eventually called and its middle column is completely marked. If you were 
to keep playing until this point, the second board would have a sum of unmarked 
numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score 
be?


"""

from copy import deepcopy
import re
from itertools import product
import aoc2021

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
        self.bingo = False

    def __repr__(self):
        return f'Board({self._raw_grid})'

    def mark_board(self, n):        
        if n in self.values:            
            idx = self.values[n]
            self.marks[idx] = True
            self.bingo = self._check_bingo(idx)
        
        if self.bingo:
            self._score_board(n)
        return self.bingo
    
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

def print_board_info(numbers_drawn, n, board):
    print("Round:", numbers_drawn, "Last number drawn:", n)
    print("Board:", board)
    print("Score:", board.score)

def find_winner(numbers_drawn, boards):
    for i, n in enumerate(numbers_drawn):
        for b in boards:
            bingo = b.mark_board(n)
            if bingo:
                print("-----Winner-----")
                print_board_info(i, n, b)
                return b.score

def find_loser(numbers_drawn, boards):
    draw_stack = deepcopy(numbers_drawn)
    draw_stack.reverse()
    while len(boards) > 1:
        n = draw_stack.pop()
        boards = [b for b in boards if not b.mark_board(n)]
    
    last_board = boards[0]
    while not last_board.bingo:
        n = draw_stack.pop()
        bingo = last_board.mark_board(n)
        if bingo:
            print("-----Loser-----")
            print_board_info(len(draw_stack), n, last_board)
            return last_board.score

numbers_drawn, boards = process_data(raw_data)
winning_score = find_winner(numbers_drawn, boards)
losing_score = find_loser(numbers_drawn, boards)