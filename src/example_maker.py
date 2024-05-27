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

# accpet에 대한 최대 깊이 도달 시 사용하는 우선순위 배열. terminal을 보장하기 위해서...
example_grammar_accept = {
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
    'BLOCK': ['int id ;'],
    'STMT': ['int id ;'],
    'COND': ['true', 'false'],
    'ELSE': ['else { }'],
    'RETURN': ['return literal ;', 'return character ;', 'return true ;', 'return false ;'],
    'VTYPE': ['int', 'float', 'char'],
    'ADDSUB': ['+', '-'],
    'MULTDIV': ['*', '/'],
    'COMP': ['==', '!='],
    'BOOLSTR': ['true', 'false']
}
# 터미널 기호. validation을 위해
terminals = [';', 'id', 'literal', 'character', 'num', 'true', 'false', 'int', 'float', 'char', '+', '-', '*', '/', '==', '!=', '(', ')', '{', '}', 'else', 'return']

# reject에 대한 최대 깊이 도달 시 사용하는 우선순위 배열
example_grammar_reject = {
    'CODE': ['!~'],
    'CODE_D': ['}~'],
    'VDECL': ['char id literal ;'],
    'ASSIGN': ['id === true'],
    'RHS': ['rhserror'],
    'EXPR': ['exprerror'],
    'EXPR_D': ['exprerror'],
    'EXPR_DD': ['exprerror'],
    'FDECL': ['char ) return character ; }'],
    'ARG': ['int id id'],
    'MOREARGS': [', float id ;'],
    'BLOCK': ['int id num ;'],
    'STMT': ['int num num = id ;'],
    'COND': ['?'],
    'ELSE': ['else ()'],
    'RETURN': ['false return ;'],
    'VTYPE': ['isanghantype'],
    'ADDSUB': ['+~-'],
    'MULTDIV': ['*.../'],
    'COMP': ['==='],
    'BOOLSTR': ['idonno']
}

# 랜덤 언어 생성 함수 accept cases만 생성함.
def generate_random_language(symbol, depth, max_depth):
    if depth >= max_depth:
        expansion = random.choice(example_grammar_accept[symbol])
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

# 리젝트 케이스를 생성하는 함수
def generate_reject_language(symbol, depth, max_depth, used_example_grammar_reject):
    if depth >= max_depth:
        expansion = random.choice(example_grammar_reject[symbol])
        used_example_grammar_reject[0] = True
    else:
        expansion = random.choice(grammar[symbol])
    
    result = []
    for token in expansion.split():
        if token in grammar:
            result.append(generate_reject_language(token, depth + 1, max_depth, used_example_grammar_reject))
        else:
            if random.random() < 0.98:
                result.append(token)
            else:
                # 랜덤한 잘못된 토큰을 삽입
                result.append(random.choice(['wrong', 'error', 'invalid', 'unknown']))
    
    return ' '.join(result)

# 리젝트 케이스에 example_grammar_reject의 내용을 추가하는 함수
def ensure_reject_case_uses_example_grammar(case):
    parts = case.split()
    for key, expansions in example_grammar_reject.items():
        for expansion in expansions:
            if expansion in case:
                return case  # 이미 사용된 경우
    # 사용되지 않은 경우 추가
    key = random.choice(list(example_grammar_reject.keys()))
    expansion = random.choice(example_grammar_reject[key])
    parts.append(expansion)
    return ' '.join(parts)

os.makedirs('rand_example', exist_ok=True)

max_depth = 20
num_cases_per_depth = 500
for depth in range(1, max_depth + 1):
    if depth < 10:
        accept_filename = f'rand_example/accept_0{depth}.test'
        reject_filename = f'rand_example/reject_0{depth}.test'
    else:
        accept_filename = f'rand_example/accept_{depth}.test'
        reject_filename = f'rand_example/reject_{depth}.test'

    accept_cases = []
    reject_cases = []
    
    for _ in range(num_cases_per_depth):
        accept_language = generate_random_language('CODE', 0, depth)
        if validate_terminal_end(accept_language):
            accept_cases.append(accept_language)
        
        used_example_grammar_reject = [False]
        reject_language = generate_reject_language('CODE', 0, depth, used_example_grammar_reject)
        if not used_example_grammar_reject[0]:
            reject_language = ensure_reject_case_uses_example_grammar(reject_language)
        if reject_language:  # 빈 문자열이 아닌 경우에만 추가
            reject_cases.append(reject_language)
    
    with open(accept_filename, 'w') as accept_file:
        accept_file.write('\n'.join(accept_cases))
    
    with open(reject_filename, 'w') as reject_file:
        reject_file.write('\n'.join(reject_cases))

print("File generation complete.")

