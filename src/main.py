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
        self.stack = [0]

    def parse(self, tokens):
        i = 0
        while True:
            state = self.stack[-1]
            current_token = tokens[i]

            # 디버깅 출력을 추가합니다.
            print(f"Current stack: {self.stack}")
            print(f"Current token: {current_token}")
            print(f"Current state: {state}")

            if current_token not in self.parse_table[state]:
                raise SyntaxError(f"Unexpected token '{current_token}' at position {i}")

            action = self.parse_table[state][current_token]
            print(f"Action: {action}")

            if action.startswith('s'):
                self.stack.append(int(action[1:]))
                i += 1

            elif action.startswith('r'):
                rule_index = int(action[1:])
                if rule_index >= len(self.rules):
                    raise IndexError(f"Rule index {rule_index} out of range")
                lhs, rhs_len = self.rules[rule_index]
                for _ in range(len(self.stack)):
                    self.stack.pop()

                state = self.stack[-1]
                if lhs not in self.parse_table[state]:
                    raise SyntaxError(f"Unexpected symbol '{lhs}' in parse table")
                self.stack.append(self.parse_table[state][lhs])

            elif action == 'acc':
                print("Accepted")
                return
            else:
                raise SyntaxError("Unknown action")

    def display_stack(self):
        print("Stack:", self.stack)


# 문법 규칙
rules = [
    ('E', 3),  # E -> E + T
    ('E', 1),  # E -> T
    ('T', 3),  # T -> T * F
    ('T', 1),  # T -> F
    ('F', 3),  # F -> ( E )
    ('F', 1)   # F -> id
]

# 파서 테이블 (예제에서는 고정된 테이블 사용)
parse_table = [
    {'id': 's5', '(': 's4', 'E': 1, 'T': 2, 'F': 3},
    {'+': 's6', '$': 'acc'},
    {'+': 'r2', '*': 's7', '$': 'r2'},
    {'+': 'r4', '*': 'r4', '$': 'r4'},
    {'id': 's5', '(': 's4', 'E': 8, 'T': 2, 'F': 3},
    {'+': 'r5', '*': 'r5', '$': 'r5'},  # Changed r6 to r5
    {'id': 's5', '(': 's4', 'T': 9, 'F': 3},
    {'id': 's5', '(': 's4', 'F': 10},
    {'+': 's6', ')': 's11'},
    {'+': 'r1', '*': 's7', ')': 'r1', '$': 'r1'},
    {'+': 'r3', '*': 'r3', ')': 'r3', '$': 'r3'},
    {'+': 'r5', '*': 'r5', ')': 'r5', '$': 'r5'}
]

# 토큰 예제 (id + id * id)
tokens = ['id', '+', 'id', '*', 'id', '$']

parser = SLRParser(parse_table, rules)
parser.parse(tokens)

