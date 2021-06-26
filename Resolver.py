from Fact import FactState
import Rule
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
        #self.true_facts = {} # dictionnary letter / bool
        #self.false_facts = {} # dictionnary letter / bool
        #Les elements inconnus sont consideres comme faux jusqu'a preuve du contraire mais ne sont pas des false_facts (prouve faux)
        self.modificationDone = True# pas de do while en py  # On garde ca pour l'instant mais voir note on va ptet plus loop
        self.operators = "+|^"

    #facts = Dictionary Letter / Fact 
    def resolve(self, rules, facts):
        self.rules = rules
        self.facts = facts
        err = None
        # for fact in facts:
        #     self.true_facts[fact] = True
        modificationDone = True
        while (modificationDone):
            modificationDone = False # Remember to set it back to true later when modification are indeed done!
            err = self.computes_all_rules()
            
        return err, self.facts

    #Voir si on remove les lines qu'on a deja entierement analyze sans inconnues, genre A is true, et la ligne A => B.
    def computes_all_rules(self):
        for rule in self.rules:
            if self.analyze_statement(rule.statement) == True:
                err =self.analyze_deduction(rule.deduction)
                if err:
                    return err

    def analyze_statement(self, statement):
        if (self.args.debug_resolve):
            print("statement debug test, statement is :" + ''.join(statement))
        current_condition, i = self.find_initial_condition(statement)
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
                new_condition =  self.analyze_statement(small_statement)
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
        
        if self.args.debug_resolve:
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

        if (self.args.debug_resolve):
            print(i , " is index and INITIAL condition = " , current_condition)
        return current_condition, i

    def analyze_deduction(self, deduction):
        #A voir :
        #si ya un '|'  -> les 2 cotes sont indetermines
        #si ya un '+' -> les 2 cote sont vrai (et faux pour les !)
        #si ya un '^' -> on check si on connait un des deux, si oui l'autre est l'inverse, si aucun des deux est connu, ils sont inconnus, si les 2 sont connus on verifie que no contradiction
        idx = 0
        lenD = len(deduction)
        negating = False
        #negating_right = False
        #on part de la gauche, et on traite a chaque fois notre lettre + celle plus a gauche.
        #on donne un etat temporaire a la lettre sur laquelle on est(2), (pour gerer XOR), on traite celle a gauche (1), avant de passer sur la (3), et d'utiliser l'etat temporaire pour traiter la (2)
        #en fait on doit toujours faire la lettre current + celle de gauche, car ca permet de recup les ! et de pas avoir a check les position apres, si elles sont pas out of bound etc
        #en resume on traite chaque lettre en 2 etape, d'abord son premier etat vis a vis du signe a sa gauche, puis en arrivant a la lettre d'apres on confirme son etat vis a vis du signe a sa droite
        left_op = ""
        right_op = ""#pas sur d'en avoir besoin -> on veut pas vraiment analyzer une lettre en checkant les 2 op des 2 cote car c'est relou si ya des !
        left_letter = ""
        left_letter_state = self.facts[deduction[idx]].FactState # temporary state in relation to 2 letters (1 and 2), before examining the 2nd one with the 3rd need to remember 2nd state relation to 1 for XOR
        #penser si ya que 1 lettre
        while (idx < lenD):
            if (deduction[idx] in self.operators):
                left_op = deduction[idx]
            elif (deduction[idx] == '!'):
                negating = True
            else:
                curr = deduction[idx]               
                curr_state = FactState.TRUE
                if negating:
                    curr_state = FactState.FALSE
                    negating = False
                if idx > 1: # pour la toute premiere lettre, on va juste la premiere estimation, et pas ce qui suit
                    # cas pas a gerer pour la premiere lettre, vu que ya rien a s gauche
                    if left_op == '+':
                        self.apply_state(left_letter, left_letter_state)
                    elif left_op == '|':
                        self.apply_state(left_letter, FactState.UNDETERMINED)
                        curr_state = FactState.UNDETERMINED 
                    elif left_op == '^':
                        if (self.facts[left_letter].FactState == FactState.UNDETERMINED and self.facts[curr].factState == FactState.UNDETERMINED):    
                            self.apply_state(left_letter, FactState.UNDETERMINED)
                            curr_state = FactState.UNDETERMINED 
                        elif (self.facts[left_letter].FactState == self.facts[curr].FactState):    
                            return "Contradiction in deduction at XOR gate"
                        elif self.facts[left_letter].FactState == FactState.UNDETERMINED: #si 1 est undetermined
                            state = FactState.TRUE if (self.facts[curr].FactState == FactState.FALSE) else FactState.FALSE
                            self.apply_state(left_letter, state)
                            curr_state = self.facts[curr].FactState
                        elif self.facts[curr].FactState == FactState.UNDETERMINED: #si 2 est undetermined
                            state = FactState.TRUE if (self.facts[left_letter].FactState == FactState.FALSE) else FactState.FALSE
                            self.apply_state(left_letter, left_letter_state)
                            curr_state = state
                        else:
                            print("wtf2")
                    else:
                        print("wtf")
                left_letter = curr
                left_letter_state = curr_state
                #ne pas set negating, que apres l'avoir use on le remet a true
                idx += 1
        
        # derniere lettre
        #rien a comparer a sa droite
        self.apply_state(left_letter, left_letter_state)

    def apply_state(self, letter, state):
        print("entering ", letter, " and state ", state)
        if (self.facts[letter] != state):
            self.facts[letter] = state
            self.modificationDone = True
            print("APPLYING STATE => ", state)

    def combine_statements(self, operand, part1, part2):
        if operand == '+':
            return (part1 and part2)
        elif operand == '|':
            return (part1 or part2)
        elif operand == '^':
            return (part1 and not part2) or (not part1 and part2)

