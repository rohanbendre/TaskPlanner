from Queue import Queue, PriorityQueue
from Task import Task
from Processor import Processor
from TaskManager import TaskManager
from ProcessorManager import ProcessorManager
from _heapq import heappush, heappop

class TaskScheduler(object):
    taskQueue = []
    processorFreeQueue = []
    processorBusyQueue = []
    taskManager = TaskManager(taskQueue)
    processorManager = ProcessorManager(processorFreeQueue, processorBusyQueue, taskManager)
        
    def getDummyTaskList(self):
        taskList = []
        task1 = Task("task1", "Y", 2, 100)
        task2 = Task("task2", "Y", 2, 200)
        task3 = Task("task3", "N", 4, 50)
        
        task1.getPostReq().append(task3)
        task2.getPostReq().append(task3)
          
        task3.getPreReq().append(task1)
        task3.getPreReq().append(task2)
        
        taskList.append(task1)
        taskList.append(task2)
        taskList.append(task3)
        
        heappush(self.taskQueue, taskList)
        print type(self.taskQueue)
#         for i,items in enumerate(self.taskList):
#             print items
#             
#         tasks = heappop(self.taskQueue)
#         for items in tasks:
#             print items  

    def getDummyProcessorList(self):
        processorList = []
        processorList.append(Processor("compute1", 2))
        processorList.append(Processor("compute2", 2))
        processorList.append(Processor("compute3", 6))
        
        heappush(self.processorFreeQueue, processorList)    
    def __str__(self):
        return ""        
        
t = TaskScheduler()
 
t.getDummyTaskList()