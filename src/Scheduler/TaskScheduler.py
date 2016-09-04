from Queue import PriorityQueue as pq
from Queue import Queue as Q
from objc._objc import NULL
from time import sleep

from Processor import Processor
from ProcessorManager import ProcessorManager
from Task import Task
from TaskManager import TaskManager
import yaml

class TaskScheduler(object):
    taskQueue = pq()
    processor = Processor
    processorFreeQueue = pq()
    processorBusyQueue = pq()
    taskManager = TaskManager(taskQueue)
    processorManager = ProcessorManager(processorFreeQueue, processorBusyQueue, taskManager)
        
    def getDummyTaskList(self):
        task1 = Task("task1", "Y", 2, 100)
        task2 = Task("task2", "N", 2, 200)
        task3 = Task("task3", "N", 4, 50)

        task1.getPostReq().append(task2)        
        task1.getPostReq().append(task3)
        task2.getPostReq().append(task3)
        
        task2.getPreReq().append(task1)
        task3.getPreReq().append(task1)
        task3.getPreReq().append(task2)

        self.taskQueue.put(task1, block=True, timeout=None)
        self.taskQueue.put(task2, block=True, timeout=None)
        self.taskQueue.put(task3, block=True, timeout=None)
        
    def getProcessorList(self):
        processorsFile = open("processors.yaml")
        processorsData = yaml.load(processorsFile)
        
        for processor, cores in processorsData.iteritems():
            self.processorFreeQueue.put(Processor(processor, cores), block=True, timeout=None)
            
    def __str__(self):
        return ""
    
    def getTaskList(self):
        taskName = ""
        cores, ticks = 0,0
        status = "Y"
        taskObjects = {}
        taskMap = {}
        taskFile = open("user.yaml")
        dependentTask = False
        
        fileData = yaml.load(taskFile)
        
        for task, details in fileData.iteritems():
            taskName = task
            if 'cores_required' in details:
                cores = int(details['cores_required'])
            if 'execution_time' in details:
                ticks = int(details['execution_time'])
            if 'parent_tasks' in details:
                status = "N"
                taskMap[taskName] = details['parent_tasks']
                
            task = self.getTask(taskName, status, cores, ticks)
            self.taskQueue.put(task, block=True, timeout=False)
            taskObjects[taskName] = task          
            if status == 'N':
                self.addDependentTasks(taskMap, taskObjects, task, details['parent_tasks'])
        
        taskFile.close()
        
    def addDependentTasks(self, taskMap, taskObjects, task, dependentTasks):
        if dependentTasks != None:
            for taskName in dependentTasks.split(","):
                task.getPreReq().append(taskObjects[taskName.strip()])
                taskObjects[taskName.strip()].getPostReq().append(task)    
    
    def getTask(self, taskName, dependent, core, ticks):
        return Task(taskName, dependent, core, ticks)
        
t = TaskScheduler()
 
t.getTaskList()
t.getProcessorList()

count = 0
while(True):
    while(True):
        count += 1
        
#         print "Count : " ,count 
        if not t.processorFreeQueue.empty():
            task = t.taskManager.getNextTask()
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