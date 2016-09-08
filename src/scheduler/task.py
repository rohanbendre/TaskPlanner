# This class is used to create object of task. 
# It has details like task name, cores needed, execution time and status which we are using to indicate if task is ready to be executed or not.
# Pre and post dependencies are also maintained by this class
from operator import xor
class Task(object):
    name,status = "",""
    core, ticks = 0,0
    
    def __init__(self, name, status, core, ticks):
        self.name = name
        self.status = status
        self.core = core
        self.ticks = ticks
        self.preReq = []
        self.postReq = []
    
    def getStatus(self):
        return self.status
    
    def setStatus(self, status):
        self.status = status 
    
    def getName(self):
        return self.name    
        
    def getPreReq(self):
        return self.preReq    
    
    def getPostReq(self):
        return self.postReq
    
    def __str__(self):
        return '{} {} {} {}'.format(self.name, self.status, self.core, self.ticks)
    
    def getCore(self):
        return self.core
    
    def getTicks(self):
        return self.ticks
    
    def __cmp__(self, other):
        if other == None:
            return -1
        # Priority of tasks based on execution time and status
        if other.status == 'Y':
            return cmp(self.ticks, other.ticks)  
        return cmp(other.status, self.status)