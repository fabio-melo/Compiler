from lexer import Token
from copy import deepcopy
from collections import Counter

class Semantic:
  
  def __init__(self):
    self.scopes = [{},]
    self.current_scope = {}
    self.scopelist_stack = []
    self.wordlist = []
    self.scopelist = []
  
  def add_scope(self):
    print(f'ADD - {self.scopelist}  {len(self.scopelist_stack)}')

    self.scopes.append(deepcopy(self.current_scope))
    self.scopelist_stack.append(self.scopelist)
    self.scopelist = []
    #print(self.current_scope)
  
  def drop_scope(self):
    print(f'DROP - {self.scopelist}  {len(self.scopelist_stack)}')
    self.current_scope = self.scopes.pop()
    self.scopelist = self.scopelist_stack.pop()

  def add_word(self, word):
    self.wordlist.append(word)

  def add_var(self, type_):
    for x in self.wordlist:
      if x in self.scopelist:
        print(f'{x} already declared on this scope')
      else:
        self.scopelist.append(x)
        self.current_scope[x] = type_
      
    self.wordlist = []

    #print(self.current_scope)

  def add_procedure(self, word):
    if word in self.scopelist:
      print(f'{word} already declared on this scope')
    else:
      self.scopelist.append(word)
      self.current_scope[word] = 'procedure'
    
    #print(self.current_scope)

  def check_if_declared(self, var_, line):
    if var_.symbol in self.current_scope:
      #print(f'OK - {var_.symbol} Line: {line}')
      pass
    else:
      print(f"Error: Line {line}: Variable {var_.symbol} not declared in this scope")
