from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from collections import deque
from lexer import Token
from semantic import Semantic

import sys

def trace(func):
  def wrapper(self, *args, **kwargs):
    self._current_level += 1
    if self._debug: print(f'Trace: ({self._read().id_}) \
      {self._read().symbol} -> {func.__name__} {self._current_level}')
    # \n'f'-> {args[1]}')
    original_result = func(self,*args, **kwargs)
    self._current_level -= 1
    #print(f'SYN: ({self._read().id_}) {self._read().symbol} -> 
    # (Return) {func.__name__} {self._current_level}')
    #print(f'TRACE: {func.__name__}() ' f'returned {original_result!r}')
    return original_result
  return wrapper


class Syntax(Semantic):
  def __init__(self, tokens, debug=False):
    super().__init__()
    self.tokens = deque(tokens)
    self._debug = debug
    self._current_line = 0
    self._tree = Node('Start')
    self._count = 99
    self._current_level = 0

  def __repr__(self):
    return "Syntax Object"

  def export_to_file(self,file_):
    self.start()
    with open(file_,'w') as file:
      for x in DotExporter(self._tree):
        file.write(x)

  def _get(self):
    """
    Retorna e apaga o token da lista
    """
    if self.tokens:
      symbol = self.tokens.popleft()
      self._current_line = symbol.line
      return symbol
    else:
      return Token(False,False,False,False)
  

  def _read(self):
    """
    (Somente) lê o próximo token da lista
    """
    if self.tokens:
      self._current_line = self.tokens[0].line
      return self.tokens[0]
    else:
      return Token(False,False,False,False)


  def _leaf(self,curr):
    tok = self._get()
    return Node(str("("+ str(tok.id_) + ") " + tok.symbol), parent=curr)

  def _node(self, curr, msg):
    self._count += 1
    return Node(str(self._count) + ': ' + msg , parent=curr)


  def _error(self, alert_msg):
    ERRORMSG = '[Syntax] ERROR: Line ' + str(self._current_line) + ':  ' + alert_msg
    print(ERRORMSG)
    return sys.exit()


  def start(self):
    """
    Inicia o Analizador e gera a arvore
    """
    if not self.tokens:
      self._error("Cannot proceed: token list contains lexical errors.")
      return False

    self._program(self._tree)
    #print(RenderTree(self._tree))


  @trace
  def _program(self, curr):

    curr = self._node(curr, 'Program')


    # PROGRAM ID ;
    if self._read().symbol == 'program': self._leaf(curr)
    else: self._error("Program: Missing 'Program' Reserved Word")

    if self._read().kind == 'identifier': 
      self.program_name = self._read().symbol
      self._leaf(curr)
    else: self._error("Program: Missing Program Identifier") 
    
    if self._read().symbol == ';': self._leaf(curr)
    else: self._error("Program: Missing Semicolon")

    # Other Functions
    self._var_declaration(curr)
    self._subprogram_declaration_list(curr)
    self._composite_command(curr)
    # Ending Dot
    if self._read().symbol == '.': self._leaf(curr)
    else: self._error("Program: Missing Ending Dot")

    # Check if ended
    if not self._read().symbol:
      if self._debug: print("Syntax Analysis - OK")
    else: self._error("Program: Tokens after Ending Dot")

  @trace
  def _subprogram_declaration_list(self,curr):
 
    curr = self._node(curr, 'Subprogram Declaration List')


    if self._read().symbol == 'procedure':
      self._subprogram_declaration(curr)
      if self._read().symbol == ';':
        self._leaf(curr)
        self._subprogram_declaration_list(curr)
      else:
        self._error("Subprogram Declaration - Missing Semicolon")
    else:
      Node( '[' + str(self._count) + '] empty', parent=curr)


  @trace
  def _subprogram_declaration(self,curr):

    curr = self._node(curr, 'Subprogram Declaration')


    if self._read().symbol == 'procedure':
      self._leaf(curr)

      if self._read().kind == 'identifier':
        self.add_procedure(self._read().symbol)
        self._leaf(curr)
        self.add_scope() #escopo
        self._arguments(curr)
        if self._read().symbol == ';':
          self._leaf(curr)
          self._var_declaration(curr)
          self._subprogram_declaration_list(curr)
          self._composite_command(curr)
          self.drop_scope() #dropa
        else:
          self._error( "Procedure Declaration - Missing Semicolon")
      else:
          self._error("Missing Procedure Identifier")


  @trace
  def _data_types(self,curr):
    curr = self._node(curr, 'Type')
    
    DATA_TYPES = ['integer', 'real', 'boolean']

    if self._read().symbol in DATA_TYPES:
      self.add_var(self._read().symbol)
      self._leaf(curr)
    else: 
      return self._error("Missing Type declaration")


  @trace
  def _var_declaration(self,curr):

    curr = self._node(curr, 'Var Declaration')


    if self._read().symbol == 'var':
      self._leaf(curr)
      self._var_declaration_list(curr)
    else:
      Node( '[' + str(self._count) + '] empty', parent=curr)


  @trace
  def _var_declaration_list(self,curr):
    """
    """
    curr = self._node(curr, 'Var Declaration List')

    self._identifier_list(curr)

    if self._read().symbol == ':':
      self._leaf(curr) 
      self._data_types(curr)
    else: 
      return self._error("Identifier - Missing ':' symbol")

    if self._read().symbol == ';':
      self._leaf(curr)
    else: 
      return self._error("Identifier - Missing Semicolon")

    if self._read().kind == 'identifier':
      self._var_declaration_list(curr)


  @trace
  def _identifier_list(self,curr):

    curr = self._node(curr, 'Identifier List')


    if self._read().kind == 'identifier':
      self.add_word(self._read().symbol)
      self._leaf(curr)
    else: 
      return self._error( 'Identifier List - Missing Identifier')

    if self._read().symbol == ',':
      self._leaf(curr)
      self._identifier_list(curr)
    

  @trace
  def _arguments(self,curr):

    curr = self._node(curr, 'Arguments')

    if self._read().symbol == '(':
      self._leaf(curr)
      self._parameter_list(curr)
      if self._read().symbol == ')':
        self._leaf(curr)
      else:
        return self._error( 'Missing ")" on Procedure Arguments')



  @trace
  def _parameter_list(self,curr):
 
    curr = self._node(curr, 'Parameter List')


    self._identifier_list(curr)

    if self._read().symbol == ':':
      self._leaf(curr)
      self._data_types(curr)
    else: 
      return self._error("Parameter - Missing ':' symbol")

    if self._read().symbol == ';':
      self._leaf(curr)
      self._parameter_list(curr)


  @trace
  def _composite_command(self,curr):
    # begin <optional_command> end

    curr = self._node(curr, 'Composite Command')


    if self._read().symbol == 'begin': self._leaf(curr)
    else: self._error( "Composite Command: Missing Begin Statement")

    self._optional_command(curr)
      
    if self._read().symbol == 'end': self._leaf(curr)
    else: self._error( "Composite Command: Missing END Statement")
      

  @trace
  def _optional_command(self,curr):
    curr = self._node(curr, 'Optional Command')

    if self._read().symbol != 'end':
      self._command_list(curr)
    else:
      Node( '[' + str(self._count) + '] empty', parent=curr)


  @trace
  def _command_list(self,curr):
    curr = self._node(curr, 'Command List')


    self._command(curr)

    if self._read().symbol == ';':
      self._leaf(curr)
      self._command_list(curr)


  @trace
  def _command(self,curr):

    curr = self._node(curr, 'Command')

    temp = self._read()


    #VARIABLE : EXPRESSION / PROCEDURE ACTIVATION 

    if temp.kind == 'identifier':
      
      declared = self.check_if_declared(temp)
      

      self._leaf(curr)
      
      if self._read().kind == 'attribution':
        self._leaf(curr)

        if declared == 'variable': self.eval_bottom(temp)

        self._expression(curr)

        self.eval_run() #RUN EVAL

      elif self._read().symbol == '(':
        self._leaf(curr)
        self._expression_list(curr)
        if self._read().symbol == ')':
          self._leaf(curr)
        else:
          return self._error( 'Missing ")" on Procedure Activation')


    elif temp.symbol == "if":
      self._leaf(curr)
      self._expression(curr)
      if self._read().symbol == "then":
        self._leaf(curr)
        self._command(curr)
        # Parte Else
        self._else_part(curr)
        
      else:
        return self._error( "Missing 'THEN' reserved word")
    elif temp.symbol == "while":
      self._leaf(curr)
      self._expression(curr)
      if self._read().symbol == 'do':
        self._leaf(curr)
        self._command(curr)
      else:
        return self._error( 'Missing "DO" reserved word')

    elif temp.symbol == 'do':
      self._leaf(curr)
      self._command(curr)
      
      if self._read().symbol == 'while':
        self._leaf(curr)
        if self._read().symbol == '(':
          self._leaf(curr)
          self._expression(curr)
          if self._read().symbol == ')':
            self._leaf(curr)
          else: self._error('missing )')
        else: self._error('missing (')
      else: self._error('missing while')



    elif temp.symbol == 'begin':
      self._composite_command(curr)

    else:
      return self._error("Broken Command")


  @trace
  def _else_part(self, curr):
    curr = self._node(curr, 'Else Part')

    
    if self._read().symbol == "else":
      self._leaf(curr)
      self._command(curr)
      self._else_part(curr)
    else:
      Node( '[' + str(self._count) + '] empty', parent=curr)


  @trace
  def _expression_list(self,curr):

    curr = self._node(curr, 'Expression List')


    self._expression(curr)

    if self._read().symbol == ',': 
      self._leaf(curr)
      self._expression_list(curr)   


  @trace
  def _expression(self,curr):

    curr = self._node(curr, 'Expression')


    self._simple_expression(curr)

    if self._read().kind == 'relation': 
      self._op_relation(curr)
      self._expression(curr)   


  @trace
  def _op_relation(self,curr):

    curr = self._node(curr, 'Relation OP')


    if self._read().kind == 'relation':
      self._leaf(curr)


  @trace
  def _simple_expression(self,curr):

    curr = self._node(curr, 'Simple Expression')

    # primeiro sinal (caso exista) e termo
    if self._read().symbol in ['+','-']:
      self._signal(curr)
      self._term(curr)
    else: 
      self._term(curr)

    # enquanto aparecer adição, loopar em busca de termos    
    if self._read().kind == 'addition':
      self._op_addition(curr)
      self._simple_expression(curr)


  @trace
  def _signal(self,curr):

    curr = self._node(curr, 'Signal')

    if self._read().symbol in ['+','-']:
      self._leaf(curr)


  @trace
  def _op_addition(self,curr):

    curr = self._node(curr, 'Additive OP')

    if self._read().kind == 'addition':
      self._leaf(curr)


  @trace
  def _op_multiplication(self,curr):

    curr = self._node(curr, 'Multiplicative OP')

    if self._read().kind == 'multiplication':
      self._leaf(curr)


  @trace
  def _term(self,curr):

    curr = self._node(curr, 'Term')


    self._factor(curr)

    if self._read().kind == 'multiplication': 
      self._op_multiplication(curr)
      self._term(curr)


  @trace
  def _factor(self,curr):

    curr = self._node(curr, 'Factor')


    factor = self._read()
    if factor.kind in ['integer','real','boolean']:
      self.eval_push_p(factor.kind)
      self._leaf(curr)

    elif factor.kind == 'identifier': 

      self.check_if_declared(factor)
      self.eval_push(factor)
      self._leaf(curr)
      if self._read().symbol == '(':
        self._leaf(curr)
        self._expression_list(curr)
        if self._read().symbol == ')':
          self._leaf(curr)
        else: 
          return self._error( "Unclosed Expression - Missing ')'")
    elif factor.symbol == 'not':
      self._leaf(curr)
      self._factor(curr)
    elif factor.symbol == '(':
      self._leaf(curr)
      self._expression(curr)
      if self._read().symbol == ')':
        self._leaf(curr)
      else:
        return self._error( 'Unclosed Expression - Missing ")" ')
    else:
      self._error("Missing Factor")

  def _variable(self, curr):
      
      curr = self._node(curr, 'Variable')
      self._leaf(curr)

  def _procedure_activation(self, curr):
      
      curr = self._node(curr, 'Procedure Activation')
      self._leaf(curr)

