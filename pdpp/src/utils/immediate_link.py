from os import link, remove, makedirs, mkdir
from posixpath import join

def immediate_link(dep_files):
    for dep_step in dep_files:
        for dep_file in dep_files[dep_step]:

            pre_link = dep_files[dep_step][dep_file]['pre_link']
            post_link = dep_files[dep_step][dep_file]['post_link']

            try:
                link(pre_link, post_link)
            except FileExistsError:
                remove(post_link)
                link(pre_link, post_link)
            except FileNotFoundError:
                post_link_list = post_link.split('/')
                print(post_link_list)
                del post_link_list[-1]

                if len(post_link_list) != 0:
                    makedirs(join(*post_link_list))

                link(pre_link, post_link)

                
