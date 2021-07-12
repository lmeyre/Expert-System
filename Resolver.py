from Fact import FactState
import Rule
import sys
import networkx as nx
import Graph

class Resolver:

    def __init__(self, args):
        self.args = args
        self.rules = []
        self.graph = nx.DiGraph()
        self.modificationDone = True
        self.operators = "+|^"

    def resolve(self, rules, facts):
        self.rules = rules
        self.facts = facts
        err = None
        self.modificationDone = True
        while (self.modificationDone):
            #print("/////////// ONE LOOP")
            self.modificationDone = False # Remember to set it back to true later when modification are indeed done!
            err = self.computes_all_rules(False)
        #on gere les faux par default
        self.modificationDone = True
        while (self.modificationDone):
            #print("/////////// ONE LOOP")
            self.modificationDone = False # Remember to set it back to true later when modification are indeed done!
            err = self.computes_all_rules(True)
        if (self.args.graph == True):
            Graph.graph_data(self.graph, self.rules, self.facts)
        return err, self.facts, self.graph

    def computes_all_rules(self, handling_default):
        for rule in self.rules:
            #print("one rule = " , rule)
            if handling_default == False and self.check_default_in_rule(rule) == True:
                continue
            if self.analyze_statement(rule.statement, 0) == True:
                rule.valid_statement = True
                err = self.analyze_deduction(rule.deduction)
                if err:
                    return err

    def analyze_statement(self, statement, depth):
        if (self.args.debug_resolve and depth == 0):
            print("statement debug test, statement is :" + ''.join(statement))
        current_condition, i= self.find_initial_condition(statement)
        #Loop and compute the initial condition with other elements, step by step
        left_op = ''
        negative = False
        while (i < len(statement)):
            if statement[i] == '(':
                small_statement = []
                i += 1
                while statement[i] != ')':
                    small_statement.append(statement[i])
                    i += 1
                new_condition =  self.analyze_statement(small_statement, depth + 1)
                current_condition = self.combine_statements(left_op, current_condition, new_condition)
            elif statement[i] in self.operators:
                left_op = statement[i]
            elif statement[i] == '!':
                negative = True
            else:
                if statement[i] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":# TMP TO REMOVE ON FINISH
                    print("Problem here, unhandled case ? -> " + statement[i])
                new_condition = True if self.facts[statement[i]].FactState == FactState.TRUE else False
                if negative:
                    negative = False
                    new_condition = not new_condition
                current_condition = self.combine_statements(left_op, current_condition, new_condition)
            i += 1
        
        if self.args.debug_resolve and depth == 0:
            print("final condition = " , current_condition)
        return current_condition
    
    def find_initial_condition(self, statement):
        i = 0
        if (statement[i] == '('):
            i = 1
            initial = []
            while (statement[i] != ')'):
                initial.append(statement[i])
                i += 1
            current_condition = self.analyze_statement(initial)
            i += 1
        else:
            neg = False
            if statement[i] == '!':
                neg = True
                i += 1
            current_condition = True if self.facts[statement[i]].FactState == FactState.TRUE else False
            if neg:
                current_condition = not current_condition
            i += 1
        return current_condition, i

    def analyze_deduction(self, deduction):
        if (self.args.debug_resolve):
            print("Statement has been proven True. Analyzing deduction : " , deduction)
        idx = 0
        lenD = len(deduction)
        negating = False
        left_op = ""
        left_letter = ""
        left_letter_state = FactState.DEFAULT
        #penser si ya que 1 lettre
        while (idx < lenD):
            if (deduction[idx] in self.operators):
                left_op = deduction[idx]
            elif (deduction[idx] == '!'):
                negating = True
            else:
                if deduction[idx] not in  "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    print("problem in resolver, tmp to remove") # to remove
                curr = deduction[idx]       
                #temporary state for current, before sometime changing it again below    
                if negating:
                    curr_state = FactState.FALSE
                    negating = False
                else:    
                    curr_state = FactState.TRUE
                if idx > 1: # pour la toute premiere lettre, on va juste la premiere estimation, et pas ce qui suit
                    # cas pas a gerer pour la premiere lettre, vu que ya rien a s gauche
                    if left_op == '+':
                        self.apply_state(left_letter, left_letter_state)
                    elif left_op == '|':
                        self.apply_state(left_letter, FactState.UNDETERMINED)
                        curr_state = FactState.UNDETERMINED 
                    elif left_op == '^':
                        #si un est vrai et l'autre faux, osef
                        if ((self.facts[left_letter].FactState == FactState.TRUE and self.facts[curr].FactState == FactState.FALSE) or (self.facts[left_letter].FactState == FactState.FALSE and self.facts[curr].FactState == FactState.TRUE)):
                            print("good xor gate already in place on : " + curr)
                            curr_state = self.facts[curr].FactState
                        #si les 2 sont default/undetermined
                        elif (self.facts[left_letter].FactState == FactState.DEFAULT or self.facts[left_letter].FactState == FactState.UNDETERMINED) and (self.facts[curr].FactState == FactState.DEFAULT or self.facts[curr].FactState == FactState.UNDETERMINED):    
                            self.apply_state(left_letter, FactState.UNDETERMINED)
                            curr_state = FactState.UNDETERMINED 
                        #si les 2 sont egaux, et true ou false, contradiction
                        elif (self.facts[left_letter].FactState == self.facts[curr].FactState) and (self.facts[left_letter].FactState == FactState.TRUE or self.facts[left_letter].FactState == FactState.FALSE):    #equal if undetermined or default isnt contradiction
                            return "Contradiction in deduction at XOR gate"
                        elif self.facts[left_letter].FactState == FactState.DEFAULT or self.facts[left_letter].FactState == FactState.UNDETERMINED: #si 1 est undetermined/default
                            state = FactState.TRUE if (self.facts[curr].FactState == FactState.FALSE) else FactState.FALSE
                            self.apply_state(left_letter, state)
                            curr_state = self.facts[curr].FactState
                        elif self.facts[curr].FactState == FactState.DEFAULT or self.facts[curr].FactState == FactState.UNDETERMINED: #si 2 est undetermined/default
                            state = FactState.TRUE if (self.facts[left_letter].FactState == FactState.FALSE) else FactState.FALSE
                            self.apply_state(left_letter, left_letter_state)
                            curr_state = state
                        else:
                            print("wtf2XXXXXXXXXXXXXXXXXXXXXXXX  ", deduction[idx], " and left op - ", left_op)
                            print(self.facts[left_letter].FactState)
                            print(self.facts[curr].FactState)
                    else:
                        print("wtfXXXXXXXXXXXXXXXXXXXXXXX")
                left_letter = curr
                left_letter_state = curr_state
                #ne pas set negating, que apres l'avoir use on le remet a true
            idx += 1
        
        # derniere lettre
        #rien a comparer a sa droite
        #print("ending, state of letter ", left_letter, "is " , left_letter_state)
        self.apply_state(left_letter, left_letter_state)

    def check_default_in_rule(self, rule):
        for letter in rule.statement:
            if letter in self.facts.keys() and self.facts[letter].FactState == FactState.DEFAULT:
                return True
        return False

    def apply_state(self, letter, state):
        print("entering : ", letter, " and state ", state)
        if (self.facts[letter].FactState != state):
            if (state == FactState.UNDETERMINED and self.facts[letter].FactState == FactState.TRUE) or (state == FactState.UNDETERMINED and self.facts[letter].FactState == FactState.FALSE):
                return  # On applique pas undetermined sur un truc prouve vrai ou faux.
            elif (self.facts[letter].FactState == FactState.TRUE and state == FactState.FALSE) or (self.facts[letter].FactState == FactState.FALSE and state == FactState.TRUE):
                print("Contradiction in rules -> " + letter + " has been proven True AND False")
                sys.exit(1)
            self.facts[letter].FactState = state
            self.modificationDone = True
            print("APPLYING STATE => ", state, " to ", letter)

    def combine_statements(self, operand, part1, part2):
        if operand == '+':
            return (part1 and part2)
        elif operand == '|':
            return (part1 or part2)
        elif operand == '^':
            return (part1 and not part2) or (not part1 and part2)


