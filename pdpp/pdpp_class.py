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

    gitignorelist = '''
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PDPP-specific
_import_/*
!_import_/.gitkeep
_export_/*
!_export_/.gitkeep
!.pdpp_export.yaml

*/input/*
*/output/*
!*.gitkeep

# doit-specific
*.doit.db*
'''

    try:
        f = open(join(target_dir,".gitignore"), "x")
        f.write(gitignorelist)
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


    filename = ".pdpp_export.yaml"
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

    filename = ".pdpp_step.yaml"
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

    filename = ".pdpp_custom.yaml"
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

    filename = ".pdpp_project.yaml"
    in_dir = "_import_"
    out_dir = "_export_"
    has_source = False

    def initialize_step(self):
        populate_new_project(self.target_dir)