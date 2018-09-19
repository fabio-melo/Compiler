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
    self.program_name = ''
    self._current_line = None # não tá DRY, mas ok
    self._debug = False
    self.v1, self.v2, self.v3 = None,None,None
    self.eval_stack = []
    self.eval_flag = ''
    self.procedure_stack = [[],]
    self.procedure_scope_stack = []


  def add_scope(self):
    if self._debug: 
      print(f'SCOPE ADD - {self.current_scope}  {len(self.scopelist_stack)}')
      print(f'SCOPE PROCEDURE ADD - {self.procedure_stack}  {len(self.procedure_scope_stack)}')
    self.scopes.append(deepcopy(self.current_scope))
    self.scopelist_stack.append(self.scopelist)
    self.scopelist = []
    self.procedure_scope_stack.append(deepcopy(self.procedure_stack))
    #print(self.current_scope)
  def drop_scope(self):
    if self._debug: 
      print(f'SCOPE DROP - {self.current_scope}  {len(self.scopelist_stack)}')
      print(f'SCOPE PROCEDURE DROP - {self.procedure_stack}  {len(self.procedure_scope_stack)}')

    self.current_scope = self.scopes.pop()
    self.scopelist = self.scopelist_stack.pop()
    self.procedure_stack = self.procedure_stack.pop()

  def add_word(self, word):
    if word == self.program_name:
      print(f'ERROR: Line {self._current_line}: program name CANNOT be assigned to a variable')
    self.wordlist.append(word)

  def add_var(self, type_):
    for x in self.wordlist:
      if x in self.scopelist:
        print(f'ERROR: Line {self._current_line}: variable "{x}" already declared on this scope')
      else:
        self.scopelist.append(x)
        self.current_scope[x] = type_
      
    self.wordlist = []

    #print(self.current_scope)

  def add_procedure(self, word):
    if word == self.program_name:
      print(f'ERROR: Line {self._current_line}: \
      Program name CANNOT be used as a Procedure Name')
      return False

    if word in self.procedure_stack:
      print(f'ERROR: Line {self._current_line}: \
      variable "{word}" already declared on this scope')
    else:
      self.procedure_stack.append(word)
      #self.current_scope[word] = 'procedure'
    
    #print(self.current_scope)

  def check_if_declared(self, var_):
    if var_.symbol == self.program_name:
      print(f'ERROR: Line {self._current_line}: \
      Program name CANNOT be used in Commands or expressions')
      return False

    if var_.symbol in self.current_scope:
      if self.current_scope[var_.symbol] == 'procedure':
        return 'procedure'
      else:
        return 'variable'
      #print(f'OK - {var_.symbol} Line: {line}')
      pass
    else:
      print(f"Error: Line {self._current_line}: Variable {var_.symbol} \
      not declared in this scope")
      return False

  def eval_bottom(self, v3):
    self.eval_stack = []
    self.v3 = self.current_scope[v3.symbol]
  
  def eval_push(self, v):
    self.eval_stack.append(self.current_scope[v.symbol])

  def eval_push_p(self, var_):
    self.eval_stack.append(var_)

  def set_eval_flag(self, op):
    flag = ''
    if self.eval_flag not in ['logical_ar','invalid_op',]:
      if op.symbol in ['and','or']:
        flag = 'logical'
      elif op.symbol in ['+','-','/','*']:
        flag = 'arithm'
      elif op.kind == 'relation':
        flag = 'relation'
      
      if (flag == 'logical' and self.eval_flag == 'relation') or \
        (flag == 'relation' and self.eval_flag == 'logical') or \
        (flag == 'arithm' and self.eval_flag == 'logical') or \
        (flag == 'logical' and self.eval_flag == 'arithm'):
        self.eval_flag = 'invalid_op'
      else: self.eval_flag = flag


  def eval_run(self):
    if self._debug: print(f"\nType Check - {self.eval_stack}")
    while len(self.eval_stack) > 1:
      v1,v2 = self.eval_stack.pop(), self.eval_stack.pop()
      v3 = ''
      if v1 == 'integer' and v2 == 'integer':
        v3 = 'integer'
      elif (v1 == 'integer' and v2 == 'real') or \
          (v1 == 'real' and v2 in ['integer','real']):
        v3 = 'real'
      elif (v1 == 'boolean' and v2 == 'boolean'):
        v3 = 'boolean'
      else: 
        #print(f'Invalid Type operation {v1} x {v2} ')
        v3 = 'INVALID'
      self.eval_stack.append(v3)
      if self._debug: 
        print(f'{v1} X {v2} = {v3}')
        print(self.eval_stack)
    
    vx = self.eval_stack.pop()
    if self.eval_flag == 'invalid_op':
      print(f"ERROR: Line {self._current_line}: Invalid Operation, Cannot Mix Relational and Logical Operations in attribution")

    elif (self.v3 == 'boolean' and vx == 'boolean') or \
      (self.v3 == 'integer' and vx == 'integer') or \
      (self.v3 == 'real' and vx in ['integer','real']):
      if self._debug: print(f"{self.v3} x {vx} ALL OK")
      pass
    else:
      print(f'ERROR: Line {self._current_line}: Incompatible Types: should be {self.v3}, read {vx} ')
    self.eval_flag = '' # reseta flag
    