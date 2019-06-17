from interpreter import Interpreter
import random


class Evolver:
    def __init__(self, inps, outs, gen_size=1000, max_life_span=1000, limit=(5, 15), trials=10):
        self.desired_inputs = inps
        self.desired_outputs = outs

        self.commands = '>', '<', '?', '+', '-', '=', '^', '!', '%', '$', '[', ']'
        self.digits = '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'

        self.freq_command = 0.75  # frequency of command being chosen as random character

        self.gen_size = gen_size
        self.generations = []
        self.individuals = []
        self.current_gen = 0

        self.trials_per_individual = trials
        self.init_gen_limit = limit
        self.max_fitness = 100
        self.interpreter = Interpreter(max_life_span)

    def generate(self, length):  # generates a random stream of given length and frequency
        stream = ''
        for i in range(length):
            freq = random.uniform(0, 1)
            if freq < self.freq_command:
                stream += random.choice(self.commands)
            else:
                stream += random.choice(self.digits)
        return stream

    def csf(self, str1, str2):  # common substring finder
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

    def run_generation(self):
        num_des_io = 0
        total_fitness = 0

        if self.current_gen == 0:  # randomly generates first generation
            generation = []
            for i in range(self.gen_size):
                x = Individual(self.generate(random.randint(self.init_gen_limit[0], self.init_gen_limit[1])), self.desired_inputs, self.desired_outputs)
                generation.append(x)
            self.generations.append(generation)

        self.individuals = self.generations[self.current_gen]


        for i in self.individuals:  # testing individuals to determine fitness
            total_error = 0
            if i.num_inputs == self.desired_inputs and i.num_outputs == self.desired_outputs:
                for j in range(self.trials_per_individual):
                    inp = [random.randint(0, 100) for x in range(2)]
                    exp_out = inp[0] + inp[1]
                    self.interpreter.set_input(inp)
                    self.interpreter.load(i.stream)
                    self.interpreter.run()
                    calc_out = self.interpreter.dequeue_output()
                    try:
                        error = abs(calc_out - exp_out)
                    except TypeError:
                        print(i.stream, calc_out)
                        self.interpreter.dump_output()
                        input()
                        break


                    total_error += error
                avg_error = total_error / self.trials_per_individual
                fitness = self.max_fitness / (avg_error + 1)

                print(f'Error: {avg_error} F: {fitness}   Stream: {i.stream}')

                num_des_io += 1

            total_fitness += i.fitness

        # math for displayed stats
        per_des_io = num_des_io / self.gen_size * 100
        avg_fitness = total_fitness / self.gen_size
        print(f"Generation {self.current_gen} {str(round(per_des_io, 2))}%   Avg. Fitness: {round(avg_fitness, 2)}")

        self.current_gen += 1
        self.generations.append([])

        for j in range(self.gen_size):
            while True:  # selects 2 different individuals to reproduce
                pair = random.choices(self.individuals, weights=[x.fitness for x in self.individuals], k=2)
                a, b = pair[0].stream, pair[1].stream
                if a != b:
                    break

            lcs = self.csf(a, b)

            if len(lcs) >= 2:  # crossover occurs if lcs at least 2
                offspring_stream = self.crossover(a, b, lcs)
                offspring = Individual(offspring_stream, self.desired_inputs, self.desired_outputs)
            else:
                offspring = random.choices(pair, weights=[x.fitness for x in pair])[0]

            self.generations[self.current_gen].append(offspring)  # filling next generation


class Individual:
    def __init__(self, stream, desired_ins, desired_outs):
        self.stream = stream

        self.num_inputs = stream.count('%')
        self.num_outputs = stream.count('$')

        io_diff = abs(desired_ins - self.num_inputs) + abs(desired_outs - self.num_outputs)
        self.fitness = 1 / (io_diff + 1)


e = Evolver(2, 1, gen_size=500)
for i in range(10):
    e.run_generation()
