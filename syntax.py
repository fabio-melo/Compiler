from token import Token
from alert import *


class Syntax:
  def __init__(self, tokens, debug=True):
    self.tokens = tokens
    self._debug = ['Syntax', debug]
    self._current_line = 0


  def _get(self):
    if self.tokens:
      symbol = self.tokens.pop(0)
      self._current_line = symbol.line
      return symbol
    else:
      return Token(False,False,False)
  

  def _read(self):
    if self.tokens:
      self._current_line = self.tokens[0].line
      return self.tokens[0]
    else:
      return Token(False,False,False)



  def _send_alert(self, code, alert_msg):
    ERRORMSG = ' Line ' + str(self._current_line) + ':  ' + alert_msg
    return alert(self._debug,code,ERRORMSG)

  def start(self):
    if not self.tokens:
      alert(self._debug, 2, "Cannot proceed: token list contains lexical errors.")
      return False
    self._program()


  def _program(self):
    if self._get().symbol == 'program':
      if self._get().kind == 'identifier':
        if self._get().symbol == ';':
          self._send_alert(0,P_DEFI_E + VALIDATED)  
          self._var_declarations()
          self._procedure_list()
          self._composite_command()
          if self._get().symbol == '.':
            self._send_alert(0, "PROGRAM PASSED!!!")
        else: return self._send_alert(2,P_DEFI_E + M_SEMI)
      else: return self._send_alert(2,P_DEFI_E + M_IDENT)
    else: return self._send_alert(2,P_DEFI_E + M_RESERV)


  def _procedure_list(self):
    """
    """
    while self._read().symbol == 'procedure':
      self._procedure()
      if self._read().symbol == ';':
        self._send_alert(0, 'Procedure List - Semicolon')
        self._get()
        break


  def _procedure(self):
    if self._read().symbol == 'procedure':
      self._send_alert(0, "Procedure")
      self._get()
      if self._read().kind == 'identifier':
        self._send_alert(0, "Procedure ID")
        self._get()
        self._arguments()
        if self._read().symbol == ';':
          self._var_declarations()
          self._procedure_list()
          self._composite_command()
        else:
          self._send_alert(2, "Procedure Declaration - Missing Semicolon")




  def _var_declarations(self):
    if self._read().symbol == 'var':
      self._send_alert(0, "Variable Declaration - VAR")
      self._get() # consumir o var
      self._identifier_list_type()
      while self._read().kind == 'identifier':
        self._identifier_list_type()


  def _identifier_list(self):
    """ (Recursive)
    <identifier> | <identifier>,<identifier>
    """
    if self._read().kind == 'identifier':
      self._send_alert(0, 'Identifier List - Identifier')
      self._get()

      while self._read().symbol == ',':
        self._send_alert(0, 'Identifier List - Comma')
        self._get()
        if self._read().kind == 'identifier':
          self._send_alert(0, 'Identifier List - Identifier')
          self._get()
        else: 
          return self._send_alert(2, 'Identifier List - Missing Identifier')


  def _identifier_list_type(self):

    self._identifier_list()
    if self._get().symbol == ':':
      if self._get().symbol in DATA_TYPES:
        if self._get().symbol == ';':
          self._send_alert(0, "Identifier Type - Validated")
        else: return self._send_alert(2,"Identifier - Missing Semicolon")
      else: return self._send_alert(2,"Identifier - Missing Type declaration")
    else: return self._send_alert(2,"Identifier - Missing ':' symbol")

  def _arguments(self):
    if self._read().symbol == '(':
      self._send_alert(0, 'Arguments - OPENED')
      self._get()
      self._parameter_list()
      if self._read().symbol == ')':
        self._send_alert(0, 'Arguments - CLOSED')
        self._get()
      else:
        return self._send_alert(2, 'Missing ")" on Procedure Arguments')
      

  def _parameter_list(self):
    self._parameter_list_type()
    while self._read().symbol == ';':
      self._send_alert(0, "Parameter List Semicolon ; ")
      self._get()
      self._parameter_list_type()


  def _parameter_list_type(self):
    """
    """
    self._identifier_list()
    if self._read().symbol == ':':
      self._get()
      if self._read().symbol in DATA_TYPES:
        self._get()
        self._send_alert(0, "Parameter Type - Validated")
      else: return self._send_alert(2,"Parameter - Missing Type declaration")
    else: return self._send_alert(2,"Parameter - Missing ':' symbol")


  def _composite_command(self):
    """
    comando_composto →
    begin
    comandos_opcionais
    end
    comandos_opcionais →
    lista_de_comandos
    | ε
    """

    if self._read().symbol == 'begin':
      self._send_alert(0, "Composite Command - BEGIN")
      self._get()
      while self._read().symbol != 'end':
        self._command_list()
      else:
        self._get()
        self._send_alert(0, "Composite Command - END")
    else: 
      self._send_alert(2, "Error: Missing Begin Statement")



  def _command_list(self):
    self._command()
    while self._read().symbol == ';':
      self._send_alert(0, "Command List - ; ")
      self._get()
      self._command()


  def _command(self):
    """
    comando →
    variável := expressão
    | ativação_de_procedimento
    | comando_composto
    | if expressão then comando parte_else
    | while expressão do comando
    """
    temp = self._read()

    #VARIABLE : EXPRESSION / PROCEDURE ACTIVATION 

    if temp.kind == 'identifier':
      self._get()
      if self._read().kind == 'attribution':
        self._send_alert(0, 'Variable := Expression')
        self._get()
        self._expression()
      elif self._read().symbol == '(':
        self._send_alert(0, 'Procedure Activation (Expression List) - OPENED')
        self._get()
        self._expression_list()
        if self._read().symbol == ')':
          self._send_alert(0, 'Procedure Activation (Expression List) - CLOSED')
          self._get()
        else:
          return self._send_alert(2, 'Missing ")" on Procedure Activation')
      else:
        self._send_alert(0, "Procedure Activation - Simple")

    elif temp.symbol == "if":
      self._send_alert(0, "Command - IF")
      self._get() 
      self._expression()
      if self._read().symbol == "then":
        self._send_alert(0, "Command - THEN")
        self._get()
        self._command()
        # Parte Else
        while self._read().symbol == "else":
          self._send_alert(0, "Command - ELSE")
          self._get()
          self._command()
      else:
        return self._send_alert(2, "Missing 'THEN' reserved word")
    elif temp.symbol == "while":
      self._send_alert(0, 'Command - WHILE')
      self._get()
      self._expression()
      if self._read().symbol == 'do':
        self._send_alert(0, 'Command - DO')
        self._get()
        self._command()
      else:
        return self._send_alert(2, 'Missing "DO" reserved word')

    elif temp.symbol == 'begin':
      self._send_alert(0, "Command -> Composite Command")
      self._composite_command()


  def _expression_list(self):

    self._expression()

    while self._read().symbol == ',': 
      self._send_alert(0, "Comma")
      self._get(); self._expression()   


  def _expression(self):
    """
    """
    self._simple_expression()

    while self._read().kind == 'relation': 
      self._get(); self._simple_expression()   


  def _simple_expression(self):
    """
    <simple_ex> -> <termo> <simple_ex'> | <signal> <termo>
    <simple_ex'> -> <addition> <termo> <simple_ex'>
    """
    # primeiro sinal (caso exista) e termo
    if self._read().symbol in ['+','-']:
      self._get(); self._term()
    else: 
      self._term()

    # enquanto aparecer adição, loopar em busca de termos    
    while self._read().kind == 'addition':
      self._send_alert(0, "Addition")
      self._get(); self._term()


  def _term(self):
    """ 
    <termo> -> <fator> <termo'> |
    <termo'> -> <op_mult> <fator> <termo'>
    | ϵ
    """
    self._factor()

    while self._read().kind == 'multiplication': 
      self._send_alert(0, "Multiplication")
      self._get(); self._factor()
    

  def _factor(self):
    """ (Factor)
    """
    factor = self._read()
    if factor.kind in ['integer','real','boolean']:
      self._get()
      return self._send_alert(0, 'Factor - Number/Bool - Ok!')
    elif factor.kind == 'identifier': 
      self._get()
      if self._read().symbol == '(':
        self._send_alert(0, "id(Expression) Opened")
        self._get()
        self._expression_list()
        #TO-DO LIST OF EXPRESSION
        if self._read().symbol == ')':
          self._get()
          self._send_alert(0, "id(Expression) Closed")
        else: 
          return self._send_alert(2, "Unclosed Expression - Missing ')'")
      else:
        #VALIDADO IDENTIFICADOR
        self._send_alert(0, "Factor -  Identifier - Ok!")
    elif factor.symbol == 'not':
      self._get()
      self._send_alert(0, "NOT")
      self._factor()
    elif factor.symbol == '(':
      self._send_alert(0, "(Expression) Opened")
      self._get(); self._expression()
      if self._read().symbol == ')':
        self._get()
        self._send_alert(0, "(Expression) Closed")
      else:
        return self._send_alert(2, 'Unclosed Expression - Missing ")" ')
    else:
      self._send_alert(2,"Missing Factor")
    


        