def make_link_task(step, dep_list, disabled_list, mylinker):

    for link_task in step['dep_dirs']:

        link_action_list = []
        link_dep_list = []
        link_targ_list = []

        if link_task in disabled_list:
            print('DISABLED')
            pass
        
        else:
            for full_file in step['dep_files'][link_task]:

                link_in = step['dep_files'][link_task][full_file]['pre_link']
                link_out = step['dep_files'][link_task][full_file]['post_link']
                
                link_dep_list.append(link_in)
                link_targ_list.append(link_out)
                dep_list.append(link_out)

                link_action_list.append(
                    (mylinker, [link_in, link_out])
                )

            yield {
                'basename': 'task_{}_LINK_TO_{}'.format(link_task, step['target_dir']),
                'actions': link_action_list,
                'file_dep': link_dep_list,
                'targets': link_targ_list,
                'clean': True,
            }