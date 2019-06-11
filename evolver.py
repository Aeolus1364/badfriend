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

    def csf(self, str1, str2):
        len1 = len(str1)
        len2 = len(str2)
        counter = [[0] * (len2 + 1) for x in range(len1 + 1)]
        longest = 0
        lcs = ''
        for i in range(1, len1 - 1):
            for j in range(1, len2 - 1):
                if str1[i] == str2[j]:
                    c = counter[i][j] + 1
                    counter[i + 1][j + 1] = c
                    if c > longest:
                        longest = c
                        lcs = str1[i-c+1:i+1]
        return lcs

    def crossover(self, a, b, common):
        x = a.split(common)
        y = b.split(common)
        return x[0] + common + y[1]

    def test(self):
        individuals = []
        for i in range(1000):
            t = Individual(self.generate(random.randint(5, 15)))
            individuals.append(t)

        for j in range(1000):
            i1, i2 = random.sample(individuals, 2)
            i1, i2 = i1.stream, i2.stream

            lcs = self.csf(i1, i2)
            if len(lcs) > 2:
                print(self.crossover(i1, i2, lcs), i1, i2)
            # print(t.stream)
            # print(abs(t.num_inputs-self.desired_inputs), abs(t.num_outputs-self.desired_outputs))


class Individual:
    def __init__(self, stream):
        self.stream = stream

        self.num_inputs = stream.count('%')
        self.num_outputs = stream.count('$')





e = Evolver(2, 1)
e.test()