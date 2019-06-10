from interpreter import Interpreter
import random


class Evolver:
    def __init__(self, inps, outs):
        self.desired_inputs = inps
        self.desired_outputs = outs

        self.commands = '>', '<', '?', '+', '-', '=', '^', '!', '%', '$', '[', ']'
        self.digits = '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'

        self.freq_command = 0.75  # frequency of command being chosen as random character

    def generate(self, length):  # generates a random stream of given length and frequency
        stream = ''
        for i in range(length):
            freq = random.uniform(0, 1)
            if freq < self.freq_command:
                stream += random.choice(self.commands)
            else:
                stream += random.choice(self.digits)
        return stream

    def test(self):
        for i in range(1000):
            t = Individual(self.generate(random.randint(5, 15)))
            print(t.stream)
            print(abs(t.num_inputs-self.desired_inputs), abs(t.num_outputs-self.desired_outputs))


class Individual:
    def __init__(self, stream):
        self.stream = stream

        self.num_inputs = stream.count('%')
        self.num_outputs = stream.count('$')





e = Evolver(2, 1)
e.test()