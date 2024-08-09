import jpype
import mpxj

jpype.startJVM()
print(jpype.getJVMVersion())
from net.sf.mpxj.reader import UniversalProjectReader
project = UniversalProjectReader().read('path_to_your_project_file.mpp')

print("Tasks")
for task in project.getTasks():
	print(f"ID: {task.getID()},\n\
	Name: {task.getName()},\n\
        Start: {task.getStart()},\n\
        Finish: {task.getFinish()},\n\
        Duration: {task.getDuration()},\n\
        ResourceNames: {task.getResourceNames()}\n\
		Percentage: {task.getPercentageComplete()}\
		")
jpype.shutdownJVM()