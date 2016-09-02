from TaskManager import TaskManager
from Queue import PriorityQueue as pq

class ProcessorManager(object):
    processorFreeQueue = pq()
    processorBusyQueue = pq()
    taskManager = TaskManager
    
    def __init__(self, processorFreeQueue, processorBusyQueue, taskManager):
        self.processorFreeQueue = processorFreeQueue
        self.processorBusyQueue = processorBusyQueue
        self.taskManager = taskManager
        
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
            else:
                removed.append(processor)
            count += 1
        for busyprocessors in removed:
            self.processorFreeQueue.put(busyprocessors)    
        return None    
            
    def allotTaskToProcessor(self, task, processor):
        self.processorBusyQueue.put(processor)
        processor.setTask(task)
        processor.setRemainingTicks(task.getTicks())
        print "Task : " + task.getName() + " , Processor : " + processor.getName()
    
    def decrementTicks(self):
        count = 0
        removed = []
        while count < self.processorBusyQueue._qsize(len):
            processor = self.processorBusyQueue.get_nowait()
            processor.decrementTick()
            removed.append(processor)
#             print " Insidie decrement"
            count += 1
        for busyprocessors in removed:
            self.processorBusyQueue.put(busyprocessors)    
            
    def markTaskAsCompleted(self, task):        
        self.taskManager.markTaskAsCompleteAndUpdateDependencies(task)
        
    def checkForCompletedTaskAndUpdate(self):
        count = 0
        removed = []
        while count < self.processorBusyQueue._qsize(len):
            processor = self.processorBusyQueue.get()
            if processor.getRemainingTicks() == 0:
                self.markTaskAsCompleted(processor.getTask())
                self.updateProcessorInformation(processor)    
            else:
                removed.append(processor)    
            count += 1    
        for busyprocessors in removed:
            self.processorBusyQueue.put(busyprocessors)    
            
    def updateProcessorInformation(self, processor):        
        processor.setTask(None)
#         self.removeProcessorFromProcessorBusyQueue(processor)
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