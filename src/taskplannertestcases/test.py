import unittest
from scheduler import task_scheduler
from scheduler import processor_manager
from scheduler import task_manager
from scheduler import processor
from Queue import PriorityQueue as pq

class MyTest(unittest.TestCase):
    t = task_scheduler.TaskScheduler()
    taskQueue = pq()
    task = task_scheduler.task.Task("task1", "Y", 1, 100)
    task1 = task_scheduler.task.Task("task1", "Y", 4, 100)
    processor = task_scheduler.processor.Processor("compute1", 2)
    processorFreeQueue = pq()
    processorBusyQueue = pq()
    
    def test_processorCoresNotAvailable(self):
        self.processorFreeQueue.put(self.processor)
        self.assertEqual(processor_manager.ProcessorManager(self.processorFreeQueue, self.processorBusyQueue, task_manager.TaskManager(self.taskQueue.put(self.task1))).getBestAvailableFreeProcessor(self.task1), -1)
        
    def test_processorAvailable(self):
        self.processorFreeQueue.put(self.processor)
        self.assertIsInstance(processor_manager.ProcessorManager(self.processorFreeQueue, self.processorBusyQueue, task_manager.TaskManager(self.taskQueue.put(self.task))).getBestAvailableFreeProcessor(self.task), processor.Processor)    
    
if __name__ == '__main__':
    unittest.main()        