def create_dodo_template():
    text = """from pdpp.automation.task_creator import gen_many_tasks, task_all
import doit
doit.run(globals())
    """
    with open("dodo.py", "x") as f:
        f.write(text)
