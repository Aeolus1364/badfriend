class Interpreter:
    def __init__(self):
        self.command_pointer = 0
        self.cell_pointer = 0

        self.store = 0
        self.active_cell = 0
        self.data = {}
        self.stream = []

        self.commands = '>', '<', '?', '+', '-', '=', ':', '(', ')', '*', '^', '!', '$', '%', '[', ']'

    def load(self, code):
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
        print(self.stream)

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
            print(self.active_cell)

        elif cmd == '%':
            while True:
                inp = input('> ')
                try:
                    inp = int(inp)
                    self.set_cell(inp)
                    break
                except ValueError:
                    print("Invalid input")

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

        # print(self.command_pointer, cmd, self.cell_pointer, self.store, self.data)

        self.command_pointer += 1

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


i = Interpreter()
i.load('=%>=%-[<2^>2+!<-]>$')
while i.command_pointer < len(i.stream):
    i.step()
# print(i.cell_pointer, i.store, i.data)

