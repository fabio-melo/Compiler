from utils import Token, alert

class Syntax:
  def __init__(self, tokens, debug=True):
    self.tokens = tokens
    self._debug = ['Syntax', debug]

  def _get_symbol(self):
    if self.tokens:
      symbol = self.tokens.pop(0)
      return symbol
    else:
      return Token(False,False,False)
  

  def _read_symbol(self):
    if self.tokens:
      return self.tokens[0]
    else:
      return Token(False,False,False)


  def _alert(self, kind, alert):
    if self._debug:
      if kind == 0: print("INFO:  " + alert); return True
      elif kind == 1: print("WARNING:" + alert); return True
      elif kind == 2: print("ERROR: " + alert); return False

  def start(self):
    if not self.tokens:
      alert(self._debug, 2, "Cannot proceed: token list contains lexical errors.")
      return False

    #alert(self._debug, 0, "------ PROGRAM BLOCK -----")
    self._program() # program name
    #alert(self._debug,0,"------ VAR BLOCK ---------")
    self._variable_declarations() #var block
    #alert(self._debug,0,"------ BEGIN BLOCK -------")
    self._begin()
    self._procedure()


  def _program(self):
    if self._get_symbol().symbol == 'program' \
    and self._get_symbol().kind == 'identifier' \
    and self._get_symbol().symbol == ';':
      return alert(self._debug,0,"Program Block Validated")  
    else: return alert(self._debug,2,"undefined_program_declaration")

  def _variable_declarations(self):

    if self._read_symbol() and self._read_symbol().symbol == 'var':
      self._get_symbol() # consumir o var
      while self._read_symbol().kind is 'identifier':
        self._identifier_declarations()
      else:
        if self._read_symbol().symbol == 'begin':
          return alert(self._debug,0,"var_block_cleared")
        else:
          return alert(self._debug,2,"broken_var_declaration_block")

  def _begin(self):
      if self._read_symbol() and self._read_symbol().symbol == 'begin':
        self._procedure()

      else: return alert(self._debug,2,'no_begin_block')
      
  def _procedure(self):
    alert(self._debug,1,"NOT YET IMPLEMENTED")
  
  def _parameters(self):
    pass

  def _identifier_declarations(self):
    DATA_TYPES = ['integer', 'real', 'boolean']

    if self._get_symbol().kind == 'identifier':
      if self._get_symbol().symbol == ':':
        if self._get_symbol().symbol in DATA_TYPES:
          if self._get_symbol().symbol == ';':
            return alert(self._debug,0, 'identifier_validated')
          else: return alert(self._debug,2,'unclosed_var_declaration')
        else: return alert(self._debug,2,'untyped_var_declaration')
      else: return alert(self._debug,2,'missing_type_declaration')
    else: return alert(self._debug,2,'broken_var_declaration_block')
      
