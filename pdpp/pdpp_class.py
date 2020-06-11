from typing import List, Dict
from posixpath import join 
from os import makedirs
from posixpath import join, exists
import yaml

class base_pdpp_class():
    """
    This is a docstring.
    """
    def __init__(
        self
        ):

        self.target_dir = "PLACEHOLDER"
        self.language = "PLACEHOLDER"
        self.enabled = True
        self.dep_files: Dict[str, List[str]]  = {}
        self.import_files = []
        self.src_files = []

    
    filename = "PLACEHOLDER"
    in_dir = "PLACEHOLDER"
    out_dir = "PLACEHOLDER"
    has_source = False

    def initialize_step(self):
        pass


def make_export(new_step_metadata: base_pdpp_class, target_dir:str): 

    '''
    Saves a pdpp-compliant step_class in the directory indicated in its
    "target_dir" metadata. 
    '''
    yaml_loc = join(target_dir, new_step_metadata.target_dir, new_step_metadata.filename)

    with open(yaml_loc, 'w') as stream:
        yaml.dump(new_step_metadata, stream, default_flow_style=False)


def create_in_out_src(target_dir):

    """
    Creates the input, output, and src directories, as well as a source file and .gitkeep files, in the new step.
    Only applicable to pdpp_step (pdpp new) and pdpp_custom (pdpp custom) steps.

    """

    makedirs(join(target_dir, "input"))
    makedirs(join(target_dir, "output"))
    makedirs(join(target_dir, "src"))
    

    f = open(join(target_dir, "input", ".gitkeep"), "a")
    f.close()

    f = open(join(target_dir, "output", ".gitkeep"), "a")
    f.close()

    f = open(join(target_dir, "src", ".gitkeep"), "a")
    f.close()

    f = open(join(target_dir, "src", (target_dir + ".py")), "a")
    f.close()


def populate_new_project(target_dir):
    """
    This is run whenever `pdpp new` and `pdpp custom` is invoked. 
    It checks to see whether the necessary support structure is in place.
    This is also run in a new pdpp subproject. 
    """

    porters = ['_import_', '_export_']
    
    for port in porters:
        port_dir = join(target_dir, port)
        if exists(port_dir) == False:
            makedirs(port_dir)
        keeper = join(port_dir, ".gitkeep")
        if exists(keeper) == False:
            f = open(keeper, "a")
            f.close()

    new_export_class = export_class()
    make_export(new_export_class, target_dir)
    
    try: 
        f = open(join(target_dir, "dodo.py"), "x")
        f.write("from pdpp.task_creator import gen_many_tasks, task_all\n")
        f.write("import doit\n")
        f.write("doit.run(globals())\n")
        f.close()
    except FileExistsError:
        pass

    gitignorelist = [
    ".*!/.gitignore!.gitkeep__pycache__.pyc\n",
    "/.*\n",
    "!/.gitignore\n",
    "*__pycache__\n",
    ".ipynb_checkpoints\n",
    "__pycache__\n",
    "*.pyc\n",
    "/dist/\n",
    "/venv/\n",
    "/build/\n",
    "/*.egg-info\n",
    "/*.egg\n",
    "/.idea\n",
    "*.db\n",
    "*.bak\n",
    "*.dat\n",
    "*.dir\n",
    ]

    try:
        f = open(join(target_dir,".gitignore"), "x")
        for entry in gitignorelist:
            f.write(entry)
    except FileExistsError:
        pass


class import_class(base_pdpp_class):
    """
    This is the class documentation
    """
    def __init__(
        self
        ):

        self.target_dir = "_import_"
        self.enabled = True
        self.dep_files: Dict[str, List[str]]  = {}

    filename = ""
    in_dir = "./"
    out_dir = "./"
    has_source = False
    import_files = []

    def initialize_step(self):
        pass


class export_class(base_pdpp_class):
    """
    This is the class documentation
    """
    def __init__(
            self,
            dep_files = {},
            target_dir = "_export_",
            enabled = True,
            ):

        self.target_dir = "_export_"
        self.dep_files: Dict[str, List[str]] = dep_files
        self.enabled = enabled
        self.import_files = []


    filename = "pdpp_export.yaml"
    in_dir = "./"
    out_dir = ""
    has_source = False
    import_files = []

    def initialize_step(self):
        pass


class step_class(base_pdpp_class):
    """
    This is the class documentation
    """

    def __init__(
            self, 
            target_dir = '',
            dep_files = {}, 
            import_files = [],
            src_files = [], 
            language = '', 
            enabled = True,
            ):

        self.target_dir = target_dir
        self.dep_files: Dict[str, List[str]] = dep_files
        self.import_files = import_files
        self.src_files = src_files
        self.language = language
        self.enabled = enabled

    filename = "pdpp_step.yaml"
    in_dir = "input"
    out_dir = "output"
    src_dir = "src"
    has_source = True

    def initialize_step(self):
        create_in_out_src(self.target_dir)
        self.src_files.append(join(self.target_dir, "src", (self.target_dir + ".py")))
        

class custom_class(base_pdpp_class):
    """
    This is the class documentation
    """
    def __init__(
            self, 
            target_dir = '',
            dep_files = {}, 
            import_files = [],
            shell_commands = [],
            enabled = True
            ):

        self.target_dir = target_dir
        self.dep_files: Dict[str, List[str]] = dep_files
        self.import_files = import_files
        self.shell_commands = []
        self.enabled = enabled

    filename = "pdpp_custom.yaml"
    in_dir = "input"
    out_dir = "output"
    has_source = False

    def initialize_step(self):
        create_in_out_src(self.target_dir)


class project_class(base_pdpp_class):
    """
    This is the class documentation
    """
    def __init__(
            self,
            target_dir = '',
            dep_files = {},
            import_files = [],
            enabled = True):
        
        self.target_dir = target_dir
        self.dep_files: Dict[str, List[str]] = dep_files
        self.import_files = import_files
        self.enabled = enabled
        self.has_source = False

    filename = "pdpp_project.yaml"
    in_dir = "_import_"
    out_dir = "_export_"
    has_source = False

    def initialize_step(self):
        populate_new_project(self.target_dir)