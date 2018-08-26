
DATA_TYPES = ['integer', 'real', 'boolean']

ID_DEF = "Identifier Declaration : "
P_DEFI_E = "Program Definition : "
M_RESERV = "Missing Reserved Word"
M_SEMI = "Missing Semicolon ';'"
M_COL = "Missing Colon ':'"
M_IDENT = "Missing Identifier"
M_TYPE = "Missing Type"
M_COMMA = "Missing Comma"
VALIDATED = "ALL CLEAR!!"
CLEARED = "Block END"
ERRORS = "Errors Found"

def alert(debug, kind, alert):
  if kind == 0: 
    if debug: print("[" + debug[0] + "]INFO:  " + alert)
    return True
  elif kind == 1: 
    if debug: print("[" + debug[0] + "]WARNING:" + alert)
    return True
  elif kind == 2: 
    if debug: print("[" + debug[0] + "]ERROR:  " + alert)
    return False
