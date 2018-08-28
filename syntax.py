from utils import Token
from alert import alert
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

import sys



class Syntax:
  def __init__(self, tokens, debug=True):
    self.tokens = tokens
    self._debug = ['Syntax', debug]
    self._current_line = 0
    self._tree = Node('Start')
    self._count = 100

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
      symbol = self.tokens.pop(0)
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


  def _add(self,curr):
    tok = self._get()
    return Node(str("("+ str(tok.id_) + ") " + tok.symbol), parent=curr)

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

  def _program(self, curr):
    '''
    Programa. 
    recebe o nó atual.
    '''
    curr = Node(str(self._count) + ' Program', parent=curr)
    self._count += 1

    if self._read().symbol == 'program':
      self._add(curr)

      if self._read().kind == 'identifier':
        self._add(curr)

        if self._read().symbol == ';':
          self._add(curr)

          if self._read().symbol == 'var':
            self._var_declaration(curr)
          self._procedure_list(curr)

          if self._read().symbol == 'begin':
            self._composite_command(curr)
          if self._read().symbol == '.':
            self._add(curr)

            if self._read().symbol is not False:
              self._error("Program - Tokens after Ending Dot")
            else:
              print("IT WORKS - Código Verificado")
          else: 
            self._error("Missing Program '.' ending dot")
        else: return self._error("Program Definition - Missing Semicolon")
      else: return self._error("Program Definition - Missing Identifier")
    else: return self._error("Program Definition - Missing Reserved Word")


  def _procedure_list(self,curr):
    """
    """
    curr = Node( str(self._count) + " : Procedure List", parent=curr)
    self._count += 1

    empty = True

    while self._read().symbol == 'procedure':
      self._procedure(curr)
      empty = False
      if self._read().symbol == ';':
        self._add(curr)
        break

    if empty: Node( " empty ", parent=curr)


  def _procedure(self,curr):
    """
    """
    curr = Node( str(self._count) + " : Procedure", parent=curr)
    self._count += 1

    if self._read().symbol == 'procedure':
      self._add(curr)

      if self._read().kind == 'identifier':
        self._add(curr)
        self._arguments(curr)
        if self._read().symbol == ';':
          self._add(curr)
          if self._read().symbol == 'var':
            self._var_declaration(curr)
          self._procedure_list(curr)
          if self._read().symbol == 'begin':
            self._composite_command(curr)
        else:
          self._error( "Procedure Declaration - Missing Semicolon")

  def _data_types(self,curr):

    DATA_TYPES = ['integer', 'real', 'boolean']
    curr = Node( str(self._count) + " : Type", parent=curr)
    self._count += 1
    if self._read().symbol in DATA_TYPES:
      self._add(curr)
    else: 
      return self._error("Missing Type declaration")


  def _var_declaration(self,curr):
    """
    """
    curr = Node( str(self._count) + " : Var Declarations", parent=curr)
    self._count += 1

    if self._read().symbol == 'var':
      self._add(curr)
      self._var_declaration_list(curr)
      while self._read().kind == 'identifier':
        self._var_declaration_list(curr)


  def _var_declaration_list(self,curr):
    """
    """
    curr = Node( str(self._count) + " : Var Declaration List", parent=curr)
    self._count += 1

    self._identifier_list(curr)
    if self._read().symbol == ':':
      self._add(curr)
      self._data_types(curr)
      if self._read().symbol == ';':
        self._add(curr)
      else: return self._error("Identifier - Missing Semicolon")
    else: return self._error("Identifier - Missing ':' symbol")


  def _identifier_list(self,curr):
    """ 
    <identifier> | <identifier>,<identifier>
    """
    curr = Node( str(self._count) + " : Identifier List", parent=curr)
    self._count += 1
    
    if self._read().kind == 'identifier':
      self._add(curr)

      while self._read().symbol == ',':
        self._add(curr)
        if self._read().kind == 'identifier':
          self._add(curr)
        else: 
          return self._error( 'Identifier List - Missing Identifier')



  def _arguments(self,curr):

    curr = Node( str(self._count) + " : (Arguments)", parent=curr)
    self._count += 1

    if self._read().symbol == '(':
      self._add(curr)
      self._parameter_list(curr)
      if self._read().symbol == ')':
        self._add(curr)
      else:
        return self._error( 'Missing ")" on Procedure Arguments')
      

  def _parameter_list(self,curr):
 
    curr = Node( str(self._count) + " : Parameter List", parent=curr)
    self._count += 1
    
    self._parameter_list_type(curr)
    while self._read().symbol == ';':
      self._add(curr)
      self._parameter_list_type(curr)


  def _parameter_list_type(self,curr):
    """
    """
    curr = Node( str(self._count) + " : Parameter List Type", parent=curr)
    self._count += 1

    self._identifier_list(curr)
    if self._read().symbol == ':':
      self._add(curr)
      self._data_types(curr)
    else: return self._error("Parameter - Missing ':' symbol")


  def _composite_command(self,curr):
    """
    comando_composto →
    begin
    comandos_opcionais
    end
    comandos_opcionais →
    lista_de_comandos
    | ε
    """
    curr = Node( str(self._count) + " : Composite Command", parent=curr)
    self._count += 1

    if self._read().symbol == 'begin':
      self._add(curr)
      self._optional_command(curr)
      if self._read().symbol == 'end':
        self._add(curr)
      else:
        self._error( "Missing END Block")
    else: 
      self._error( "Error: Missing Begin Statement")


  def _optional_command(self,curr):
    curr = Node( str(self._count) + " : Optional Command", parent=curr)
    self._count += 1
    if self._read().symbol != 'end':
      self._command_list(curr)
    else:
      Node("empty", parent=curr)

  def _command_list(self,curr):
    curr = Node( str(self._count) + " : Command List", parent=curr)
    self._count += 1

    self._command(curr)
    while self._read().symbol == ';':
      self._add(curr)
      self._command(curr)


  def _command(self,curr):
    """
    comando →
    variável := expressão
    | ativação_de_procedimento
    | comando_composto
    | if expressão then comando parte_else
    | while expressão do comando
    """
    temp = self._read()
    curr = Node( str(self._count) + " : Command", parent=curr)
    self._count += 1

    #VARIABLE : EXPRESSION / PROCEDURE ACTIVATION 

    if temp.kind == 'identifier':
      self._add(curr)
      if self._read().kind == 'attribution':
        self._add(curr)
        self._expression(curr)
      elif self._read().symbol == '(':
        self._add(curr)
        self._expression_list(curr)
        if self._read().symbol == ')':
          self._add(curr)
        else:
          return self._error( 'Missing ")" on Procedure Activation')


    elif temp.symbol == "if":
      self._add(curr)
      self._expression(curr)
      if self._read().symbol == "then":
        self._add(curr)
        self._command(curr)
        # Parte Else
        self._else_part(curr)
        
      else:
        return self._error( "Missing 'THEN' reserved word")
    elif temp.symbol == "while":
      self._add(curr)
      self._expression(curr)
      if self._read().symbol == 'do':
        self._add(curr)
        self._command(curr)
      else:
        return self._error( 'Missing "DO" reserved word')

    elif temp.symbol == 'begin':
      self._composite_command(curr)

    else:
      return self._error("Broken Command")


  def _else_part(self, curr):
    curr = Node( str(self._count) + 'Else Part', parent=curr)
    self._count += 1
    
    while self._read().symbol == "else":
      self._add(curr)
      self._command(curr)
      

  def _expression_list(self,curr):

    curr = Node( str(self._count) + 'Expression List', parent=curr)
    self._count += 1

    self._expression(curr)

    while self._read().symbol == ',': 
      self._add(curr)
      self._expression(curr)   


  def _expression(self,curr):
    """
    """
    curr = Node( str(self._count) + ': Expression', parent=curr)
    self._count += 1

    self._simple_expression(curr)

    while self._read().kind == 'relation': 
      self._add(curr)
      self._simple_expression(curr)   


  def _simple_expression(self,curr):
    """
    <simple_ex> -> <termo> <simple_ex'> | <signal> <termo>
    <simple_ex'> -> <addition> <termo> <simple_ex'>
    """

    curr = Node( str(self._count) + ': Simple Expression', parent=curr)
    self._count += 1
    # primeiro sinal (caso exista) e termo
    if self._read().symbol in ['+','-']:
      self._add(curr)
      self._term(curr)
    else: 
      self._term(curr)

    # enquanto aparecer adição, loopar em busca de termos    
    while self._read().kind == 'addition':
      self._add(curr) 
      self._term(curr)


  def _term(self,curr):
    """ 
    <termo> -> <fator> <termo'> |
    <termo'> -> <op_mult> <fator> <termo'>
    | ϵ
    """

    curr = Node( str(self._count) + ': Term', parent=curr)
    self._count += 1

    self._factor(curr)

    while self._read().kind == 'multiplication': 
      self._add(curr) 
      self._factor(curr)
    

  def _factor(self,curr):
    """ (Factor)
    """

    curr = Node( str(self._count) + ': Factor', parent=curr)
    self._count += 1


    factor = self._read()
    if factor.kind in ['integer','real','boolean']:
      self._add(curr)
    elif factor.kind == 'identifier': 
      self._add(curr)
      if self._read().symbol == '(':
        self._add(curr)
        self._expression_list(curr)
        #TO-DO LIST OF EXPRESSION
        if self._read().symbol == ')':
          self._add(curr)
        else: 
          return self._error( "Unclosed Expression - Missing ')'")
    elif factor.symbol == 'not':
      self._add(curr)
      self._factor(curr)
    elif factor.symbol == '(':
      self._add(curr)
      self._expression(curr)
      if self._read().symbol == ')':
        self._add(curr)
      else:
        return self._error( 'Unclosed Expression - Missing ")" ')
    elif factor.symbol == 'begin':
      self._composite_command(curr)
    else:
      self._error("Missing Factor")
    


        