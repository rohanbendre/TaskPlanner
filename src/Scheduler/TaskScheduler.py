from Queue import Queue as Q
from Queue import PriorityQueue as pq
from Task import Task
from Processor import Processor
from TaskManager import TaskManager
from ProcessorManager import ProcessorManager
from time import sleep
from objc._objc import NULL

class TaskScheduler(object):
    taskQueue = pq()
    processor = Processor
    processorFreeQueue = pq()
    processorBusyQueue = pq()
    taskManager = TaskManager(taskQueue)
    processorManager = ProcessorManager(processorFreeQueue, processorBusyQueue, taskManager)
        
    def getDummyTaskList(self):
        task1 = Task("task1", "Y", 2, 100)
        task2 = Task("task2", "Y", 2, 200)
        task3 = Task("task3", "N", 4, 50)
        
        task1.getPostReq().append(task3)
        task2.getPostReq().append(task3)
          
        task3.getPreReq().append(task1)
        task3.getPreReq().append(task2)

        self.taskQueue.put(task1, block=True, timeout=None)
        self.taskQueue.put(task2, block=True, timeout=None)
        self.taskQueue.put(task3, block=True, timeout=None)
        
    def getDummyProcessorList(self):
        self.processorFreeQueue.put(Processor("compute1",2), block=True, timeout=None)
        self.processorFreeQueue.put(Processor("compute2",2), block=True, timeout=None)
        self.processorFreeQueue.put(Processor("compute3",6), block=True, timeout=None)
            
    def __str__(self):
        return ""   
        
t = TaskScheduler()
 
t.getDummyTaskList()
t.getDummyProcessorList()
# print t.processor.processorFreeQueue.qsize()

count = 0
while(True):
    while(True):
        count += 1
        
#         print "Count : " ,count 
        if not t.processorFreeQueue.empty():
            task = t.taskManager.getNextTask()
#             print "TASK : " + str(task)
            if task == None:
                break
            p = t.processorManager.getBestAvailableFreeProcessor(task)
#             print p
            if p == None:
                t.taskManager.addTaskToQueue(task)
                break
            else:
                t.processorManager.allotTaskToProcessor(task,p)
                
    t.processorManager.decrementTicks()   
    t.processorManager.checkForCompletedTaskAndUpdate()
    
    if (not t.processorManager.runningTasks()) and t.taskQueue.empty():
        break    
    
exit    