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
            if arg:
                self.cell_pointer += arg
            else:
                self.cell_pointer += 1

        elif cmd == '<':
            arg = self.search_arg()
            if arg:
                self.cell_pointer -= arg
            else:
                self.cell_pointer -= 1
            if self.cell_pointer < 0:  # ignore negative cell indices
                self.cell_pointer = 0

        elif cmd == '?':
            arg = self.search_arg()
            if arg:
                self.cell_pointer = arg

        elif cmd == '+':
            arg = self.search_arg()
            if arg:
                self.set_cell(self.active_cell + arg)
            else:
                self.set_cell(self.active_cell + 1)

        elif cmd == '-':
            arg = self.search_arg()
            if arg:
                self.set_cell(self.active_cell - arg)
            else:
                self.set_cell(self.active_cell - 1)

        elif cmd == '=':
            arg = self.search_arg()
            if arg:
                self.set_cell(arg)

        print(self.cell_pointer, self.active_cell)

        self.command_pointer += 1

    def search_arg(self):
        next = self.next_in_stream()
        if next and type(next) == int:
            self.command_pointer += 1  # skip over argument
            return next

    def next_in_stream(self):
        if self.command_pointer < len(self.stream) - 1:
            return self.stream[self.command_pointer + 1]

    def call_cell(self):
        try:
            self.active_cell = self.data[self.cell_pointer]
        except KeyError:
            self.data[self.cell_pointer] = 0

    def set_cell(self, value):
        self.data[self.cell_pointer] = value


i = Interpreter()
i.load('>+ff>')
while i.command_pointer < len(i.stream):
    i.step()

