def parse_grammar(grammar_file):
    rules = []
    with open(grammar_file, 'r') as file:
        for line in file:
            line = line.strip()
            if '->' in line:
                left, right = line.split('->')
                left = left.strip()
                right = right.strip()
                symbols = right.split()
                rule_length = len(symbols)
                rules.append((left, rule_length))
    return rules

def parse_parse_table(parse_table_file):
    parse_table = []
    with open(parse_table_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('parse_table = ['):
                continue
            if line.startswith(']'):
                break
            if line.endswith(','):
                line = line[:-1]
            if line.startswith('{') and line.endswith('}'):
                row = eval(line)
                parse_table.append(row)
    return parse_table

grammar_file = './data/grammar.txt'
parse_table_file = './data/parse_table.txt'

rules = parse_grammar(grammar_file)
parse_table = parse_parse_table(parse_table_file)

if __name__ == "__main__":
    print("Rules:")
    for rule in rules:
        print(f"('{rule[0]}', {rule[1]})")

    print("\nParse Table:")
    for row in parse_table:
        print(row)
