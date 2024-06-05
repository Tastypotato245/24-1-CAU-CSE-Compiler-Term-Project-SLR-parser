import sys
from data import rules, parse_table


# 출력을 위한 트리 노드
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


# 부모에서 자식 방향으로 깊이 우선 탐색하며 출력함.
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


# 파서 부분임
class SLRParser:
    def __init__(self, parse_table, rules):
        self.parse_table = parse_table
        self.rules = rules
        self.statestack = []  # 상태를 관리할 스택임
        self.statestack.append(0)
        self.inputStack = []  # input을 넣으며 실제로 reduce 하는 데 사용하는 스택임
        self.inputStack.append('$')
        self.nodequeue = []  # tree를 관리할 스택

    # def value_exists(self, current_state, current_token: str):
    #     try:
    #         value = self.parse_table[current_state][current_token]
    #         return True
    #     except KeyError:
    #         return False
    #     except IndexError:
    #         return False

    def parse(self, tokens):
        current_state = 0
        token_index = 0
        nodes = []
        child_nodes = []
        # 내부에서 False 또는 True로 리턴될거라 루프 돌림
        while True:
            # print('step')
            current_state = self.statestack[-1]
            current_token = tokens[token_index]

            try:
                # 일단 파스 테이블에 현재 상태에서의 현재 토큰일 때의 action이 있는지를 봄
                action = self.parse_table[current_state][current_token]
            except KeyError:
                # 없으면 오류임. 이상한 토큰이 나온 것
                print(f"Reject at state {current_state}, unexpected token: {current_token}")
                self.statestack = []
                self.statestack.append(0)
                self.inputStack = []
                self.inputStack.append('$')
                self.nodequeue = []
                return False
            except IndexError:
                # 없으면 오류임. 이상한 토큰이 나온 것
                print(f"Reject at state {current_state}, unexpected token: {current_token}")
                self.statestack = []
                self.statestack.append(0)
                self.inputStack = []
                self.inputStack.append('$')
                self.nodequeue = []
                return False
            # print(f'current state: {current_state}')
            # print(f'current token: {current_token}')
            # print(f'action : {action}')

            if action.startswith('s'):
                # action이 s일 때는 shift를 함.
                # inputStack에 현재 토큰을 push함
                self.inputStack.append(current_token)
                # 트리에 출력에 활용하기 위해 큐에 붙임
                # 트리 구성을 위해 shift의 경우 queue 배열에 append함
                self.nodequeue.append(TreeNode(current_token))
                # 상태 스택에 이제 해야하는 action을 push함
                self.statestack.append(int(action[1:]))
                token_index += 1
            elif action.startswith('r'):
                # action이 r일 때는 reduce를 함.
                node = TreeNode(self.rules[int(action[1:])][0])
                # reduce할 노드의 갯수를 받아 queue 길이에서 빼줌
                # reduce의 경우 뒤에 추가된 노드가 우선적으로 reduce되지만 input의 순서 상 reduce되는 노드들의 경우 먼저 추가된 노드가 먼저 pop해야함
                # 이 때문에 reduce가 시작되는 위치에서 pop을 시작
                pop_ = len(self.nodequeue) - self.rules[int(action[1:])][1]
                # grammar인 rules에서 그것의 길이만큼 빼줘야함. 그만큼 reduce된 것이니.
                for _ in range(self.rules[int(action[1:])][1]):
                    self.statestack.pop()
                    # print(self.rules[int(action[1:])][1])
                    # print(f'debug : {int(action[1:])}')
                    # print(f'pop:{self.inputStack.pop()}')
                    # 트리에 pop한 노드 추가
                    # reduce될 노드의 개수만큼 for loop
                    node.add_child(self.nodequeue.pop(pop_))
                # reduce된 노드를 queue에 append
                self.nodequeue.append(node)
                self.inputStack.append(self.rules[int(action[1:])][0])
                # 현재 상태와 토큰을 업데이트 해줌 (top에 있는 거로 최신화 해주는 것임)
                current_state = self.statestack[-1]
                current_token = self.inputStack[-1]
                try:
                    # 파스 테이블에 현재 상태에서의 현재 토큰일 때의 action이 있는지를 봄 (위에 처음 시도한거랑 같음. goto 해야해서 한 번 여기서 하는 거)
                    action = self.parse_table[current_state][current_token]
                except KeyError:
                    print(f"Reject at state {current_state}, unexpected token: {current_token}")
                    self.statestack = []
                    self.statestack.append(0)
                    self.inputStack = []
                    self.inputStack.append('$')
                    self.nodequeue = []
                    return False
                except IndexError:
                    print(f"Reject at state {current_state}, unexpected token: {current_token}")
                    self.statestack = []
                    self.statestack.append(0)
                    self.inputStack = []
                    self.inputStack.append('$')
                    self.nodequeue = []
                    return False
                # goto case임
                self.statestack.append(int(action))
            elif action == 'acc':
                # accept할 때임.
                # accept의 경우 현재 node queue에 있는 node가 root
                print_tree(node)
                self.statestack = []
                self.statestack.append(0)
                self.inputStack = []
                self.inputStack.append('$')
                self.nodequeue = []
                return True
            else:
                print(f"Reject at state {current_state}, unexpected token: {current_token}")
                self.statestack = []
                self.statestack.append(0)
                self.inputStack = []
                self.inputStack.append('$')
                self.nodequeue = []
                return False
            # print(f'state stack: {self.statestack}')
            # print(f'input stack: {self.inputStack}')
            # print()


def main():
    parser = SLRParser(parse_table, rules)
    if len(sys.argv) < 2:
        # 예외처리하기
        print("Usage: team23_kyuho_slr_parser <input_file>")
        return

    input_file = sys.argv[1]

    with open(input_file, 'r') as file:
        lines = file.readlines()

    line_index = 0
    # 한 라인 단위로 파서를 돌림. 즉, 한 라인에 한 케이스(CODE로 REDUCE되는. 한 언어의 문장)가 올 수 있음.
    for line in lines:
        line_index += 1
        tokens = line.strip().split()
        tokens.append("$")
        #        print(tokens)
        if parser.parse(tokens):
            # 쉘 스크립트에서 이 스트링을 검출하기 위해 앞에 prefix가 있는 RESULT 를 출력함.
            print("HOGEUN_KYUSUNG_SLR_PARSER RESULT: ACCEPT")
        else:
            print(f"line : {line_index}")
            # 쉘 스크립트에서 이 스트링을 검출하기 위해 앞에 prefix가 있는 RESULT 를 출력함.
            print("HOGEUN_KYUSUNG_SLR_PARSER RESULT: REJECT")


if __name__ == "__main__":
    main()
