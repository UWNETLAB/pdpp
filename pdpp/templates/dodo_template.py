def create_dodo_template():
    f = open("dodo.py", "x")
    text = """from pdpp.automation.task_creator import gen_many_tasks, task_all
import doit
doit.run(globals())
    """
    f.write(text)
    f.close()
