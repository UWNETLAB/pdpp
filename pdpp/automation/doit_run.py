from pdpp.automation.task_creator import gen_many_tasks, task_all


def doit_run():
    import doit

    doit.run(globals())


if __name__ == "__main__":
    doit_run()
