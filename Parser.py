import re
import Rule as rule_obj
import Fact
class Parser:

    def __init__(self, args):
        self.valid_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.args = args
        self.facts = {}

    def parse(self, file_data):
        rules = []  
        queries = []
        for line in file_data:
            if self.args.show :
                print(line)
            isolate = line.split('#')
            if not isolate[0]:
                continue
            isolate[0] = isolate[0].strip()
            if not isolate[0]:
                continue
            if isolate[0][0] == '=':
                err = self.add_fact(isolate[0])
            elif isolate[0][0] == '?':
                err = self.add_query(queries, isolate[0])
            else:
                err = self.add_rule(isolate[0], rules)
            if err:
                return None, None, None, err
        return rules, queries, self.facts, None

    def add_fact(self, line):
        i = 1
        while (i < len(line)):
            if (line[i] not in self.valid_char):
                return "Error, wrong symbol in facts"
            self.facts[line[i]] = Fact.Fact(Fact.FactState.TRUE)
            i += 1

    def add_query(self, queries, line):
        i = 1
        while (i < len(line)):
            if (line[i] not in self.valid_char):
                return "Error, wrong symbol in queries"
            elif line[i] not in queries:
                queries.append(line[i])
                if line[i] not in self.facts:
                    self.facts[line[i]] = Fact.Fact(Fact.FactState.DEFAULT)
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
                return "Missing one side of a rule"
            new_rule = rule_obj.Rule()
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

            for l in new_rule.statement:
                if l in self.valid_char and l not in self.facts.keys():
                    self.facts[l] = Fact.Fact(Fact.FactState.DEFAULT)
            for l in new_rule.deduction:
                if l in self.valid_char and l not in self.facts.keys():
                    self.facts[l] = Fact.Fact(Fact.FactState.DEFAULT)
            rules.append(new_rule)

    def check_valid(self, rule):
        if rule.count("=>") != 1:
            return ("Error in format of rule linking")
        spliter = "=>"
        if ("<=>" in rule):
            spliter = "<=>"
        rule_divided = rule.split(spliter)
        err = self.check_valid_part(rule_divided[0])
        if err:
            return err
        if ("(" in rule_divided[1] or ")" in rule_divided[1]):
            return ("Parenthesis in deduction problem.")
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
                if letter_next is False or idx == len(rule_part) or rule_part[idx + 1] not in self.valid_char:
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