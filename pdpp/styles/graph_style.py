class base_graph_style:
    NAME: str = ""


class default_graph_style(base_graph_style):
    NAME: str = "default"
    # Task Nodes:
    TASK_NODE_STYLE = "filled"
    TASK_NODE_SHAPE = "box3d"
    TASK_NODE_PENWIDTH = (1,)
    TASK_NODE_FONTCOLOR = "black"
    DISABLED_TASK_COLOR = "dimgrey"
    DISABLED_TASK_FONTCOLOR = TASK_NODE_FONTCOLOR
    DISABLED_TASK_STYLE = "dashed"
    START_TASK_COLOR = "#3E8DCF"
    END_TASK_COLOR = "#E95C3F"
    MID_TASK_COLOR = "#F2A93B"

    # File Nodes:
    FILE_NODE_STYLE = "filled"
    FILE_FILE_SHAPE = "note"
    FILE_DIR_SHAPE = "tab"
    FILE_NODE_COLOR = "#bbd698"
    FILE_NODE_PENWIDTH = 1

    # Source Nodes:
    SOURCE_STYLE = "filled"
    SOURCE_FONT_COLOR = "black"
    SOURCE_FILL_COLOR = "#9d6edb"
    SOURCE_SHAPE = "component"
    SOURCE_PENWIDTH = 1

    # Edges:
    EDGE_COLOR = "#828282"
    EDGE_PEN_WIDTH = 1.5


class greyscale_graph_style(base_graph_style):
    NAME: str = "greyscale"
    # Task Nodes:
    TASK_NODE_STYLE = "filled"
    TASK_NODE_SHAPE = "box3d"
    TASK_NODE_PENWIDTH = (1,)
    TASK_NODE_FONTCOLOR = "black"
    DISABLED_TASK_COLOR = "black"
    DISABLED_TASK_FONTCOLOR = "black"
    DISABLED_TASK_STYLE = "dashed"
    START_TASK_COLOR = "#c4c4c4"
    MID_TASK_COLOR = "#b0b0b0"
    END_TASK_COLOR = "#787878"

    # File Nodes:
    FILE_NODE_STYLE = "filled"
    FILE_FILE_SHAPE = "note"
    FILE_DIR_SHAPE = "tab"
    FILE_NODE_COLOR = "#f0f0f0"
    FILE_NODE_PENWIDTH = 1

    # Source Nodes:
    SOURCE_STYLE = "filled"
    SOURCE_FONT_COLOR = "black"
    SOURCE_FILL_COLOR = "white"
    SOURCE_SHAPE = "component"
    SOURCE_PENWIDTH = 1

    # Edges:
    EDGE_COLOR = "#828282"
    EDGE_PEN_WIDTH = 1.5
