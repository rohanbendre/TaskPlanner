import scheduler

from scheduler import task_scheduler

t = task_scheduler.TaskScheduler()
t.getTaskList("/Users/rohanbendre/Desktop/user.yaml")
t.getProcessorList("/Users/rohanbendre/Desktop/processors.yaml")
t.executeTasks()