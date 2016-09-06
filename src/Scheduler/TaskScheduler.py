from Queue import PriorityQueue as pq
from Processor import Processor
from ProcessorManager import ProcessorManager
from Task import Task
from TaskManager import TaskManager
import yaml
import time

class TaskScheduler(object):
    taskQueue = pq()
    processor = Processor
    processorFreeQueue = pq()
    processorBusyQueue = pq()
    taskManager = TaskManager(taskQueue)
    processorManager = ProcessorManager(processorFreeQueue, processorBusyQueue, taskManager)
    
    def getProcessorList(self, filePath):
        try:
            processorsFile = open(filePath)
        except IOError:
            print "File not found. Please specify the correct path!"
            exit(1)
        else:        
            processorsData = yaml.load(processorsFile)
            if processorsData != None:
                for processor, cores in processorsData.iteritems():
                    if ProcessorManager.maxCoresAvailable < cores:
                        ProcessorManager.maxCoresAvailable = cores
                    self.processorFreeQueue.put(Processor(processor, cores), block=True, timeout=None)
            else:
                print "Input file is empty. Please include computing resources present!"        
                exit(1)
                
            processorsFile.close()
                
    def getTaskList(self,filePath):
        taskName = ""
        cores, ticks = 0,0
        status = "Y"
        taskObjects = {}
        taskMap = {}
        
        try:
            taskFile = open(filePath)
        except IOError:
            print "File not found. Please specify the correct path!"   
            exit(1) 
        else:
            fileData = yaml.load(taskFile)
            if fileData != None:
                for task, details in fileData.iteritems():
                    status = "Y"
                    taskName = task
                    if 'cores_required' in details:
                        cores = int(details['cores_required'])
                    else:
                        cores = 1    
                    if 'execution_time' in details:
                        ticks = int(details['execution_time'])
                    else:
                        ticks = 100    
                    if 'parent_tasks' in details:
                        if (bool(details['parent_tasks'])):
                            status = "N"
                            taskMap[taskName] = details['parent_tasks']
                        
                    task = self.getTask(taskName, status, cores, ticks)
                    self.taskQueue.put(task, block=True, timeout=False)
                    taskObjects[taskName] = task          
                    if status == 'N':
                        self.addDependentTasks(taskMap, taskObjects, task, details['parent_tasks'])
            else:
                print "Input file is empty. Please include tasks to be processed!"
                exit(1)
                            
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
                if not self.processorFreeQueue.empty():
                    task = self.taskManager.getNextTask()
                    if task == None:
                        break
                    p = self.processorManager.getBestAvailableFreeProcessor(task)
                    if p == None:
                        self.taskManager.addTaskToQueue(task)
                        break
                    elif p == -1:
                        print task.name + " cannot be assigned because resources required exceeds available resources!"
                        break
                    else:
                        self.processorManager.allotTaskToProcessor(task,p)
                
                else:
                    self.processorManager.decrementTicks()   
                    self.processorManager.checkForCompletedTaskAndUpdate()
                    
            self.processorManager.decrementTicks()   
            self.processorManager.checkForCompletedTaskAndUpdate()
            
            if (not self.processorManager.runningTasks()) and self.taskQueue.empty():
                break    
            
        exit    
        