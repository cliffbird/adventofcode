from collections import Counter
from copy import copy
from main import BaseProcessor

class D8Processor(BaseProcessor):

    def setup(self):
        patterns = []
        part1 = 0
        part2 = 0
        with open(self.path, "r") as f:
            for line in f:
                p = Pattern(line)
                part1 += p.part1
                part2 += p.part2

        print(f"part1: {part1}")
        print(f"part2: {part2}")


    def run1(self):
        self.setup()

    def run2(self):
        pass


class Pattern:
    def __init__(self, line):
        signals_section, output_section = line.strip().split(" | ")
        self.signals = signals_section.split()
        self.output = output_section.split()
        self.part1 = 0
        self.segment_map = {}

        self.process_signals()
        self.process_output()



    def process_signals(self):

        signals = []
        for i in range(10):
            signals.append(None)

        zero_six_nine = []
        two_three_five = []

        # get 1 and 7
        for signal in self.signals:
            if len(signal) == 2:
                signals[1] = signal
            elif len(signal) == 3:
                signals[7] = signal
            elif len(signal) == 4:
                signals[4] = signal
            elif len(signal) == 5:
                two_three_five.append(signal)
            elif len(signal) == 6:
                zero_six_nine.append(signal)
            elif len(signal) == 7:
                signals[8] = signal

        self.signals.remove(signals[1])
        self.signals.remove(signals[4])
        self.signals.remove(signals[7])

        # the uncommon piece in 7 is the top
        # the common pieces are the right
        top = None
        right2 = ""
        for char in signals[7]:
            if char in signals[1]:
                right2 += char
            else:
                top = char

        # left-top and middle are the unique ones in 4
        lefttop_middle = ""
        for char in signals[4]:
            if char not in right2:
                lefttop_middle += char


        # 4 is entirely in 9
        for s1 in zero_six_nine:
            found = True
            for char in signals[4]:
                if char not in s1:
                    found = False
                    break
            if found:
                signals[9] = s1
                break
        zero_six_nine.remove(signals[9])
        zero_six = zero_six_nine

        bottom = copy(signals[9])
        bottom = bottom.replace(top, '')
        for char in signals[4]:
            bottom = bottom.replace(char, '')

        # get left bottom
        leftbottom = copy(zero_six[0])
        for char in signals[9]:
            leftbottom = leftbottom.replace(char, '')

        # get middle and left
        for signal in zero_six:
            for char in lefttop_middle:
                if char not in signal:
                    middle = char
                    signals[6] = signal
                    break
        zero_six.remove(signals[6])
        signals[0] = zero_six[0]
        lefttop = lefttop_middle.replace(middle, '')

        for signal in two_three_five:
            if lefttop in signal:
                signals[5] = signal
                break
        two_three_five.remove(signals[5])
        two_three = two_three_five

        if right2[0] in signals[6]:
            rightbottom = right2[0]
            righttop = right2[1]
        else:
            rightbottom = right2[1]
            righttop = right2[0]

        self.segment_map['a'] = top
        self.segment_map['b'] = lefttop
        self.segment_map['c'] = righttop
        self.segment_map['d'] = middle
        self.segment_map['e'] = leftbottom
        self.segment_map['f'] = rightbottom
        self.segment_map['g'] = bottom


    def process_output(self):

        output = ""
        # get 1 and 7
        for digit in self.output:
            if len(digit) == 2:
                output += "1"
                self.part1 += 1
            elif len(digit) == 3:
                output += "7"
                self.part1 += 1
            elif len(digit) == 4:
                output += "4"
                self.part1 += 1
            elif len(digit) == 5 or len(digit) == 6:
                output += self.get_digit_value(digit)
            elif len(digit) == 7:
                output += "8"
                self.part1 += 1

        assert len(output) == 4
        self.part2 = int(output)

    def get_digit_value(self, digit):
        if len(digit) == 5:
            if self.segment_map['b'] in digit:
                return "5"
            elif self.segment_map['e'] in digit:
                return "2"
            else:
                return "3"

        elif len(digit) == 6:
            if self.segment_map['d'] not in digit:
                return "0"
            elif self.segment_map['e'] in digit:
                return "6"
            else:
                return "9"
