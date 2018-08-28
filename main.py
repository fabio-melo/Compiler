from utils import load, gui_l
from lexer import Lexer
from sys import argv
from syntax import Syntax
import os
import webbrowser

Syntax(Lexer(load('code.for')).get_tokens(''),debug="all").export_to_file('syntax.dot')

os.system("dot syntax.dot -Tpng -o syntax.png")

# Gambiarra Fedorenta.
#os.system('%SystemRoot%\\System32\\rundll32.exe "%ProgramFiles%\\Windows Photo Viewer\\PhotoViewer.dll", ImageView_Fullscreen D:\\Google Drive\\Computação\\Atual\\_Working\\Compiler\\syntax.png')
webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open_new("file:///D:/Google%20Drive/Computa%C3%A7%C3%A3o/Atual/_Working/Compiler/syntax.png")
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