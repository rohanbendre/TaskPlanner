from Queue import PriorityQueue as pq

# This class is used to manage tasks to be executed
class TaskManager(object):
    taskQueue = pq()
    
    def __init__(self, taskQueue):
        self.taskQueue = taskQueue
    
    # This method returns the task in queue which is ready to be executed    
    def getNextTask(self):
        if not self.taskQueue.empty(): 
            task = self.taskQueue.get(block=True, timeout=None)
            if task.status == 'Y' or task.status == 'S' or task.status == 'D':
                return task
            else:
                self.taskQueue.put(task)
                return None
        return None    

    def addTaskToQueue(self, task):
        self.taskQueue.put(task)

    # This method marks the task as complete when ticks become 0 and makes the status of task that depend on it to ready        
    def markTaskAsCompleteAndUpdateDependencies(self, task):    
        self.markTaskAsComplete(task)
        self.updatePostTasks(task)
        
    def updatePostTasks(self, task): 
        if task.getPostReq() != None:
            for postTask in task.getPostReq():
                self.updatePreTask(postTask)
                
    def updatePreTask(self, task):            
        for preReqTask in task.getPreReq():
            if preReqTask.getStatus() == 'S':
                self.markTaskAsDiscarded(task)
                return
            if preReqTask.getStatus() != 'C':
                return
        self.markTaskAsReady(task)    
        
    def markTaskAsReady(self, task):    
        task.setStatus("Y")
    
    def markTaskAsComplete(self, task):
        task.setStatus("C")
    
    def markTaskAsDiscarded(self, task):
        task.setStatus("S") 
        print task.name + " cannot be assigned because resources required exceeds available resources or parent task has failed execution!"   

    def markTaskAsDeadlocked(self, task):
        task.setStatus('D')
        print task.name + " cannot be scheduled because of deadlock!"
        