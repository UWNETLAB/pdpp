from pdpp.task_types.custom_task import CustomTask
from pdpp.task_types.export_task import ExportTask
from pdpp.task_types.import_task import ImportTask
from pdpp.task_types.step_task   import StepTask
from pdpp.task_types.sub_task    import SubTask
from pdpp.pdpp_class_base import BasePDPPClass
from typing import List, Type

all_task_types: List[Type[BasePDPPClass]]
all_task_types = [CustomTask, ExportTask, ImportTask, StepTask, SubTask]
all_task_filenames = [task.FILENAME for task in all_task_types]