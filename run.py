import interpreter

code = '''
<]+3^]$A?0>]+]F3^
'''

i = interpreter.Interpreter(human_mode=True)
i.load(code)
# print(i.num_inputs, i.num_outputs)
i.run()
i.dump_output()

# i.dump_output()

