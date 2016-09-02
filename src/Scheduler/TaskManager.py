class TaskManager(object):
    taskQueue = []
    
    def __init__(self, taskQueue):
        print type(taskQueue)
        self.taskQueue = taskQueue
        
#     def getNextTask(self):
#         if self.taskQueue.