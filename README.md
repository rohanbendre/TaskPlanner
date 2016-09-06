#TASK PLANNER v1.0

**A python module to schedule tasks according to resources available and dependencies on other tasks.**

**To get started:**
Create a folder with any name (e.g.TaskPanner) on your machine
Clone the repository using git clone https://github.com/rohanbendre/TaskPlanner.git
Go inside src directory and run : sudo python setup.py install

**TUTORIAL:**
A sample program written in python to schedule and execute tasks by reading 2 yaml files for tasks and processors. You can use files given in SampleFiles folder. 

Create a file  and name it TaskPlannerTutorial.py. Copy and paste the given code in it. Save and run from terminal using "python 
TaskPlannerTutorial.py"

```
import Scheduler
from Scheduler import TaskScheduler

t = TaskScheduler.TaskScheduler()
t.getTaskList("path to yaml file with tasks details")
t.getProcessorList("path to yaml file with processor details")
t.executeTasks()
```