from os.path import isdir, join


def proj_folder_test(dirs):

    if isdir(join(dirs, 'src')) and isdir(join(dirs, 'input')) and isdir(join(dirs, 'output')):
        return True
    else:
        return False
