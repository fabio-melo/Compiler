from utils import load, gui_l
from lexical import Lexer
from sys import argv
import timeit

if __name__ == '__main__':

  if len(argv) > 1:
    if '-gui' in argv:
      argv.remove('-gui')
      gui_l(Lexer(load(argv[1])).get_tokens())
    else:
      Lexer(load(argv[1])).get_tokens('verbose')
  else:
    Lexer(load('code.for')).get_tokens('verbose')
