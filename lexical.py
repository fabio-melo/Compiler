import io, re, typing
from sys import argv


RESERVED_WORDS = [ 'program', 'var', 'integer', 'real', 'boolean', 'procedure', 
                   'begin', 'end', 'if', 'then', 'else', 'while', 'do', 'not' ]

class Token:
    def __init__(self, symbol, kind: str, line: int):
        self.symbol = symbol
        self.kind = kind
        self.line = line

    def print_token(self):
        print(self.line, end=' ')
        print(self.kind, end=' ')
        print(self.symbol)

class LexicalFSM:
    def __init__(self, program, verbose=True):
        self.tokens = []
        self.current_symbol = []
       # self.temp_code = 'undefined'
        self.current_line = 1
        self.queue = program
        self.verbose = verbose
 
    def send_alert(self, alert_code, line=False):
        if self.verbose:
            if alert_code == 'unclosed_comment':
                print('ERROR: unclosed comment on line ' + str(line))
            elif alert_code == 'invalid':
                print('ERROR: invalid symbol \"' + str(''.join(self.current_symbol)) \
                      + '\" on line ' + str(self.current_line))
        else:
            print('WARNING: Program contain Lexical Errors')
            


    def fetch_next_char(self): 
        return self.queue[0] if self.queue else False

    def fetch_next_non_blank_char(self):
        while True:
            if not self.queue: 
                return False
            elif re.match(r'[\t\r\f\040]', self.queue[0]): 
                self.queue.pop(0)
            elif re.match(r'[\n]',self.queue[0]): 
                self.current_line += 1
                self.queue.pop(0)
            else: 
                return self.queue[0]


    def consume_char(self): 
        if self.queue: self.current_symbol.append(self.queue.pop(0))

    # Automato

    def q_start(self):
        while self.queue:
            char = self.fetch_next_non_blank_char()

            if not char: break

            if re.match(r'[a-zA-Z_]',char): self.q_identifier()
            elif re.match(r'[0-9]',char): self.q_number()
            elif re.match(r'[\{]',char): self.q_comments()
            elif re.match(r'[\.\;\(\),:]',char): self.q_delimiter()
            elif re.match(r'[=<>]',char): self.q_relation()
            elif re.match(r'[+-/\*]',char): self.q_arithmethic()
            else: self.q_invalid()

    def q_identifier(self):
        while True:
            char = self.fetch_next_char()
            if not char: break
            if re.match('[a-zA-Z0-9_]', char): 
                self.consume_char()
            else: break
        self.commit_token('identifier')

    def q_number(self):
        invalid, real = False, False
        while True:
            char = self.fetch_next_char()
            if not char: break
            if re.match('[0-9]',char): 
                self.consume_char()
            elif re.match('[.]',char) and not real:
                real = True
                self.consume_char()
            elif re.match('[.]',char) and real:
                invalid = True
                self.consume_char()
            elif re.match('[a-zA-Z_]',char):
                invalid = True
                self.consume_char()
            else: break

        if invalid: 
            self.commit_token('invalid')
        elif real: 
            self.commit_token('real')
        else: 
            self.commit_token('integer')

    def q_delimiter(self):
        char = self.fetch_next_char()
        self.consume_char()
        if char == ':':
            test_for_equals = self.fetch_next_char()
            if test_for_equals == '=':
                self.consume_char()
                self.commit_token('attibution')
                return
        self.commit_token('delimiter')

    def q_relation(self):
        char = self.fetch_next_char()
        self.consume_char()

        test = self.fetch_next_char()   
        if char is '<' and test in ['=','>'] or (char is '>' and test is '='):        
           self.consume_char()
        self.commit_token('relation')        

    def q_arithmethic(self):
        char = self.fetch_next_char()
        self.consume_char()
        if char in ['+','-']: self.commit_token('addition')
        elif char in ['*','/']: self.commit_token('multiplication')

    def q_comments(self):
        _line = self.current_line
        while True:
            if not self.queue:
                self.send_alert('unclosed_comment',line=_line)
                return False
            elif re.match(r'[\}]', self.queue[0]): 
                self.queue.pop(0)
                break
            elif re.match(r'[\n]',self.queue[0]): 
                self.current_line += 1
                self.queue.pop(0)    
            else: 
                self.queue.pop(0)                


    def q_invalid(self):
        self.consume_char()
        self.commit_token('invalid')

    def commit_token(self,code):
        if self.current_symbol:
            temp = ''.join(self.current_symbol)
            if code == 'identifier':
                if temp in RESERVED_WORDS:
                    self.tokens.append(Token(temp, 'reserved', self.current_line))
                elif temp in 'and':
                    self.tokens.append(Token(temp, 'multiplication', self.current_line))
                elif temp in 'or':
                    self.tokens.append(Token(temp, 'addition', self.current_line))
                else:
                    self.tokens.append(Token(temp, 'identifier', self.current_line))
            elif code == 'invalid':
                self.send_alert('invalid')
            else:
                self.tokens.append(Token(temp, code, self.current_line))

            self.current_symbol = [] # reseta a variavel temporaria
  
def load_program(program_file):
    with open(program_file,'r') as pr: # assegurar que o arquivo irá ser fechado
        program = pr.read()
    listified_program = []
    for p in program: listified_program.append(p)
    return listified_program


def gui_results(results):
    from tkinter import FLAT,Entry,NSEW,END,GROOVE,Button,mainloop,Tk
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

if __name__ == '__main__':
    
    programa = load_program('code.for') 
    l = LexicalFSM(programa)
    l.q_start()
    for x in l.tokens:
        x.print_token()

    if '-gui' in argv:
        gui_results(l.tokens)
        