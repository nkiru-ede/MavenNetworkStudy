import pandas as pd
import os
import networkx as nx
from collections import defaultdict, deque

data_folder = './data'
links_file = os.path.join(data_folder, 'links_all.csv')


new_df = pd.read_csv(links_file, delimiter=',')

new_df.columns = new_df.columns.str.replace('"', '').str.strip()

dag = nx.DiGraph()
cycle_error_count = 0
loop_error_count = 0
valid_rows = []

for index, row in new_df.iterrows():
    source = row['source']
    target = row['target']

    if source == target:
        loop_error_count += 1
        continue

    dag.add_node(source)
    dag.add_node(target)

    if nx.has_path(dag, target, source):
        cycle_error_count += 1
        continue

    dag.add_edge(source, target)
    valid_rows.append(index)

new_df_cleaned = new_df.loc[valid_rows].reset_index(drop=True)

vertex_count = len(dag.nodes)
edge_count = len(dag.edges)

print("Cycle errors adding edges:", cycle_error_count)
print("Loop errors adding edges:", loop_error_count)
print("Vertex count:", vertex_count)
print("Edge count:", edge_count)
print(new_df_cleaned.head())
print("Length of cleaned DataFrame:", len(new_df_cleaned))

# Convert cleaned DataFrame to graph
def df_to_graph(df):
    graph = defaultdict(list)
    for _, row in df.iterrows():
        graph[row['source']].append(row['target'])
    return graph

def topological_sort(graph, all_nodes):
    in_degree = {u: 0 for u in all_nodes}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1
    
    queue = deque([u for u in all_nodes if in_degree[u] == 0])
    topo_order = []
    
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    return topo_order

def compute_transitive_dependencies(graph, topo_order, depth_limit=None):
    transitive_deps = defaultdict(list)
    for u in reversed(topo_order):
        for v in graph[u]:
            if depth_limit is not None and len(transitive_deps[u]) >= depth_limit:
                continue
            transitive_deps[u].append(v)
            if depth_limit is None:
                transitive_deps[u].extend(transitive_deps[v])
            else:
                transitive_deps[u].extend(transitive_deps[v][:depth_limit - len(transitive_deps[u])])
    return transitive_deps

def identify_highly_connected_nodes(graph, threshold=10):
    highly_connected = {node: len(edges) for node, edges in graph.items() if len(edges) > threshold}
    return highly_connected

# Ensure all rows in the output file conform to the expected format
def save_transitive_dependencies(transitive_deps, output_file_path):
    with open(output_file_path, 'w') as f:
        f.write('source,target\n')
        for u in transitive_deps:
            for v in transitive_deps[u]:
                f.write(f'{u},{v}\n')

def main():
    output_file_path = './data/transitive_dependencies.csv'
    depth_limit = 10  # Example depth limit, adjust as needed

    #print(f"Cleaned DataFrame loaded with {len(new_df_cleaned)} entries.")
    
    graph = df_to_graph(new_df_cleaned)
    all_nodes = set(new_df_cleaned['source']).union(set(new_df_cleaned['target']))
    
    #print(f"Graph created with {len(all_nodes)} nodes.")
    
    topo_order = topological_sort(graph, all_nodes)
    if not topo_order:
        print("Failed to perform topological sorting.")
        return
    
    #print("Topological sorting completed.")
    
    transitive_deps = compute_transitive_dependencies(graph, topo_order, depth_limit)
    
    print("Transitive dependencies computed.")
    
    save_transitive_dependencies(transitive_deps, output_file_path)
    
    print(f"Transitive dependencies saved to {output_file_path}.")
    
    highly_connected_nodes = identify_highly_connected_nodes(graph)
    print(f"Highly connected nodes (threshold > 10): {highly_connected_nodes}")

if __name__ == '__main__':
    main()
