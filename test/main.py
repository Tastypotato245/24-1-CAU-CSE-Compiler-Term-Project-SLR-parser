from data.data import grammar, parse_table

def parse(input_tokens):

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        return
    
    input_file = sys.argv[1]
    
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        tokens = line.strip().split()
        if parse(tokens):
            print("ACCEPT")
        else:
            print("REJECT")

if __name__ == "__main__":
    main()

