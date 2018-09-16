import re, sys
from collections import deque


class Token:
  def __init__(self, symbol, kind, line, id_):
    self.symbol = symbol
    self.kind = kind
    self.line = line
    self.id_ = id_

  def print_token(self):
    print(str(self.line) + ' ' + str(self.kind) + ' ' + str(self.symbol))


class Lexer:
  def __init__(self, program_file, debug=False):
    self.tokens = []
    self._current_symbol = []
    self._current_line = 1
    self._current_id = 0
    self._queue = deque(self._load(program_file))
    self._debug = debug
    self._errors = []


  def _load(self, program_file):
    with open(program_file,'r') as pr: # assegurar que o arquivo irá ser fechado
      program = pr.read()
    listified_program = []
    for p in program: listified_program.append(p)
    return listified_program


  def _fetch_next_char(self): 
    return self._queue[0] if self._queue else False


  def _fetch_next_non_blank_char(self):
    while True:
      if not self._queue: 
        return False
      elif re.match(r'[\t\r\f\040]', self._queue[0]): 
        self._queue.popleft()
      elif re.match(r'[\n]',self._queue[0]): 
        self._current_line += 1
        self._queue.popleft()
      else: 
        return self._queue[0]


  def _send_alert(self, alert_code, line=False):
    if alert_code == 'unclosed_comment':
      self._errors.append([line, 'unclosed_comment'])
      ERRORMSG = 'Unclosed comment on line ' + str(line)
      print("[Syntax] ERROR:" + ERRORMSG)
      sys.exit()
      return False
    elif alert_code == 'invalid':
      self._errors.append([self._current_line, 'invalid'])
      ERRORMSG = 'Invalid symbol \"' + str(''.join(self._current_symbol)) \
            + '\" on line ' + str(self._current_line)
      print("[Syntax] ERROR:" + ERRORMSG)
      sys.exit()
      return False



  def _consume_char(self): 
    if self._queue: self._current_symbol.append(self._queue.popleft())


  def _start(self):
    while self._queue:
      char = self._fetch_next_non_blank_char()

      if not char: break

      elif re.match(r'[a-zA-Z_]',char): self._identifier()
      elif re.match(r'[0-9]',char): self._number()
      elif re.match(r'[\{]',char): self._comments()
      elif re.match(r'[\.\;\(\),:+-/\*=<>]',char): self._special()
      else: self._invalid()


  def _identifier(self):
    while True:
      char = self._fetch_next_char()
      if not char: break
      if re.match('[a-zA-Z0-9_]', char): 
        self._consume_char()
      else: break
    self._commit_token('identifier')


 
  def _number(self):
    invalid, real = False, False
    while True:
      char = self._fetch_next_char()
      if not char: break
      if re.match('[0-9]',char): 
        self._consume_char()
      elif re.match('[.]',char) and not real:
        real = True
        self._consume_char()
      elif re.match('[.]',char) and real:
        invalid = True
        self._consume_char()
      elif re.match('[a-zA-Z_]',char):
        invalid = True
        self._consume_char()
      else: break

    if invalid: 
      self._commit_token('invalid')
    elif real: 
      self._commit_token('real')
    else: 
      self._commit_token('integer')


  def _special(self):
    char_1 = self._fetch_next_char(); self._consume_char()
    char_2 = self._fetch_next_char() # Testar sem consumir

    # Simbolos Compostos de 2 caracteres
    if char_1 is '/' and char_2 is '/':
      self._commit_token('comment')
      self._line_comment()

    if char_1 is ':' and char_2 is '=':
      self._consume_char() 
      self._commit_token('attribution')

    elif (char_1 is '<' and char_2 in ['=','>']) or \
       (char_1 is '>' and char_2 is '='):        
      self._consume_char()
      self._commit_token('relation')

    elif (char_1 is '-' and char_2 is '>'):
      self._consume_char()
      self._commit_token('new_type')
    
    elif (char_1 is '*' and char_2 is '*'):
      self._consume_char()
      self._commit_token('exponent')


    # Simbolos Compostos de unico caractere

    elif char_1 in ['.',';','(',')',':',',']: 
      self._commit_token('delimiter')
    
    elif char_1 in ['=','<','>']:
      self._commit_token('relation')

    elif char_1 in ['+','-']: 
      self._commit_token('addition')
    elif char_1 in ['*','/']: 
      self._commit_token('multiplication')
 

  def _comments(self):
    _line = self._current_line
    while True:
      if not self._queue:
        self._send_alert('unclosed_comment',line=_line)
        return False
      elif re.match(r'[\}]', self._queue[0]): 
        self._queue.popleft()
        break
      elif re.match(r'[\n]',self._queue[0]): 
        self._current_line += 1
        self._queue.popleft()    
      else: 
        self._queue.popleft()                


  def _line_comment(self):
    while True:
      if not self._queue:
        return False
      elif re.match(r'[\n]',self._queue[0]): 
        self._current_line += 1
        self._queue.popleft()
        break    
      else: 
        self._queue.popleft()  

  def _invalid(self):
    self._consume_char()
    self._commit_token('invalid')


  def _commit_token(self,code):

    RESERVED_WORDS = [ 'program', 'var', 'integer', 'real', 'boolean', 
               'procedure', 'begin', 'end', 'if', 'then', 'else', 
               'while', 'do', 'not' ]

    if self._current_symbol:
      temp = ''.join(self._current_symbol)
      if code == 'identifier':
        if temp in RESERVED_WORDS:
          self.tokens.append(Token(temp, 'reserved', self._current_line,self._current_id))
        elif temp == 'and':
          self.tokens.append(Token(temp, 'multiplication', self._current_line, self._current_id))
        elif temp == 'or':
          self.tokens.append(Token(temp, 'addition', self._current_line,self._current_id))
        elif temp in ['true','false']:
          self.tokens.append(Token(temp, 'boolean', self._current_line,self._current_id))
        else:
          self.tokens.append(Token(temp, 'identifier', self._current_line,self._current_id))
      elif code == 'invalid':
        self._send_alert('invalid')
      elif code == 'comment':
        pass #não faz nada
      else:
        self.tokens.append(Token(temp, code, self._current_line,self._current_id))

      self._current_symbol = [] # reseta a variavel temporaria
      self._current_id += 1

  def _print_tokens(self):
    if self._errors:
      ERRORMSG = str(len(self._errors)) + " Lexical Errors were Found!, cannot continue"
      print("[Syntax] ERROR:" + ERRORMSG)
      sys.exit()

    print('\n\n[Lexer] ----- SYMBOL TABLE -----')
    print("{:<5} {:<8} {:<20} {:<15} ".format("Line", 'Id', 'Symbol','Kind'))
    for x in self.tokens:
      print("{:<5} {:<8} {:<20} {:<15} ".format(x.line, x.id_, x.symbol, x.kind))
    


  # Metodos Publicos


  def run(self):
    self._start()

    if self._debug:
      self._print_tokens()
      print('')

    if self._errors: 
      print("Lexical Errors Found")
      return False
    else: 
      if self._debug: print('[PASSED] Lexical Analysis')
      return self.tokens
  