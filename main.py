from utils import load_program,pretty_print
from lexical import Lexer
from sys import argv
import timeit

if __name__ == '__main__':
   # t0 = time.time()
    programa = load_program('code.for') 
    l = Lexer(programa)
    l.get_tokens('verbose')

    print(timeit.timeit(l.get_tokens, number=100000))
