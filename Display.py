#Details -> Show not only Queries, but all. Also show those proven false, and those false by default
from Fact import FactState
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

#queries non used ? voir ca
def display_facts(args, queries, facts):
    if args.details == True:
        for key in facts:
            facts[key].print_state(key)
    else:
        for key in facts:
            if (facts[key].FactState == FactState.TRUE):
                facts[key].print_state(key)

def display_graph(graph, facts):
        colors = []
        for x in graph.nodes():
            if graph.nodes[x]:
                if graph.nodes[x]["FactState"] == FactState.TRUE:
                    colors.append("green")
                elif graph.nodes[x]["FactState"] == FactState.FALSE:
                    colors.append("red")
                elif graph.nodes[x]["FactState"] == FactState.DEFAULT:
                    colors.append('#FF0000')
                elif graph.nodes[x]["FactState"] == FactState.UNDETERMINED:
                    colors.append("grey")
                elif graph.nodes[x]["FactState"] == FactState.OUT:
                    colors.append("yellow")
                elif graph.nodes[x]["FactState"] == FactState.LINKER:
                    colors.append("purple")
                else:
                    print("CRITICALLL", x , " is " , graph.nodes[x]["FactState"])
        df = pd.DataFrame(index=graph.nodes(), columns=graph.nodes())
        for row, data in nx.shortest_path_length(graph):
            for col, dist in data.items():
                df.loc[row,col] = dist
        df = df.fillna(df.max().max())
        layout = nx.kamada_kawai_layout(graph, dist=df.to_dict())
        #nx.draw(graph, pos=layout,with_labels=True)
        nx.draw(graph, pos=layout ,with_labels=True, node_color=colors)
        plt.show()