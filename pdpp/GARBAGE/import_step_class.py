# import yaml
# from posixpath import join
# from os.path import exists
# from pdpp.pdpp_class import base_pdpp_class, step_class, custom_class, project_class, export_class


# def export_pdpp_class(new_step_metadata: base_pdpp_class): 

#     '''
#     Saves a pdpp-compliant step_class in the directory indicated in its
#     "target_dir" metadata. 
#     '''
#     yaml_loc = join(new_step_metadata.target_dir, new_step_metadata.filename)

#     with open(yaml_loc, 'w') as stream:
#         yaml.dump(new_step_metadata, stream, default_flow_style=False)


# def import_step_class(target_dir:str, filename:str) -> base_pdpp_class:
#     ''' 
#     Loads the .yaml file containing a pdpp-compliant class and returns 
#     a step_class object.
#     '''


#     yaml_loc = join(target_dir, filename)

#     if exists(yaml_loc):
#         with open(join(yaml_loc), 'r') as stream:
#             step = yaml.full_load(stream) 

#             if isinstance(step, base_pdpp_class):
#                 return step
#             else:
#                 if filename == step_class.filename:
#                     return step_class(target_dir=target_dir)
#                 elif filename == custom_class.filename:
#                     return custom_class(target_dir=target_dir)
#                 elif filename == project_class.filename:
#                     return project_class(target_dir=target_dir)
#                 elif filename == export_class.filename:
#                     return export_class()
#                 else:
#                     print("something messed up!")
#                     raise Exception
            

#     else:
#         return step_class()