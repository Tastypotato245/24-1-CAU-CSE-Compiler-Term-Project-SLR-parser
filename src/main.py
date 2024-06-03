import sys
from data import rules, parse_table

class TreeNode:
    def __init__(self, value) :
        self.value=value
        self.children = []
        
    def add_child(self, child_node):
        self.children.append(child_node)

def print_tree(node, prefix="", is_last=True, is_root=True):
    # 루트 노드 출력
    if is_root:
        print(node.value)
    else:
        print(prefix + "|--" + str(node.value))
    
    # 새로운 prefix 계산
    new_prefix = prefix + ("    " if is_last else "|   ")
    
    # 자식 노드들 출력
    for i, child in enumerate(node.children):
        print_tree(child, new_prefix, i == len(node.children) - 1, is_root=False)


class SLRParser:
    def __init__(self, parse_table, rules):
        self.parse_table = parse_table
        self.rules = rules
        self.statestack = []
        self.statestack.append(0)
        self.inputStack=[]
        self.inputStack.append('$')
        self.nodequeue=[]

    def value_exists(self, current_state, current_token:str):
        try:
            value = self.parse_table[current_state][current_token]
            return True
        except KeyError:
            return False
        except IndexError:
            return False
    
    def parse(self, tokens):
        current_state=0
        token_index=0
        nodes=[]
        child_nodes=[]
        while True:
            #print('step')
            current_state=self.statestack[-1]
            current_token=tokens[token_index]

            try:
                action = self.parse_table[current_state][current_token]
            except KeyError:
                print(f"Reject at state {current_state}, unexpected token: {current_token}")
                self.statestack = []
                self.statestack.append(0)
                self.inputStack=[]
                self.inputStack.append('$')
                self.nodequeue=[]
                return False
            except IndexError:
                print(f"Reject at state {current_state}, unexpected token: {current_token}")
                self.statestack = []
                self.statestack.append(0)
                self.inputStack=[]
                self.inputStack.append('$')
                self.nodequeue=[]
                return False
            #print(f'current state: {current_state}')
            #print(f'current token: {current_token}')
            #print(f'action : {action}')
            
            if action.startswith('s'):
                self.inputStack.append(current_token)
                self.nodequeue.append(TreeNode(current_token))
                self.statestack.append(int(action[1:]))
                token_index+=1
            elif action.startswith('r'):
                node=TreeNode(self.rules[int(action[1:])][0])
                pop_=len(self.nodequeue)-self.rules[int(action[1:])][1]
                for _ in range(self.rules[int(action[1:])][1]):
                    self.statestack.pop()
                    #print(self.rules[int(action[1:])][1])
                    #print(f'debug : {int(action[1:])}')
                    #print(f'pop:{self.inputStack.pop()}')
                    node.add_child(self.nodequeue.pop(pop_))
                self.nodequeue.append(node)
                self.inputStack.append(self.rules[int(action[1:])][0])
                current_state=self.statestack[-1]
                current_token=self.inputStack[-1]
                try:
                    action = self.parse_table[current_state][current_token]
                except KeyError:
                    print(f"Reject at state {current_state}, unexpected token: {current_token}")
                    self.statestack = []
                    self.statestack.append(0)
                    self.inputStack=[]
                    self.inputStack.append('$')
                    self.nodequeue=[]
                    return False
                except IndexError:
                    print(f"Reject at state {current_state}, unexpected token: {current_token}")
                    self.statestack = []
                    self.statestack.append(0)
                    self.inputStack=[]
                    self.inputStack.append('$')
                    self.nodequeue=[]
                    return False
                #goto case임
                self.statestack.append(int(action))
            elif action=='acc':
                print_tree(node)
                self.statestack = []
                self.statestack.append(0)
                self.inputStack=[]
                self.inputStack.append('$')
                self.nodequeue=[]
                return True
            else :
                print(f"Reject at state {current_state}, unexpected token: {current_token}")
                self.statestack = []
                self.statestack.append(0)
                self.inputStack=[]
                self.inputStack.append('$')
                self.nodequeue=[]
                return False
            #print(f'state stack: {self.statestack}')
            #print(f'input stack: {self.inputStack}')
            #print()

def main():
    parser = SLRParser(parse_table, rules)
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        return
    
    input_file = sys.argv[1]
    
    with open(input_file, 'r') as file:
        lines = file.readlines()

    line_index=0
    for line in lines:
        line_index+=1
        tokens = line.strip().split()
        tokens.append("$")
#        print(tokens)
        if parser.parse(tokens):
            print("HOGEUN_KYUSUNG_SLR_PARSER RESULT: ACCEPT")
        else:
            print(f"line : {line_index}")
            print("HOGEUN_KYUSUNG_SLR_PARSER RESULT: REJECT")

if __name__ == "__main__":
    main()
