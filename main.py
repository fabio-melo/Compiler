from utils import load, gui_l
from lexer import Lexer
from sys import argv
from syntax import Syntax
import timeit


Syntax(Lexer(load('code.for'),debug=True).get_tokens('output')).start()

'''
if __name__ == '__main__':

  if len(argv) > 1:
    if '-gui' in argv:
      argv.remove('-gui')
      gui_l(Lexer(load(argv[1])).get_tokens())
    else:
      Lexer(load(argv[1]),verbose=True).get_tokens()
  else:
    Lexer(load('code.for'),verbose=True).get_tokens()
'''