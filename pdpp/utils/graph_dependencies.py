import networkx as nx
import os
from pdpp.tasks.base_task import BaseTask
from typing import List
from pdpp.automation.task_creator import find_dependencies_from_others
from posixpath import join
from pdpp.styles.graph_style import default_graph_style
import pydot

if os.name == 'nt':
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz2.38/bin/'


def src_links(target_dir: str, source_file: str, G, gs):

    """
    This is a docstring
    """
    
    G.add_edge(source_file, target_dir, dir='none', color=gs.EDGE_COLOR, penwidth=gs.EDGE_PEN_WIDTH)
    #G.add_edge(target_dir, source_file, dir='none', color=gs.EDGE_COLOR, penwidth=2)
    G.nodes[source_file]['style'] = gs.SOURCE_STYLE
    G.nodes[source_file]['fontcolor'] = gs.SOURCE_FONT_COLOR 
    G.nodes[source_file]['fillcolor'] = gs.SOURCE_FILL_COLOR
    G.nodes[source_file]['shape'] = gs.SOURCE_SHAPE
    G.nodes[source_file]['penwidth'] = gs.SOURCE_PENWIDTH
    G.nodes[source_file]['categ'] = 'source'


def node_colour(G, gs):

    """
    This is a docstring
    """ 

    for node in G:
        if G.nodes[node]['categ'] == 'disabled':
            G.nodes[node]['fillcolor'] = gs.DISABLED_TASK_COLOR
            G.nodes[node]['fontcolor'] = gs.DISABLED_TASK_FONTCOLOR
            G.nodes[node]['style'] = gs.DISABLED_TASK_STYLE
        elif G.in_degree(node) == 0:
            G.nodes[node]['fillcolor'] = gs.START_TASK_COLOR
        elif G.out_degree(node) == 0:
            G.nodes[node]['fillcolor'] = gs.END_TASK_COLOR
        else:
            G.nodes[node]['fillcolor'] = gs.MID_TASK_COLOR


def export_graph(G, output_name, files):

    """
    This is a docstring
    """

    # This loop checks for and removes any isolated nodes

    remlist = [node for node in G if G.degree[node] == 0]

    for node in remlist:
        G.remove_node(node)

    toPdot = nx.drawing.nx_pydot.to_pydot # type:ignore
    N:pydot.Dot = toPdot(G)

    N.obj_dict['attributes']['concentrate'] = 'true' # Combines edges
    N.obj_dict['attributes']['rankdir'] = 'LR' # Runs graph left-to-right
    N.obj_dict['attributes']['dpi'] = 300

    # Add all source nodes to subgraphs with their tasks so that they are 
    # displayed on the same rank:

    for edge in N.get_edge_list():
        if N.get_node(edge.get_source())[0].get('categ') == "source":
            S = pydot.Subgraph(rank = 'same')
            S.add_node(N.get_node(edge.get_source())[0])
            S.add_node(N.get_node(edge.get_destination())[0])
            N.add_subgraph(S)

    ext = "." + files

    N.write(output_name + ext, prog='dot', format=files)



def depgraph(files='png', gs=default_graph_style):

    """
    This is a docstring
    """

    from pdpp.utils.directory_test import get_pdpp_tasks

    all_tasks: List[BaseTask] = get_pdpp_tasks()

    SOURCE = nx.DiGraph()
    SPARSE = nx.DiGraph()

    nodes = []
    edges = []
    disabled_nodes = []

    """
    This section populates the graph with nodes and edges from dependency tasks to dependent tasks
    """

    for task in all_tasks:
        if task.enabled:
            nodes.append(task.target_dir)
        else:
            disabled_nodes.append(task.target_dir)
        for linkage in task.dep_files:
            edges.append((linkage, task.target_dir))

    """
    This section creates the SPARSE graph, consisting only of edges indicating dependencies between tasks
    """

    SPARSE.add_nodes_from(
        nodes, 
        style=gs.TASK_NODE_STYLE, 
        shape=gs.TASK_NODE_SHAPE, 
        penwidth=gs.TASK_NODE_PENWIDTH, 
        categ="task"
        )
    SPARSE.add_nodes_from(
        disabled_nodes, 
        style=gs.TASK_NODE_STYLE, 
        shape=gs.TASK_NODE_SHAPE, 
        penwidth=gs.TASK_NODE_PENWIDTH, 
        categ="disabled"
        )
    SPARSE.add_edges_from(
        edges, 
        color=gs.EDGE_COLOR, 
        penwidth=gs.EDGE_PEN_WIDTH
        )        
    node_colour(SPARSE, gs)  

    output_name = "dependencies_sparse"
    export_graph(SPARSE, output_name, files)

    """
    The SOURCE graph can be built out from the SPARSE graph; it simply adds source files and draws edges between them and their tasks
    """

    SOURCE = SPARSE.copy()

    for task in all_tasks:
        for source_file in task.src_files:                
            src_links(task.target_dir, source_file, SOURCE, gs)

            
    output_name = "dependencies_source"
    export_graph(SOURCE, output_name, files)

    """
    The FILE graph is built from scratch, using edges to represent the connections between tasks and the files that they have as either 
    targets (implicitly defined as a file they output that another task relies upon) or dependencies (defined explicitly)
    """

    FILE = nx.create_empty_copy(SPARSE)    

    for task in all_tasks:
        
        # Add edges from dependency files
        for dep_dataclass in task.dep_files.values():

            # ADD FILES
            for dep_file in dep_dataclass.file_list:
                dep_name = join(dep_dataclass.task_name, dep_dataclass.task_out, dep_file)
                FILE.add_node(
                    dep_name, 
                    style=gs.FILE_NODE_STYLE, 
                    shape=gs.FILE_FILE_SHAPE, 
                    fillcolor=gs.FILE_NODE_COLOR, 
                    categ='file', 
                    label=dep_file, 
                    penwidth=gs.FILE_NODE_PENWIDTH
                    )
                FILE.add_edge(
                    dep_name, 
                    task.target_dir, 
                    color=gs.EDGE_COLOR, 
                    penwidth=gs.EDGE_PEN_WIDTH
                    )
            
            # ADD DIRECTORIES
            for dep_dir in dep_dataclass.dir_list:
                dep_name = join(dep_dataclass.task_name, dep_dataclass.task_out, dep_dir)
                dep_label = dep_dir + "/"
                FILE.add_node(
                    dep_name, 
                    style=gs.FILE_NODE_STYLE, 
                    shape=gs.FILE_DIR_SHAPE, 
                    fillcolor=gs.FILE_NODE_COLOR, 
                    categ='file', 
                    label=dep_label, 
                    penwidth=gs.FILE_NODE_PENWIDTH
                    )
                FILE.add_edge(
                    dep_name, 
                    task.target_dir, 
                    color=gs.EDGE_COLOR, 
                    penwidth=gs.EDGE_PEN_WIDTH
                    )
        
        # Add edges to targets (as defined by others)
        target_list = find_dependencies_from_others(task, all_tasks)

        for full_target_path in target_list:
            target_name = full_target_path.split('/')[-1]
            FILE.add_edge(
                task.target_dir, 
                full_target_path, 
                color=gs.EDGE_COLOR, 
                penwidth=gs.EDGE_PEN_WIDTH)
                    

    output_name = "dependencies_file"
    export_graph(FILE, output_name, files)
    
    ALL = FILE.copy()
    for task in all_tasks:        
        for source_file in task.src_files:                
            src_links(task.target_dir, source_file, ALL, gs)

    output_name = "dependencies_all"
    export_graph(ALL, output_name, files)

if __name__ == '__main__':
    depgraph()