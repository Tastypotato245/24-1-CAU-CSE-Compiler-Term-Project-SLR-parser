import os
import random

grammar = {
    'CODE': ['CODE_D'],
    'CODE_D': ['VDECL CODE_D', 'FDECL CODE_D', ''],
    'VDECL': ['VTYPE id ;', 'VTYPE ASSIGN ;'],
    'ASSIGN': ['id = RHS'],
    'RHS': ['EXPR', 'literal', 'character', 'BOOLSTR'],
    'EXPR': ['EXPR_D ADDSUB EXPR', 'EXPR_D'],
    'EXPR_D': ['EXPR_DD MULTDIV EXPR_D', 'EXPR_DD'],
    'EXPR_DD': ['( EXPR )', 'id', 'num'],
    'FDECL': ['VTYPE id ( ARG ) { BLOCK RETURN }'],
    'ARG': ['VTYPE id MOREARGS', ''],
    'MOREARGS': [', VTYPE id MOREARGS', ''],
    'BLOCK': ['STMT BLOCK', ''],
    'STMT': ['VDECL', 'ASSIGN ;', 'if ( COND ) { BLOCK } ELSE', 'while ( COND ) { BLOCK }'],
    'COND': ['BOOLSTR COMP COND', 'BOOLSTR'],
    'ELSE': ['else { BLOCK }', ''],
    'RETURN': ['return RHS ;'],
    'VTYPE': ['int', 'float', 'char'],
    'ADDSUB': ['+', '-'],
    'MULTDIV': ['*', '/'],
    'COMP': ['==', '!='],
    'BOOLSTR': ['true', 'false']
}

# 최대 깊이 도달 시 사용하는 우선순위 배열. terminal을 보장하기 위해서...
example_grammar = {
    'CODE': [''],
    'CODE_D': [''],
    'VDECL': ['int id ;', 'char id = literal ;', 'char id = character ;', 'int id = true ;', 'int id = false ;'],
    'ASSIGN': ['id = literal', 'id = character', 'id = true', 'id = false'],
    'RHS': ['literal', 'character', 'true', 'false'],
    'EXPR': ['num'],
    'EXPR_D': ['num'],
    'EXPR_DD': ['num'],
    'FDECL': ['char id ( ) { return character ; }', 'int id ( ) { return true ; }'],
    'ARG': ['int id'],
    'MOREARGS': [', float id'],
    'BLOCK': ['return literal ;', 'return character ;', 'return true ;', 'return false ;'],
    'STMT': ['return literal ;', 'return character ;', 'return true ;', 'return false ;'],
    'COND': ['true', 'false'],
    'ELSE': ['else { return character ; }', 'else { return true ; }'],
    'RETURN': ['return literal ;', 'return character ;', 'return true ;', 'return false ;'],
    'VTYPE': ['int', 'float', 'char'],
    'ADDSUB': ['+', '-'],
    'MULTDIV': ['*', '/'],
    'COMP': ['==', '!='],
    'BOOLSTR': ['true', 'false']
}

# 터미널 기호
terminals = [';', 'id', 'literal', 'character', 'num', 'true', 'false', 'int', 'float', 'char', '+', '-', '*', '/', '==', '!=', '(', ')', '{', '}', 'else', 'return']

# 랜덤 언어 생성 함수
def generate_random_language(symbol, depth, max_depth):
    if depth >= max_depth:
        expansion = random.choice(example_grammar[symbol])
    else:
        expansion = random.choice(grammar[symbol])
    
    result = []
    for token in expansion.split():
        if token in grammar:
            result.append(generate_random_language(token, depth + 1, max_depth))
        else:
            result.append(token)
    
    return ' '.join(result)

# 혹시 몰라 만든 검증 함수
def validate_terminal_end(language):
    tokens = language.split()
    return all(token in terminals for token in tokens[-1:])

os.makedirs('rand_example', exist_ok=True)

max_depth = 15
num_cases_per_depth = 30
for depth in range(1, max_depth + 1):
    filename = f'rand_example/{depth}'
    cases = []
    for _ in range(num_cases_per_depth):
        language = generate_random_language('CODE', 0, depth)
        if validate_terminal_end(language):
            cases.append(language)
        else:
            print(f"Validation failed for depth {depth}")
    
    with open(filename, 'w') as file:
        file.write('\n'.join(cases))

print("File generation complete.")
