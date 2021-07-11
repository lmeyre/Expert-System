#Details -> Show not only Queries, but all. Also show those proven false, and those false by default
from Fact import FactState


def display_facts(args, queries, facts):
    if args.details == True:
        for key in facts:
            facts[key].print_state(key)
    else:
        for key in facts:
            if (facts[key].FactState == FactState.TRUE):
                facts[key].print_state(key)