import interpreter

code = '''
%^>%+!$
'''

i = interpreter.Interpreter(True)
i.load(code)
i.set_input(1)
i.run()
i.dump_output()

# i.dump_output()

