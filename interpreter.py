class Interpreter:
    def __init__(self, human_mode=False):
        self.command_pointer = 0
        self.cell_pointer = 0

        self.store = 0
        self.active_cell = 0
        self.data = {}
        self.stream = []

        self.commands = '>', '<', '?', '+', '-', '=', ':', '(', ')', '*', '^', '!', '$', '%', '[', ']'

        self.life_span = 0
        self.output = []
        self.input = []

        self.human_mode = human_mode

    def reset(self):
        self.command_pointer = 0
        self.cell_pointer = 0
        self.store = 0
        self.active_cell = 0
        self.data = {}
        self.life_span = 0
        self.output = []

    def load(self, code):
        self.reset()
        self.stream = []
        code = ''.join(code.split())  # removes formatting
        hex_holder = ''  # limits hex to one byte
        for n, c in enumerate(code):
            if c in self.commands:
                if hex_holder:
                    self.stream.append(int(hex_holder[:2], 16))
                    hex_holder = ''
                self.stream.append(c)

            else:
                hex_holder += c
            if len(code) - 1 == n and hex_holder:
                self.stream.append(int(hex_holder[:2], 16))

    def step(self):
        cmd = self.stream[self.command_pointer]
        arg = None
        self.call_cell()

        if cmd == '>':
            arg = self.search_arg()
            if arg is not None:
                self.cell_pointer += arg
            else:
                self.cell_pointer += 1

        elif cmd == '<':
            arg = self.search_arg()
            if arg is not None:
                self.cell_pointer -= arg
            else:
                self.cell_pointer -= 1
            if self.cell_pointer < 0:  # ignore negative cell indices
                self.cell_pointer = 0

        elif cmd == '?':
            arg = self.search_arg()
            if arg is not None:
                self.cell_pointer = arg

        elif cmd == '+':
            arg = self.search_arg()
            if arg is not None:
                self.set_cell(self.active_cell + arg)
            else:
                self.set_cell(self.active_cell + 1)

        elif cmd == '-':
            arg = self.search_arg()
            if arg is not None:
                self.set_cell(self.active_cell - arg)
            else:
                self.set_cell(self.active_cell - 1)

        elif cmd == '=':
            arg = self.search_arg()
            if arg is not None:
                self.set_cell(arg)

        elif cmd == '^':
            self.store = self.active_cell

        elif cmd == '$':
            self.queue_output(self.active_cell)

        elif cmd == '%':
            self.set_cell(self.request_input())

        elif cmd == '[':
            if self.active_cell == 0:
                pointer = self.command_pointer

                while True:
                    command = self.stream[pointer]
                    if command == ']':  # set active command to end bracket
                        self.command_pointer = pointer
                        break
                    else:
                        if pointer < len(self.stream) - 1:
                            pointer += 1
                        else:  # end at end of stream
                            break

        elif cmd == ']':
            if self.active_cell != 0:
                pointer = self.command_pointer

                while True:
                    command = self.stream[pointer]
                    if command == '[':  # set active command to start bracket
                        self.command_pointer = pointer
                        break
                    else:
                        if pointer > 0:
                            pointer -= 1
                        else:  # end at end of stream
                            break

        self.command_pointer += 1
        self.life_span += 1

    def run(self):
        self.reset()
        while self.command_pointer < len(self.stream):
            if self.life_span < 1000:
                self.step()
            else:
                # print("Lifespan exceeded, terminating")
                break

    def search_arg(self):
        next = self.next_in_stream()
        if next is not None:
            if type(next) == int:  # using int in code
                self.command_pointer += 1  # skip over argument
                return next
            elif next == '!':  # using stored int
                self.command_pointer += 1
                return self.store

    def next_in_stream(self):  # returns next command or int in stream if possible
        if self.command_pointer < len(self.stream) - 1:
            next_ = self.stream[self.command_pointer + 1]
            return next_

    def call_cell(self):  # retrieves cell data or initializes new cell to zero
        try:
            self.active_cell = self.data[self.cell_pointer]
        except KeyError:
            self.data[self.cell_pointer] = 0

    def set_cell(self, value):
        self.data[self.cell_pointer] = value

    def queue_output(self, out):
        self.output.append(out)

    def dequeue_output(self):
        if self.output:
            return self.output.pop(0)

    def dump_output(self):
        for i in self.output:
            print(i)

    def set_input(self, inp, *inps):
        if inps:
            self.input = list((inp,) + inps)
        else:
            self.input = [inp]

    def request_input(self):
        if self.human_mode:
            while True:
                inp = input('> ')
                try:
                    inp = int(inp)
                    return inp
                except ValueError:
                    print("Invalid input")
        else:
            if self.input:
                return self.input.pop(0)
            else:
                return 0