import yaml
from posixpath import join
from os.path import exists
from pprint import pprint

def test_pdpp_version(step):
    step['target_dir'] != None
    step['dep_dirs'] != None
    step['dep_files'] != None
    step['src_files'] != None
    step['language'] != None
    step['target_status'] != None
    step['target_files'] != None
    step['self_deps'] != None
    step['enabled'] != None


def return_empty_yaml(yaml_loc, return_empty):
    if return_empty:
        return {
        'target_dir': None,
        'dep_dirs': [],
        'dep_files': {},
        'src_files': [],
        'language': [],
        'target_status': False,
        'target_files': [],
        'self_deps': [], 
        'enabled': True,
        }, yaml_loc
    else:
        return False, False



def import_yaml(target_dir = './', return_empty=True):

    yaml_loc = join(target_dir, 'pdpp_step.yaml')

    if exists(yaml_loc):
        with open(join(yaml_loc), 'r') as stream:
            step = yaml.load(stream) 
            try:
                test_pdpp_version(step)
                return step, yaml_loc 

            except KeyError:
                junk = input(f"""
                {yaml_loc} is not 
                compatible with the current version of pdpp.
                It will be overwritten with an empty pdpp yaml file.
                Press enter to contine.
                """)

                return return_empty_yaml(yaml_loc, return_empty)
    else:
        return return_empty_yaml(yaml_loc, return_empty)

if __name__ == '__main__':
    pprint(import_yaml())
