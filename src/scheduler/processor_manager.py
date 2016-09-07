from Queue import PriorityQueue as pq
from scheduler import task_manager

# This class is used to manage all the processor related operations for tasks
class ProcessorManager(object):
    maxCoresAvailable = 0
    processorFreeQueue = pq()
    processorBusyQueue = pq()
    taskManager = task_manager
    def __init__(self, processorFreeQueue, processorBusyQueue, taskManager):
        self.processorFreeQueue = processorFreeQueue
        self.processorBusyQueue = processorBusyQueue
        self.taskManager = taskManager
    
    # Method to get processor for a task that is ready to be executed    
    def getBestAvailableFreeProcessor(self, task):
        count = 0
        removed = []
        freeProcessors = self.processorFreeQueue._qsize(len)
        while count < freeProcessors:
            processor = self.processorFreeQueue.get()
            if processor.getCore() >= task.getCore():
                for busyprocessors in removed:
                    self.processorFreeQueue.put(busyprocessors)
                return processor
            # If requirements for task exceed available resources, we discard the task and tasks dependent on it 
            elif task.getCore() > self.maxCoresAvailable:
                removed.append(processor)
                self.taskManager.markTaskAsDiscarded(task)
                self.taskManager.updatePostTasks(task)
                self.updateProcessorInformation(processor)
                return -1
            else:
                removed.append(processor)
            count += 1
        self.maintainFreeQueue(removed)    
        return None    
    
    # Allot task to processor and start execution        
    def allotTaskToProcessor(self, task, processor):
        self.processorBusyQueue.put(processor)
        processor.setTask(task)
        processor.setRemainingTicks(task.getTicks())
        print "Task : " + task.getName() + " , Processor : " + processor.getName()
    
    # Simulating ticks for a process
    def decrementTicks(self):
        count = 0
        removed = []
        busyProcessors = self.processorBusyQueue._qsize(len) 
        while count < busyProcessors:
            processor = self.processorBusyQueue.get_nowait()
            processor.decrementTick(processor.getCore())
            removed.append(processor)
            count += 1
        self.maintainBusyQueue(removed)    
     
    # Methods to handle freeing of processor, marking tasks as complete when execution has finished (tick remaining is 0)        
    def markTaskAsCompleted(self, task):        
        self.taskManager.markTaskAsCompleteAndUpdateDependencies(task)
        
    def checkForCompletedTaskAndUpdate(self):
        count = 0
        removed = []
        busyProcessors = self.processorBusyQueue._qsize(len) 
        while count < busyProcessors:
            processor = self.processorBusyQueue.get()
            if processor.getRemainingTicks() == 0:
                self.markTaskAsCompleted(processor.getTask())
                self.updateProcessorInformation(processor)    
            else:
                removed.append(processor)    
            count += 1    
        self.maintainBusyQueue(removed)    
            
    def updateProcessorInformation(self, processor):        
        processor.setTask(None)
        self.addProcessorToProcessorFreeQueue(processor)
        
    def addProcessorToProcessorFreeQueue(self, processor):    
        self.processorFreeQueue.put(processor)
    
    def removeProcessorFromProcessorBusyQueue(self, processor):    
        processor.processorBusyQueue.get()
        
    def runningTasks(self):
        if self.processorBusyQueue._qsize(len) > 0:
            return True
        else:
            return False    
        
    def maintainFreeQueue(self, removedProcessors):
        for busyprocessors in removedProcessors:
            self.processorFreeQueue.put(busyprocessors)
            
    def maintainBusyQueue(self, removedProcessors):
        for busyprocessors in removedProcessors:
            self.processorBusyQueue.put(busyprocessors)        