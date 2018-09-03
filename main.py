from utils import load, gui_l
from lexer import Lexer
from sys import argv
from syntax import Syntax
import os
import webbrowser
import time
now = time.time()

Syntax(Lexer(load('code.for')).get_tokens('output'),debug=True).export_to_file('syntax.dot')
#Lexer(load('code.for')).get_tokens('output')
done = time.time()
print(done - now)

os.system("dot syntax.dot -Tpng -o syntax.png")

# Gambiarra Fedorenta.
#os.system('%SystemRoot%\\System32\\rundll32.exe "%ProgramFiles%\\Windows Photo Viewer\\PhotoViewer.dll", ImageView_Fullscreen D:\\Google Drive\\Computação\\Atual\\_Working\\Compiler\\syntax.png')
webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open_new("file:///D:/Google%20Drive/Computa%C3%A7%C3%A3o/Atual/_Working/Compiler/syntax.png")
