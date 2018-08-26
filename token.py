
class Token:
  def __init__(self, symbol, kind, line):
    self.symbol = symbol
    self.kind = kind
    self.line = line

  def print_token(self):
    print(str(self.line) + ' ' + str(self.kind) + ' ' + str(self.symbol))


def load(program_file):
  with open(program_file,'r') as pr: # assegurar que o arquivo irá ser fechado
    program = pr.read()
  listified_program = []
  for p in program: listified_program.append(p)
  return listified_program
