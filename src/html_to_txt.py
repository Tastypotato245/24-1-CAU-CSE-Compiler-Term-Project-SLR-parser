from bs4 import BeautifulSoup

with open("./data/SLRtable.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')
lr_table_view_div = soup.find('div', id='lrTableView')

if lr_table_view_div:
    th_tags = lr_table_view_div.find_all('th')
    td_tags = lr_table_view_div.find_all('td')

    symbol = []
    table = []

    check_symbol = False
    for th in th_tags:
        if check_symbol:
            symbol.append(th.text.strip())
        if th.text.strip() == "GOTO":
            check_symbol = True

    for i, td in enumerate(td_tags):
        command = td.text.strip()
        if i % (len(symbol) + 1) == 0:
            table.append({})
        elif command == "":
            continue
        elif command.isdigit():
            table[-1][symbol[i % (len(symbol) + 1) - 1]] = int(command)
        elif command[0] == 's':
            table[-1][symbol[i % (len(symbol) + 1) - 1]] = 's' + command[1:]
        elif command[0] == 'r':
            table[-1][symbol[i % (len(symbol) + 1) - 1]] = 'r' + command[1:]
        elif command == "acc":
            table[-1][symbol[i % (len(symbol) + 1) - 1]] = 'acc'

    with open("./table_data/parsing_table.txt", "w", encoding="utf-8") as file:
        file.write("parse_table = [\n")
        for state in table:
            file.write("    {")
            for symbol, action in state.items():
                file.write(f"'{symbol}': '{action}', ")
            file.write("},\n")
        file.write("]\n")

