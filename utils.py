# Utils

class Token:
  def __init__(self, symbol, kind, line):
    self.symbol = symbol
    self.kind = kind
    self.line = line

  def print_token(self):
    print(str(self.line) + ' ' + str(self.kind) + ' ' + str(self.symbol))


def alert(debug, kind, alert):
  if kind == 0: 
    if debug: print("[" + debug[0] + "]INFO:  " + alert)
    return True
  elif kind == 1: 
    if debug: print("[" + debug[0] + "]WARNING:" + alert)
    return True
  elif kind == 2: 
    if debug: print("[" + debug[0] + "]ERROR: " + alert)
    return False

def load(program_file):
  with open(program_file,'r') as pr: # assegurar que o arquivo irá ser fechado
    program = pr.read()
  listified_program = []
  for p in program: listified_program.append(p)
  return listified_program



def gui_l(results):
  from tkinter import FLAT,Entry,NSEW,END,GROOVE,mainloop,Tk
  root = Tk()
  root.title("Análise Lexica")
  rows = []
  i = 1
  cols = []
  e = Entry(relief=FLAT)
  e.grid(row=0, column=0, sticky=NSEW)
  e.insert(END, "Line")
  cols.append(e)
  e = Entry(relief=FLAT)
  e.grid(row=0, column=1, sticky=NSEW)
  e.insert(END, "Symbol")
  cols.append(e)
  e = Entry(relief=FLAT)
  e.grid(row=0, column=2, sticky=NSEW)
  e.insert(END, "Kind")
  cols.append(e)

  rows.append(cols)

  for x in results:
    cols = []
    e = Entry(relief=GROOVE)
    e.grid(row=i, column=0, sticky=NSEW)
    e.insert(END, x.line)
    cols.append(e)
    e = Entry(relief=GROOVE)
    e.grid(row=i, column=1, sticky=NSEW)
    e.insert(END, x.symbol)
    cols.append(e)
    e = Entry(relief=GROOVE)
    e.grid(row=i, column=2, sticky=NSEW)
    e.insert(END, x.kind)
    cols.append(e)
    i +=1

    rows.append(cols)

  mainloop()