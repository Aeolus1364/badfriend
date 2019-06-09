import interpreter

code = '''

%+5$%$%$

'''

i = interpreter.Interpreter(True)
i.load(code)
i.set_input(1)
i.run()
print(i.dequeue_output())
print(i.dequeue_output())
print(i.dequeue_output())

# i.dump_output()

