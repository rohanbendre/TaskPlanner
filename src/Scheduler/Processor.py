import Task

class Processor(object):
    name = ""
    core = 0
    remainingTicks = 0
    task = Task.Task
    
    def __init__(self, name, core):
        self.name = name
        self.core = core
        
    def getRemainingTicks(self):
        return self.remainingTicks    
    
    def setRemainingTicks(self, remainingTicks):
        self.remainingTicks = remainingTicks
    
    def getTask(self):
        return self.task
    
    def setTask(self, task):
        self.task = task
        
    def getName(self):
        return self.name
    
    def getCore(self):
        return self.core
    
    def decrementTick(self, cores):
        self.remainingTicks -= cores
        
    def __str__(self):
        return '{} {} {} {}'.format(self.name, self.core, self.remainingTicks, self.task)            
    
    def __cmp__(self, other):
        if other == None or other == -1:
            return -1
        return cmp(self.core,other.core)