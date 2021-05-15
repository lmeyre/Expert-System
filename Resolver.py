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

    def __init__(self, args):
        self.args = args
        self.rules = []#2d array of rules
        #self.rules = None  # 2d string array   1st - statement   2nd - deduction
                            # ou 3d ? 1d - ligne   2d - statement/deduction  3d/ separated statement letters/operators
        self.true_facts = {} # dictionnary letter / bool
        self.false_facts = {} # dictionnary letter / bool
        #Les elements inconnus sont consideres comme faux jusqu'a preuve du contraire mais ne sont pas des false_facts (prouve faux)
        self.modificationDone = True# pas de do while en py
        self.operators = "+|^!"

    def resolve(self, rules, facts):
        self.rules = rules
        for fact in facts:
            self.true_facts[fact] = True
        modificationDone = True
        while (modificationDone):
            modificationDone = False # Remember to set it back to true later when modification are indeed done!
            self.computes_all_rules()

    #Voir si on remove les lines qu'on a deja entierement analyze sans inconnues, genre A is true, et la ligne A => B.
    def computes_all_rules(self):
        for rule in self.rules:
            if self.analyze_statement(rule.statement) == True:
                for part in rule.deduction:
                    if part not in self.operators and part not in "()":
                        #to update to handle more
                        # pour l'instant on gere pas les trucs genre A => B | C, voir comment on le gere dans la logique avant le code
                        if part not in self.true_facts:
                            modificationDone = True
                            self.true_facts[part] = True
                        #Ici en ajoutant les trucs a true / false facts, on verifie si certains sont inconnus,
                        #si aucun le sont, on peut virer cette ligne de la loop de rules
            #else set deduction to false, or ignore ? -> ignore

    def analyze_statement(self, statement):
        #new rework
        if (self.args.debug_resolve):
            print("statement debug test, statement is :" + ''.join(statement))
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
            current_condition = statement[i] in self.true_facts    
            i += 1

        if (self.args.debug_resolve):
            print(i , " is index and INITIAL condition = " , current_condition)
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
                new_condition = statement[i] in self.true_facts
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
        
        if self.args.debug_resolve:
            print("final condition = " , current_condition)
        return current_condition

    def combine_statements(self, operand, part1, part2):
        if operand == '+':
            return (part1 and part2)
        elif operand == '|':
            return (part1 or part2)
        elif operand == '^':
            return (part1 and not part2) or (not part1 and part2)

