from TaskManager import TaskManager

class ProcessorManager(object):
    processorFreeQueue = []
    processorBusyQueue = []
    taskManager = TaskManager
    
    def __init__(self, processorFreeQueue, processorBusyQueue, taskManager):
        self.processorFreeQueue = processorFreeQueue
        self.processorBusyQueue = processorBusyQueue
        self.taskManager = taskManager