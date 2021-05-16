import re
import rule as rule_obj
class Parser:

    def __init__(self, args):
        self.valid_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.args = args

    def parse(self, file_data):
        facts = []
        rules = []  
        queries = []
        for line in file_data:
            if self.args.show :
                print(line) # check if empty line appear and we have to handle or not
            isolate = line.split('#')
            if not isolate[0]: # if empty line
                continue
            isolate[0] = isolate[0].strip()
            if not isolate[0]:
                continue
            if isolate[0][0] == '=':
                err = self.add_fact(facts, isolate[0])
            elif isolate[0][0] == '?':
                err = self.add_query(queries, isolate[0])
            else:
                err = self.add_rule(isolate[0], rules)
            if err:
                return err
        return rules, facts, queries, None

    def add_fact(self, facts, line):
        i = 1#dodging '='
        while (i < len(line)):
            if (line[i] not in self.valid_char):
                return "Error, wrong symbol in facts"
            elif line[i] not in facts:
                facts.append(line[i])
            # if already in fact, no error, just not added
            i += 1

    def add_query(self, queries, line):
        i = 1
        while (i < len(line)):
            if (line[i] not in self.valid_char):
                return "Error, wrong symbol in queries"
            elif line[i] not in queries:
                queries.append(line[i])
            i += 1

    def add_rule(self, rule, rules):
        err = self.check_valid(rule)
        if err:
            return err
        if "<=>" in rule:
            self.handle_bilateral_rule(rule, rules)
        else:    
            splitted = rule.split("=>")
            if not splitted[0] or not splitted[1]:
                return "Missing one side of a rule" # could improve error later

            new_rule = rule_obj.rule()
            for c in splitted[0]:
                if c  == ' ':
                    continue
                else:
                    new_rule.statement.append(c)
            for c in splitted[1]:
                if c  == ' ':
                    continue
                else:
                    new_rule.deduction.append(c)

            rules.append(new_rule)

    def check_valid(self, rule):
        if rule.count("=>") != 1:#handle both <=> and =>
            return ("Error in format of rule linking")
        
        rule_divided = rule.split("<=>") if "<=>" in rule else rule.split("=>")
        
        # rule_part = rule.split()
        # for part in rule_part:# we can have 2 char without space if its !A or (A  or  A)
        #     if len(part) != 1:
        #         if part[0] != '!' and ("(" not in part or ")" not in part or ):
        #             return ("Error in format of rule statement")

        err = self.check_valid_part(rule_divided[0])
        if err:
            return err
        err = self.check_valid_part(rule_divided[1])
        if err:
            return err


    def check_valid_part(self, rule_part):
        open_parenthesis = 0
        letter_next = True
        for idx, c in enumerate(rule_part):
            if c == " ":
                continue
            elif c == "(":
                if letter_next is False:
                    return ("Problem in parenthesis order")
                open_parenthesis += 1
            elif c == ")":
                if letter_next is True:
                    return ("Problem in parenthesis order")
                open_parenthesis -= 1    
                if open_parenthesis < 0:
                    return ("Problem in parenthesis order")
            elif c == "!":
                if letter_next is False:
                    return ("'!' Symbol is in invalid position")
            elif letter_next is True and c not in self.valid_char:
                return "Missing letter"
            elif letter_next is False and c not in "+|^":
                return "Missing operator"
            else:
                letter_next = not letter_next   

        if letter_next is True:
            return ("Missing letter at end of rule part")
        if (open_parenthesis) != 0:
            return ("Parenthesis count doesnt match")

    def handle_bilateral_rule(self, rule, rules):
        rule_divided = rule.split("<=>")
        rule_one = rule_divided[0] + " => " + rule_divided[1]
        rule_two = rule_divided[1] + " => " + rule_divided[0]
        self.add_rule(rule_one, rules)
        self.add_rule(rule_two, rules)