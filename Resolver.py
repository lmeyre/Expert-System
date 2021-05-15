import rule
#Il faudra loop dans les deduction a chaque fois qu'un progres a lieux, en effet, si on :
#B => A
#C => B

#=C
#Dans ce cas la, on ne saura que A est vrai que lors du deuxieme passage

#Les lettres indeterminees sont considerees comme fausse par default
#Mais il y a une difference si une fausse par default est prouvee vrai
#Et si une qui a ete prouvee fausse, est ensuite prouvee vrai, la il y aura contradiction et probleme
#Il faut donc un etat special pour les faux, qui le sont par default

#Biconditionale rule <=> , est ce que c'est pas juste egal a deux ligne :
# A + B <=> C + D  ->   A + B => C + D   &&   C + D => A + B
# dans ce cas nico devrait peut etre creer 2 ligne dans l'array

#exemple dico in py
#thisdict =	{
#  "brand": "Ford",
#  "model": "Mustang",
#  "year": 1964
#}
#ternary:
#state = "nice" if is_nice else "not nice"

#legend :
# =ABC -> FACTS
# A + B => C     -> RULE
# A + B    -> RULE STATEMENT
# => C     -> RULE DEDUCTION


class Resolver:

    def __init__(self):
        self.rules = []#2d array of rules
        #self.rules = None  # 2d string array   1st - statement   2nd - deduction
                            # ou 3d ? 1d - ligne   2d - statement/deduction  3d/ separated statement letters/operators
        self.true_facts = {} # dictionnary letter / bool
        self.false_facts = {} # dictionnary letter / bool
        self.modificationDone = True# pas de do while en py
        self.operators = "+|^!"

    def resolve(self, rules, facts):
        self.rules = rules
        self.true_facts = facts
        while (modificationDone):
            modificationDone = False # Remember to set it back to true later when modification are indeed done!
            self.computes_all_rules()

    #Voir si on remove les lines qu'on a deja entierement analyze sans inconnues, genre A is true, et la ligne A => B.
    def computes_all_rules(self):
        #on deduit si le rule statement est vrai
        #si oui on met les valeur de rule deduction a vrai ?
        #voir si on met les rule deduction a faux si c'est pas vrai
        for rule in rules:
            # rule_statement = line[0]
            # rule_deduction = line[1]
            if self.analyze_statement(rule.statement) == True:
                # pour l'instant on gere pas les trucs genre A => B | C, voir comment on le gere dans la logique avant le code
                if current_condition == True:
                    for line in rule_deduction:
                        if line not in operators and line not in self.true_facts:
                            self.true_facts[line] = True
            #else set deduction to false, or ignore ? -> ignore

    def analyze_statement(self, statement):

        #new rework
        print("statement debug test, statement is :" + statement)
        i = 0
        #Get initial condition
        if (statement[i] == '('):
            i = 1
            initial = []
            while (statement[i] != ')'):
                initial.append(statement[x])
                i += 1
            current_condition = self.analyze_statement(initial)
        else:
            current_condition = statement[i] in true_facts    
            i += 1

        print(i + " is index and condition = " + current_condition)
        #Loop and compute the condition with other elements
        
        last_operator = ''
        while (i < len(statement)):
            if statement[i] == '(':
                small_statement = []
                i += 1
                while statement[i] != ')':
                    small_statement.append(statement[i])
                new_condition =  self.analyze_statement(small_statement)
                current_condition = self.combine_statements(last_operator, current_condition, new_condition)
            elif statement[i] in self.operators:
                last_operator = statement[i]
            else:
                if statement[i] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    print("Problem here, unhandled case ? -> " + statement[i])
                new_condition = statement[i] in true_facts
                current_condition = self.combine_statements(last_operator, current_condition, new_condition)
            i += 1

        #Old :
        # current_condition = rule_statement[0] in true_facts
        
        # i = 2
        # while (i < len(rule_statement)):
        #     operand = rule_statement[i - 1]
        #     part2 = rule_statement[i] in true_facts
        #     current_condition = self.combine_statements(operand, current_condition, part2)
        #     i += 2
        
        return current_condition

    def combine_statements(self, operand, part1, part2):
        if operand == '+':
            return (part1 and part2)
        elif operand == '|':
            return (part1 or part2)
        elif operand == '^':
            return (part1 and not part2) or (not part1 and part2)

