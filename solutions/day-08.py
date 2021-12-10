"""
--- Day 8: Seven Segment Search ---

You barely reach the safety of the cave when the whale smashes into the cave 
mouth, collapsing it. Sensors indicate another exit to this cave at a much 
greater depth, so you have no choice but to press on.

As your submarine slowly makes its way through the cave system, you notice that 
the four-digit seven-segment displays in your submarine are malfunctioning; they 
must have been damaged during the escape. You'll be in a lot of trouble without 
them, so you'd better figure out what's wrong.

Each digit of a seven-segment display is rendered by turning on or off any of 
seven segments named a through g:

  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

So, to render a 1, only segments c and f would be turned on; the rest would be 
off. To render a 7, only segments a, c, and f would be turned on.

The problem is that the signals which control the segments have been mixed up on 
each display. The submarine is still trying to display numbers by producing 
output on signal wires a through g, but those wires are connected to segments 
randomly. Worse, the wire/segment connections are mixed up separately for each 
four-digit display! (All of the digits within a display use the same 
connections, though.)

So, you might know that only signal wires b and g are turned on, but that 
doesn't mean segments b and g are turned on: the only digit that uses two 
segments is 1, so it must mean segments c and f are meant to be on. With just 
that information, you still can't tell which wire (b/g) goes to which segment 
(c/f). For that, you'll need to collect more information.

For each display, you watch the changing signals for a while, make a note of all 
ten unique signal patterns you see, and then write down a single four digit 
output value (your puzzle input). Using the signal patterns, you should be able 
to work out which pattern corresponds to which digit.

For example, here is what you might see in a single entry in your notes:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf

(The entry is wrapped here to two lines so it fits; in your notes, it will all 
be on a single line.)

Each entry consists of ten unique signal patterns, a | delimiter, and finally 
the four digit output value. Within an entry, the same wire/segment connections 
are used (but you don't know what the connections actually are). The unique 
signal patterns correspond to the ten different ways the submarine tries to 
render a digit using the current wire/segment connections. Because 7 is the 
only digit that uses three segments, dab in the above example means that to 
render a 7, signal lines d, a, and b are on. Because 4 is the only digit 
that uses four segments, eafb means that to render a 4, signal lines e, a, f, 
and b are on.

Using this information, you should be able to work out which combination of 
signal wires corresponds to each of the ten digits. Then, you can decode the 
four digit output value. Unfortunately, in the above example, all of the digits 
in the output value (cdfeb fcadb cdfeb cdbaf) use five segments and are more 
difficult to deduce.

For now, focus on the easy digits. Consider this larger example:

be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
fgae cfgab fg bagce

Because the digits 1, 4, 7, and 8 each use a unique number of segments, you 
should be able to tell which combinations of signals correspond to those digits. 
Counting only digits in the output values (the part after | on each line), in 
the above example, there are 26 instances of digits that use a unique number of 
segments (highlighted above).

In the output values, how many times do digits 1, 4, 7, or 8 appear?
"""

from aoc2021 import import_data
from collections import Counter, defaultdict

class SevenSegmentDigits():
    default_digit_segments = (
        'abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg' 
    )    

    def __init__(self, raw_digit_segments = default_digit_segments):
        self.digit_segments = dict(
            zip(list(range(10)), raw_digit_segments.split())
            )
        self.segment_digits = {
            s: [k for k, v in self.digit_segments.items() if s in v] 
            for s in 'abcdefg'
            }
        self.n_segments = {k: len(v) for k,v in self.digit_segments.items()}
        self.digits_by_n_segments = {}
        for k, v in self.n_segments.items():
            self.digits_by_n_segments[v] = (
                self.digits_by_n_segments.get(v, []) + [k]
            )


class FourDigitDisplay():
    def __init__(self, data_stream):
        self.data_stream = data_stream.split('|')
        self.signals_patterns = self.data_stream[0].strip()
        self.output_signals = self.data_stream[1].strip().split(' ')
        self.output_lengths = Counter([len(l) for l in self.output_signals])
        self.ssd = SevenSegmentDigits(self.signals_patterns)
        self.default_ssd = SevenSegmentDigits()
        # map first, easy digits
        self.digit_to_number_map = {
            v[0] : self.ssd.digits_by_n_segments[k][0]
            for k, v in self.default_ssd.digits_by_n_segments.items() 
            if len(v) == 1
            } 

        # to map next characters:
        # 3 is length 5, and all segments of 1 are in 3
        # 9 is length 6, and all segments of 3 are in 9
        # 0 is length 6, and all segements of 1 are in 6 and it's not 9
        # 6 is length 6, and is not 9 or 0
        # 5 is length 5, and all segments of 5 are in 9
        # 2 is length 5, and is not 3 or 5

class SubmarineDisplays():
    def __init__(self, raw):
        self.raw = raw        
        self.displays = [FourDigitDisplay(l) for l in raw]
        self.get_output_lengths()

    def get_output_lengths(self):
        output_counter = Counter()
        for d in self.displays:
            output_counter.update(d.output_lengths)
        self.output_lengths = output_counter


def solve_puzzle_1(data):
    test_sub_displays = SubmarineDisplays(data)    
    print("Output lengths:", test_sub_displays.output_lengths)    
    default_ssd = SevenSegmentDigits()    
    dbs = default_ssd.digits_by_n_segments
    print('dbs', dbs)
    print("Number of each digit")
    digit_occurances = {tuple(dbs[k]): v for k, v in test_sub_displays.output_lengths.items()}
    print("1, 4, 7, 8, total", sum([v for k, v in digit_occurances.items()
                                     if k[0] in [1, 4, 7, 8]]))
    print("Default segment digits")
    print(default_ssd.segment_digits)
    print("First item segment digit mapping")
    print(test_sub_displays.displays[0].digit_to_number_map)
    

def test_displays():
    raw_test = ("""
        be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
        edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
        fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
        fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
        aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
        fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
        dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
        bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
        egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
        gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
        """).split('\n')[1:-1]
    solve_puzzle_1(raw_test)

def solution_1():
    data = import_data(8)
    solve_puzzle_1(data)


if __name__ == '__main__':
    test_displays()
    # solution_1()
