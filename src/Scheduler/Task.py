class Task(object):
    name,status = "",""
    preReq = []
    postReq = []
    core, ticks = 0,0
    
    def __init__(self, name, status, core, ticks):
        self.name = name
        self.status = status
        self.core = core
        self.ticks = ticks
    
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