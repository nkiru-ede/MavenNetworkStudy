import pandas as pd
import os
import networkx as nx
import json

data_folder = './data'
cleaned_data_file = os.path.join(data_folder, 'cleaned_data.csv')
new_df_cleaned = pd.read_csv(cleaned_data_file)

def df_to_graph(df):
    graph = nx.DiGraph()
    for _, row in df.iterrows():
        graph.add_edge(row['source'], row['target'])
    return graph

dag = df_to_graph(new_df_cleaned)

def collapse_sccs(graph):
    sccs = list(nx.strongly_connected_components(graph))
    scc_map = {}
    condensed_graph = nx.DiGraph()

    for scc in sccs:
        if len(scc) > 1:
            super_node = frozenset(scc)
            for node in scc:
                scc_map[node] = super_node
            condensed_graph.add_node(super_node)
        else:
            node = next(iter(scc))
            scc_map[node] = node
            condensed_graph.add_node(node)

    for u, v in graph.edges():
        u_super = scc_map[u]
        v_super = scc_map[v]
        if u_super != v_super:
            condensed_graph.add_edge(u_super, v_super)

    return condensed_graph, scc_map

condensed_dag, scc_map = collapse_sccs(dag)

print("Number of SCCs:", len(scc_map))
print("Condensed graph nodes:", len(condensed_dag.nodes))
print("Condensed graph edges:", len(condensed_dag.edges))

# Save the condensed graph
condensed_dag_data = nx.node_link_data(condensed_dag)
with open(os.path.join(data_folder, 'condensed_dag.json'), 'w') as f:
    json.dump(condensed_dag_data, f)
