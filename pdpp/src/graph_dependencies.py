import networkx as nx
import os
import sys
from pdpp.src.yaml_handlers.import_yaml import import_yaml
from pprint import pprint

if os.name == 'nt':
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz2.38/bin/'


def src_links(target_dir, source_file, G):
    G.add_edge(source_file, target_dir, color='darkslategrey', dir='none', weight=20)
    G.nodes[source_file]['style'] = 'filled'
    if '.py' in source_file:
        G.nodes[source_file]['fillcolor'] = 'turquoise4'
    else:
        G.nodes[source_file]['fillcolor'] = 'violetred'
    G.nodes[source_file]['shape'] = 'square'
    G.nodes[source_file]['fixedsize'] = 'shape'
    G.nodes[source_file]['penwidth'] = 0

def node_colour(G):
    for node in G:
        try:
            if G.in_degree(node) == 0 and G.nodes[node]['categ'] == 'task':
                G.nodes[node]['fillcolor'] = 'springgreen'
            elif G.out_degree(node) == 0 and G.nodes[node]['categ'] == 'task':
                G.nodes[node]['fillcolor'] = 'firebrick1'
            elif G.nodes[node]['categ'] == 'task':
                G.node[node]['fillcolor'] = 'cadetblue2'
            elif G.nodes[node]['categ'] == 'disabled':
                G.node[node]['fillcolor'] = 'dimgrey'
        except KeyError:
            pass



def export_graph(G, output_name, files):

    toPdot = nx.drawing.nx_pydot.to_pydot
    N = toPdot(G)

    if files == "pdf" or files == "both":
        N.write(output_name + ".pdf", prog='dot', format='pdf')

    if files == "png" or files == "both":
        N.write(output_name + ".png", prog='dot', format='png')


def depgraph(files='both'):
    from pdpp.src.utils.proj_folder_test import proj_folder_test

    subdirs = [f.path.replace('./', '').replace('.\\', '') for f in os.scandir() if proj_folder_test(f)]

    yaml_steps = []

    for directory in subdirs:
        yaml_dict, _ = import_yaml(directory, return_empty=False)
        if yaml_dict:
            yaml_steps.append(yaml_dict)

    SOURCE = nx.DiGraph()
    SPARSE = nx.DiGraph()

    nodes = []
    edges = []
    disabled_nodes = []

    for step in yaml_steps:
        if step:
            pprint(step)
            if step['enabled'] == True:
                nodes.append(step['target_dir'])
            else:
                disabled_nodes.append(step['target_dir'])
            for linkage in step['dep_dirs']:
                edges.append((linkage, step['target_dir']))


    SPARSE.add_nodes_from(nodes, style='filled', shape='circle', fixedsize='shape', penwidth=0, categ="task")
    SPARSE.add_nodes_from(disabled_nodes, style='filled', shape='circle', fixedsize='shape', penwidth=0, categ="disabled")
    SPARSE.add_edges_from(edges, color='darkslategrey', weight=20)
    node_colour(SPARSE)  
    output_name = "dependencies_sparse"
    export_graph(SPARSE, output_name, files)

    SOURCE.add_nodes_from(nodes, style='filled', shape='circle', fixedsize='shape', penwidth=0, categ="task")
    SPARSE.add_nodes_from(disabled_nodes, style='filled', shape='circle', fixedsize='shape', penwidth=0, categ="disabled")
    SOURCE.add_edges_from(edges, color='darkslategrey', weight=20)
    node_colour(SOURCE)
    for step in yaml_steps:  
        for source_file in step['src_files']:
            src_links(step['target_dir'], source_file, SOURCE)
    output_name = "dependencies_source"
    export_graph(SOURCE, output_name, files)
    

    FILE = nx.create_empty_copy(SPARSE)
    # Add edges to target files
    for step in yaml_steps:
        for target in step['target_files']:
            FILE.add_node(target.split('/')[-1], style="filled", shape='hexagon', fillcolor='darkgoldenrod3', fixedsize='shape', categ='file', penwidth=0)
            FILE.add_edge(step['target_dir'], target.split('/')[-1],  fillcolor='greenyellow')
    # Add edges from dependency files
        for dep_dir in step['dep_dirs']:
            for dep_file in step['dep_files'][dep_dir]:
                FILE.add_node(dep_file.split('/')[-1], style="filled", shape='hexagon', fillcolor='darkgoldenrod3', fixedsize='shape', categ='file', penwidth=0)
                FILE.add_edge(dep_file.split('/')[-1], step['target_dir'])
        for self_dep in step['self_deps']:
            FILE.add_node(self_dep.split('/')[-1], style="filled", shape='hexagon', fillcolor='coral', fixedsize='shape', categ='self_dep_file', penwidth=0)
            FILE.add_edge(self_dep.split('/')[-1], step['target_dir'])
    output_name = "dependencies_file"
    export_graph(FILE, output_name, files)
    
    ALL = FILE.copy()
    for step in yaml_steps:  
        for source_file in step['src_files']:
            src_links(step['target_dir'], source_file, ALL)

    output_name = "dependencies_all"
    export_graph(ALL, output_name, files)


if __name__ == '__main__':
    depgraph()