###def input():
#        with open('C:\\Users\\phg52\\OneDrive\\바탕 화면\\compiler_term_proj\\24-1-CAU-CSE-Compiler-Term-Project-SLR-parser\\src\\input.txt', 'r', encoding='utf-8') as file:
#            # 파일 내용 전체를 읽어서 변수에 저장
#            content = file.read()
#        tokens = content.split()
#        print(tokens)    
#        return tokens
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
            print('step')
            current_state=self.statestack[-1]
            current_token=tokens[token_index]
            action= self.parse_table[current_state][current_token]
            print(f'current state: {current_state}')
            print(f'current token: {current_token}')
            print(f'action : {action}')

            if action.startswith('s'):
                self.inputStack.append(current_token)
                self.statestack.append(int(action[1]))
                token_index+=1
            elif action.startswith('r'):
                for _ in range(self.rules[int(action[1])][1]):
                    self.statestack.pop()
                    print(self.rules[int(action[1])][1])
                    print(f'pop:{self.inputStack.pop()}')
                self.inputStack.append(self.rules[int(action[1])][0])
                current_state=self.statestack[-1]
                current_token=self.inputStack[-1]
                action=self.parse_table[current_state][current_token]
                self.statestack.append(int(action))
            elif action=='acc':
                print('Accept')
                return
            print(f'state stack: {self.statestack}')
            print(f'input stack: {self.inputStack}')
            print()

# 문법 규칙
rules = [
    ('E', 1),  # E -> T
    ('T', 3),  # T -> T * F
    ('T', 1),  # T -> F
    ('F', 3),  # F -> ( T )
    ('F', 1)   # F -> id
]

# 파서 테이블 (예제에서는 고정된 테이블 사용)
parse_table = [
    { '(': 's3', 'id': 's4', 'T': 1, 'F': 2},
    {'*': 's5', '$': 'acc'},
    {'*': 'r2', ')': 'r2', '$': 'r2'},  # Changed r2 to r4
    {'(': 's3','id': 's4', 'T': 6, 'F': 2},  # Changed T to 7
    {'*': 'r4', ')': 'r4', '$':'r4'},
    {'(': 's3', 'id': 's4', 'F':7},  # Changed r6 to r5 and removed '+'
    {'*': 's5', ')': 's8'},
    {'*': 'r1', ')': 'r1', '$': 'r1'},
    {'*': 'r3', ')': 'r3', '$': 'r3'},
]

# 토큰 예제 (id + id * id)
tokens = ['id', '*', 'id', '$']

parser = SLRParser(parse_table, rules)
parser.parse(tokens)

