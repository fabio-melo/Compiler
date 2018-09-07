from lexer import Lexer
from syntax import Syntax
import os, webbrowser, time

now = time.time()

#Syntax(Lexer('code.for').get_tokens('output'),debug=True).export_to_file('syntax.dot')
Syntax(Lexer('code.for').get_tokens('output'),debug=False).export_to_file('syntax.dot')

done = time.time()

#print(done - now) # imrpime tempo levado para análise

# Graphviz - Converter o arquivo .dot gerado em uma imagem PNG
#os.system("dot syntax.dot -Tpng -o syntax.png")

# Abrir o arquivo no Chrome
# webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open_new("file:///D:/Google%20Drive/Computa%C3%A7%C3%A3o/Atual/_Working/Compiler/syntax.png")
