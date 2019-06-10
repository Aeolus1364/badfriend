import interpreter

code = '''
%^>%+!$
'''

i = interpreter.Interpreter(True)
i.load(code)
print(i.num_inputs, i.num_outputs)
i.set_input(1)
i.run()
i.dump_output()

# i.dump_output()

