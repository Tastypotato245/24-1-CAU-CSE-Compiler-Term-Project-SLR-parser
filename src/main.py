import sys
from data import rules, parse_table

class SLRParser:
    def __init__(self, parse_table, rules):
        self.parse_table = parse_table
        self.rules = rules
        self.statestack = []
        self.statestack.append(0)
        self.inputStack=[]
        self.inputStack.append('$')

    def parse(self, tokens):
        current_state=0
        token_index=0
        while True:
            #print('step')
            current_state=self.statestack[-1]
            current_token=tokens[token_index]
            action= self.parse_table[current_state][current_token]
#            print(f'current state: {current_state}')
#            print(f'current token: {current_token}')
#            print(f'action : {action}')

            if action.startswith('s'):
                self.inputStack.append(current_token)
                self.statestack.append(int(action[1:]))
                token_index+=1
            elif action.startswith('r'):
                for _ in range(self.rules[int(action[1:])][1]):
                    self.statestack.pop()
#                   print(self.rules[int(action[1:])][1])
#                   print(f'debug : {int(action[1:])}')
#                   print(f'pop:{self.inputStack.pop()}')
                self.inputStack.append(self.rules[int(action[1:])][0])
                current_state=self.statestack[-1]
                current_token=self.inputStack[-1]
                action=self.parse_table[current_state][current_token]
                #goto case임
                self.statestack.append(int(action))
            elif action=='acc':
                self.statestack = []
                self.statestack.append(0)
                self.inputStack=[]
                self.inputStack.append('$')
                return True
            else :
                self.statestack = []
                self.statestack.append(0)
                self.inputStack=[]
                self.inputStack.append('$')
                return False
#            print(f'state stack: {self.statestack}')
#            print(f'input stack: {self.inputStack}')
#            print()

def main():
    parser = SLRParser(parse_table, rules)
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        return
    
    input_file = sys.argv[1]
    
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        tokens = line.strip().split()
        tokens.append("$");
        print(tokens)
        if parser.parse(tokens):
            print("ACCEPT")
        else:
            print("REJECT")

if __name__ == "__main__":
    main()
