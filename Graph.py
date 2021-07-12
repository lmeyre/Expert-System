from Fact import FactState


def graph_data(graph, rules, facts):
    for rule in rules:
        statement = add_nodes_edges(rule.statement, facts, graph)
        deduction = add_nodes_edges(rule.deduction, facts, graph)
        linker = Node("=>")
        valid = FactState.FALSE
        if (rule.valid_statement == True):
            valid = FactState.TRUE
        graph.add_node(linker, FactState=valid)
        graph.add_edge(statement, linker)
        graph.add_edge(linker, deduction)

def add_nodes_edges(rule_part, facts, graph):
    operator = None
    last_letter = ""
    neg = None
    last_neg = None
    for symbol in rule_part:
        if symbol in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            tmp = symbol# Here we DONT use a ref class (Node), because we want all "A" to be only 1, where for "!" we want multiple
            graph.add_node(tmp, FactState=facts[symbol].FactState)
            if (neg is not None):    
                st = FactState.TRUE
                if (facts[symbol] == FactState.TRUE):#Ca valide si c'est intermine/default/faux, donc tout sauf TRUE
                    st = FactState.FALSE
                graph.add_node(neg, FactState=st)#We gray those special symbol (nor true nor false)
                graph.add_edge(tmp, neg)#On lie la lettre vers le !
            if (operator is not None):#Si c'est pas la premiere lettre
                if last_neg is not None:
                    graph.add_edge(last_neg, operator)
                else:
                    graph.add_edge(last_letter, operator)
                if (neg is not None):
                    graph.add_edge(neg, operator)
                else:
                    graph.add_edge(tmp, operator)
            last_letter = tmp
            last_neg = neg
            neg = None
            # print(last_letter)
            # print(last_neg)
            # print(neg)
        elif symbol in "+|^":
            operator = Node(symbol)
            graph.add_node(operator, FactState=FactState.OUT)
        elif symbol == '!':
            neg = Node(symbol)
        else:
            continue
    if operator is not None:
        return operator
    elif last_neg is not None:
        return last_neg
    else:
        return last_letter

#Pour creer des references. Il n'y qu'un 'A', donc on utilise un char, mais il y a plusieurs '!' ou '+', on utilise donc une class pour la ref
class Node:
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return self.symbol
