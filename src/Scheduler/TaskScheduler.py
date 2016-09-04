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
        
    def getProcessorList(self, filePath):
        processorsFile = open(filePath)
        processorsData = yaml.load(processorsFile)
        
        for processor, cores in processorsData.iteritems():
            self.processorFreeQueue.put(Processor(processor, cores), block=True, timeout=None)
         
        processorsFile.close()
            
    def getTaskList(self,filePath):
        taskName = ""
        cores, ticks = 0,0
        status = "Y"
        taskObjects = {}
        taskMap = {}
        taskFile = open(filePath)
        
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
    
    def __str__(self):
        return ""

    def executeTasks(self):
        count = 0
        while(True):
            while(True):
                count += 1
                
                if not self.processorFreeQueue.empty():
                    task = self.taskManager.getNextTask()
                    if task == None:
                        break
                    p = self.processorManager.getBestAvailableFreeProcessor(task)
                    if p == None:
                        self.taskManager.addTaskToQueue(task)
                        break
                    else:
                        self.processorManager.allotTaskToProcessor(task,p)
                        
            self.processorManager.decrementTicks()   
            self.processorManager.checkForCompletedTaskAndUpdate()
            
            if (not self.processorManager.runningTasks()) and self.taskQueue.empty():
                break    
            
        exit    
        
