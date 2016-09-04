from Queue import PriorityQueue as pq

class TaskManager(object):
    taskQueue = pq()
    
    def __init__(self, taskQueue):
        self.taskQueue = taskQueue
        
    def getNextTask(self):
        if not self.taskQueue.empty(): 
            task = self.taskQueue.get(block=True, timeout=None)
            if task.status == 'Y':
                return task
            else:
                self.taskQueue.put(task)
                return None
        return None    

    def addTaskToQueue(self, task):
        self.taskQueue.put(task)
        
    def markTaskAsCompleteAndUpdateDependencies(self, task):    
        self.markTaskAsComplete(task)
        self.updatePostTasks(task)
        
    def updatePostTasks(self, task): 
        if task.getPostReq() != None:
            for postTask in task.getPostReq():
                self.updatePreTask(postTask)
                
    def updatePreTask(self, task):            
        for preReqTask in task.getPreReq():
            if preReqTask.getStatus() != 'C':
                return
        self.markTaskAsReady(task)    
        
    def markTaskAsReady(self, task):    
        task.setStatus("Y")
        self.taskQueue.get()
        self.taskQueue.put(task)
    
    def markTaskAsComplete(self, task):
        task.setStatus("C")