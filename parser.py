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
            isolate[0] = isolate[0].strip()
            if not isolate[0]:
                continue
            if isolate[0][0] == '=':
                err = add_fact(facts, isolate[0])
            elif isolate[0][0] == '?':
                err = add_query(queries, isolate[0])
            else:
                err = add_rule(isolate[0], rules)
            if err:
                return err
        return rules, facts, queries, None

def add_rule(self, rule, rules):
    err = check_valid(rule)
    if err:
        return err
    #if "<=>" in rule: to handle
        
    splitted = rule.split("=>")
    if not splitted[0] or not splitted[1]:
        return "Missing one side of a rule" # could improve error later
        
    splitted_right = splitted[1].split("+")

    new_rule = [] 
    new_rule[0] = splitted[0].split() # we assume that A + B is separated by space and not A+B
    new_rule[1] = splitted[1].split()
    for part in new_rule[0]:
        if len(part) != 1:
            return ("Error in format of rule statement")
    for part in new_rule[1]:
        if len(part) != 1:
            return ("Error in format of deduction")

    rules.append(new_rule)

    def add_fact(self, facts, line):
        i = 1#dodging '='
        while (i < len(line)):
            if (fact not in valid_char):
                return "Error, wrong symbol in facts"
            elif fact not in facts:
                facts.append(fact)
            # if already in fact, no error, just not added
            i += 1

    def add_query(self, queries, line):
        i = 1
        while (i < len(line)):
            if (query not in valid_char):
                return "Error, wrong symbol in queries"
            elif query not in queries:
                queries.append(query)
            i += 1