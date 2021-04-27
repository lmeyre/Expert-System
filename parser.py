class Parser:

    #def __init__(self):
    valid_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def parse(self, file_data):
        facts = []
        rules = []  
        queries = []
        for line in file_data:
            print(line) # check if empty line appear and we have to handle or not
            isolate = line.split('#')
            if not isolate[0]: # if empty line
                continue
            isolate[0] = isolate[0].lstrip()
            if not isolate[0]:
                continue
            if isolate[0][0] == '=':
                add_fact(facts, isolate[0])
            elif isolate[0][0] == '?':
                add_query(queries, isolate[0])
            # else:
            #     add_rule(isolate[0], rules)
        return rules, facts, queries, None

# def add_rule(self, rule, rules):
#     if not check_valid(rule):
#         raise ValueError
#     if "<=>" in rule:
#         create_two(rule, rules)
#         return
#     splitted = rule.split("=>")
#     if not splitted[0] or not splitted[1]:
#         raise ValueError
#     splitted_right = splitted[1].split("+")
#     for value in splitted_right:
#         value = value.strip()
#         if not value[0].isupper():
#             continue
#     rules.append((splitted[0].strip(), splitted[1].strip()))

    def add_fact(self, facts, line):
        i = 1#dodging '='
        while (i < len(line)):
            if (fact not in valid_char):
                return "Error, wrong symbol in facts"
            elif fact not in facts:
                facts += fact
            # if already in fact, no error, just not added
            i += 1

    def add_query(self, queries, line):
        i = 1
        while (i < len(line)):
            if (query not in valid_char):
                return "Error, wrong symbol in queries"
            elif query not in queries:
                queries += query
            i += 1