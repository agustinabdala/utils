import jpype
import mpxj

jpype.startJVM()
print(jpype.getJVMVersion())
from net.sf.mpxj.reader import UniversalProjectReader
project = UniversalProjectReader().read('240226- Plan AV 1039 IDBP 70.mpp')

print("Tasks")

for task in project.getTasks():
    print(f"ID: {task.getID()},\n\
        Name: {task.getName()},\n\
        Start: {task.getStart()},\n\
        Finish: {task.getFinish()},\n\
        Duration: {task.getDuration()},\n\
        ResourceNames: {task.getResourceNames()},\n\
        PercentageComplete: {task.getPercentageComplete()},\n\
        Notes: {task.getNotes()},\n\
        Priority: {task.getPriority()},\n\
        BaselineStart: {task.getBaselineStart()},\n\
        BaselineFinish: {task.getBaselineFinish()},\n\
        ActualStart: {task.getActualStart()},\n\
        ActualFinish: {task.getActualFinish()},\n\
        Work: {task.getWork()},\n\
        ActualWork: {task.getActualWork()},\n\
        RemainingWork: {task.getRemainingWork()},\n\
        Milestone: {task.getMilestone()},\n\
        LevelingDelay: {task.getLevelingDelay()}\n\
        ")
jpype.shutdownJVM()
