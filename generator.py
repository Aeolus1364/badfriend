import random
import interpreter


characters = '>', '<', '?', '+', '-', '=', '^', '!', '%', '$', '[', ']'
digits = '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'
counter = 0

i = interpreter.Interpreter()

while True:
    stream = ''
    length = 4

    for k in range(length):
        stream += random.choice(characters + digits)

    print("Test", counter)
    print(stream)
    print()
    i.load(stream)

    success_rate = 0

    for k in range(10):
        inp = random.randint(0, 10)
        i.set_input(inp)
        desired_out = inp + 5

        i.run()
        out = i.dequeue_output()

        print(out, desired_out, success_rate)

        if out == desired_out:
            success_rate += 1

    if success_rate > 5:
        print("success")
        input()

    elif stream == "%+5$":
        print("match not registered")
        input()

    counter += 1

    print()
