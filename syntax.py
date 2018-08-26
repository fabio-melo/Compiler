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
    self._expression_list()

    #self._program_id() # program name
    #self._var_declarations() #var block
     # self._subprograms()
    #self._begin()
    #self._procedure()


  def _program_id(self):
    if self._get().symbol == 'program':
      if self._get().kind == 'identifier':
        if self._get().symbol == ';':
          return self._send_alert(0,P_DEFI_E + VALIDATED)  
        else: return self._send_alert(2,P_DEFI_E + M_SEMI)
      else: return self._send_alert(2,P_DEFI_E + M_IDENT)
    else: return self._send_alert(2,P_DEFI_E + M_RESERV)


  def _var_declarations(self):
    if self._read().symbol == 'var':
      self._get() # consumir o var
      self._var_declaration_list()



  def _var_declaration_list(self):
    """ (Recursive)
    < identifier_list > : <type> ;


    """
    inside = False
    while True:
      if self._read().kind == 'identifier':
        inside = True
        self._identifier_list()

        if self._get().symbol == ':':
          if self._get().symbol in DATA_TYPES:
            if self._get().symbol == ';':
              inside = False
              self._send_alert(0, ID_DEF + VALIDATED)
            else: return self._send_alert(2,ID_DEF + M_SEMI)
          else: return self._send_alert(2,ID_DEF + M_TYPE)
      elif not inside:
        return self._send_alert(0, ID_DEF + CLEARED)
      else:
        return self._send_alert(2, ID_DEF + ERRORS)



  def _identifier_list(self):
    """ (Recursive)
    <identifier> | <identifier>,<identifier>
    """
    if self._read().kind == 'identifier':
        self._get()
        if self._read().symbol == ',':
          self._get()
          if self._read().kind == 'identifier':
            self._identifier_list()
          else: 
            return self._send_alert(2, ID_DEF + M_IDENT)



  def _expression_list(self):

    self._expression()

    while self._read().symbol == ',': 
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
    


        
