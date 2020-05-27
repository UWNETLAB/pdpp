import networkx as nx
import os
from pdpp.pdpp_class import base_pdpp_class, export_class, step_class
from typing import List
from pdpp.task_creator import find_dependencies_from_others
from posixpath import join

if os.name == 'nt':
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz2.38/bin/'


def src_links(target_dir: str, source_file: str, G):

    """
    This is a docstring
    """
    
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

    """
    This is a docstring
    """

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
        except AttributeError:
            pass

def export_graph(G, output_name, files):

    """
    This is a docstring
    """

    toPdot = nx.drawing.nx_pydot.to_pydot
    N = toPdot(G)

    if files == "pdf" or files == "both":
        N.write(output_name + ".pdf", prog='dot', format='pdf')

    if files == "png" or files == "both":
        N.write(output_name + ".png", prog='dot', format='png')

def depgraph(files='both'):

    """
    This is a docstring
    """

    from pdpp.utils.directory_test import get_riggable_classes

    riggable_classes: List[base_pdpp_class] = get_riggable_classes()

    SOURCE = nx.DiGraph()
    SPARSE = nx.DiGraph()

    nodes = ["_import_"]
    edges = []
    disabled_nodes = []

    """
    This section adds _import_ to the loaded steps
    """ 

    for step_metadata in riggable_classes:
        if isinstance(step_metadata, export_class) == False:
            if len(step_metadata.import_files) > 0:
                step_metadata.dep_files["_import_"] = step_metadata.import_files

    """
    This section populates the graph with nodes
    """

    for step_metadata in riggable_classes:
        #pprint(step_metadata)
        if step_metadata.enabled:
            nodes.append(step_metadata.target_dir)
        else:
            disabled_nodes.append(step_metadata.target_dir)
        for linkage in step_metadata.dep_files:
            edges.append((linkage, step_metadata.target_dir))

    """
    This section creates the SPARSE graph, consisting only of edges indicating dependencies between steps
    """

    SPARSE.add_nodes_from(nodes, style='filled', shape='circle', fixedsize='shape', penwidth=0, categ="task")
    SPARSE.add_nodes_from(disabled_nodes, style='filled', shape='circle', fixedsize='shape', penwidth=0, categ="disabled")
    SPARSE.add_edges_from(edges, color='darkslategrey', weight=20)
    node_colour(SPARSE)  

    output_name = "dependencies_sparse"
    export_graph(SPARSE, output_name, files)

    """
    The SOURCE graph can be built out from the SPARSE graph; it simply adds source files and draws edges between them and their steps
    """

    SOURCE = SPARSE.copy()

    for step_metadata in riggable_classes:        
        if isinstance(step_metadata, step_class):
            for source_file in step_metadata.src_files:                
                src_links(step_metadata.target_dir, source_file, SOURCE)
        
    output_name = "dependencies_source"
    export_graph(SOURCE, output_name, files)

    """
    The FILE graph is built from scratch, using edges to represent the connections between steps and the files that they have as either 
    targets (implicitly defined as a file they output that another step relies upon) or dependencies (defined explicitly)
    """

    FILE = nx.create_empty_copy(SPARSE)    
    export_ = next((c for c in riggable_classes if isinstance(c, export_class)))

    for step_metadata in riggable_classes:

        # Add edges to target files
        if isinstance(step_metadata, export_class) == False:
            target_list = find_dependencies_from_others(step_metadata, export_, [riggable_classes])
            for target in target_list:
                target_name = join(step_metadata.target_dir, target)
                FILE.add_node(target_name, style="filled", shape='hexagon', fillcolor='violetred', fixedsize='shape', categ='file', penwidth=0)
                FILE.add_edge(step_metadata.target_dir, target_name, fillcolor='greenyellow')

        # Add edges from dependency files
        for dep_dir in step_metadata.dep_files:
            for dep_file in step_metadata.dep_files[dep_dir]:
                dep_name = join(dep_dir, dep_file)
                FILE.add_node(dep_name, style="filled", shape='hexagon', fillcolor='violetred', fixedsize='shape', categ='file', penwidth=0)
                FILE.add_edge(dep_name, step_metadata.target_dir, fillcolor='greenyellow')
                if dep_dir == "_import_":
                    FILE.add_edge("_import_", dep_name, fillcolor='greenyellow')
                    
    output_name = "dependencies_file"
    export_graph(FILE, output_name, files)
    
    ALL = FILE.copy()
    for step_metadata in riggable_classes:        
        if isinstance(step_metadata, step_class):
            for source_file in step_metadata.src_files:                
                src_links(step_metadata.target_dir, source_file, ALL)

    output_name = "dependencies_all"
    export_graph(ALL, output_name, files)

if __name__ == '__main__':
    depgraph()