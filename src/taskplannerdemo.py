import scheduler

from scheduler import task_scheduler

t = task_scheduler.TaskScheduler()
t.getTaskList("path_to_yaml_file_for_tasks")
t.getProcessorList("path_to_yaml_file_for_processors")
t.executeTasks()
