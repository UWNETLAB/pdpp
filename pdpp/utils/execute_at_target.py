from os import chdir, getcwd

# VERY IMPORTANT: Use the 'execute_at_target' function wrapper to
# take actions inside task directories; do not manually
# move the target directory!!


def execute_at_target(func, task):
    original_dir = getcwd()
    chdir(task.target_dir)
    try:
        func(task)
    finally:
        chdir(original_dir)
