from Queue import PriorityQueue as pq
from scheduler import processor
from scheduler import processor_manager
from scheduler import task
from scheduler import task_manager
import yaml
from collections import defaultdict

# This is the main driver class
class TaskScheduler(object):
    taskQueue = pq()
    processorQueue = processor
    processorFreeQueue = pq()
    processorBusyQueue = pq()
    taskManager = task_manager.TaskManager(taskQueue)
    processorManager = processor_manager.ProcessorManager(processorFreeQueue, processorBusyQueue, taskManager)
    
    # Read yaml file and create list of available computing resources
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
                    if processor_manager.ProcessorManager.maxCoresAvailable < cores:
                        processor_manager.ProcessorManager.maxCoresAvailable = cores
                    self.processorFreeQueue.put(self.processorQueue.Processor(processor, cores), block=True, timeout=None)
            else:
                print "Input file is empty. Please include computing resources present!"        
                exit(1)
                
            processorsFile.close()
    
    # Read yaml file that contains task list            
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
            # Updating task queue with various details of task like cores needed, execution time, parent tasks
            if fileData != None:
                for task, details in fileData.iteritems():
                    status = "Y"
                    taskName = task.lower()
                    if 'cores_required' in details:
                        if int(details['cores_required']) > 0:
                            cores = int(details['cores_required'])
                        else:
                            cores = 0    
                    else:
                        cores = 1    
                    if 'execution_time' in details:
                        if int(details['execution_time']) > 0:
                            ticks = int(details['execution_time'])
                        else:
                            ticks = 100    
                    else:
                        ticks = 100    
                    if 'parent_tasks' in details:
                        if (bool(details['parent_tasks'])):
                            status = "N"
                            taskMap[taskName] = details['parent_tasks'].lower()
                        
                    task = self.getTask(taskName, status, cores, ticks)
                    self.taskQueue.put(task, block=True, timeout=False)
                    taskObjects[taskName] = task          
                    if status == 'N':
                        self.addDependentTasks(taskMap, taskObjects, task, details['parent_tasks'].lower())
                
                for task in taskObjects.itervalues():
                    if len(task.PreReq) > 0:
                        for i, taskString in enumerate(task.PreReq):
                            task.getPreReq().append(taskObjects[taskString])
                            taskObjects[taskString].getPostReq().append(task)
                
            else:
                print "Input file is empty. Please include tasks to be processed!"
                exit(1)
                            
            taskFile.close()
    
    # If tasks depend on some other tasks, we create a list of dependencies called Post-requirements and Pre-requirements    
    def addDependentTasks(self, taskMap, taskObjects, task, dependentTasks):
        if dependentTasks != None:
            for taskName in dependentTasks.split(","):   
                task.PreReq.append(taskName.strip())
    
    def getTask(self, taskName, dependent, core, ticks):
        return task.Task(taskName, dependent, core, ticks)
    
    def __str__(self):
        return ""

    # This function will execute till the taskQueue is not empty and processor busy queue is not empty
    def executeTasks(self):
        while(True):
            while(True):                
                if not self.processorFreeQueue.empty():
                    task = self.taskManager.getNextTask()
                    if task == None:
                        break
                    if task.status == 'S':
                        self.taskManager.updatePostTasks(task)
                        break
                    p = self.processorManager.getBestAvailableFreeProcessor(task)
                    if p == None:
                        self.taskManager.addTaskToQueue(task)
                        break
                    elif p == -1:
#                         print task.name + " cannot be assigned because resources required exceeds available resources!"
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
        