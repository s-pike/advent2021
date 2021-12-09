"""
Import data for advent of code
"""

import os

def import_data(day, puzzle=1, input_dir = 'data'):
    input_path = os.path.join(input_dir, f'day-{day:02d}_input-{puzzle}.txt')
    with open(input_path, 'r') as f:
        data = [l.strip() for l in f.readlines()]

    return data