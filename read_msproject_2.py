import jpype
import mpxj

jpype.startJVM()

from net.sf.mpxj.reader import UniversalProjectReader
from net.sf.mpxj import FieldTypeClass
from net.sf.mpxj import TaskField

# Load the project file
project = UniversalProjectReader().read('project-with-custom-fields.mpp')

# Display basic task information
print("Tasks")
tasks = project.getTasks()

for task in tasks:
    print(f"{task.getID()}\t{task.getName()}")
print()

# Display custom fields available in the project
print("Custom Fields")
for field in project.getCustomFields():
    print(f"{field.getFieldType().getFieldTypeClass()}\t{field.getFieldType()}\t{field.getAlias()}")
print()

# Filter out custom fields that are specific to tasks
task_custom_fields = [field for field in project.getCustomFields()
                      if field.getFieldType().getFieldTypeClass() == FieldTypeClass.TASK]

print("Task Custom Fields")
for field in task_custom_fields:
    print(f"{field.getFieldType().getFieldTypeClass()}\t{field.getFieldType()}\t{field.getAlias()}")

# Prepare column headings and field types for reporting
column_names = ['ID', 'Name']
column_types = [TaskField.ID, TaskField.NAME]
for field in task_custom_fields:
    column_names.append(str(field.getAlias()))
    column_types.append(field.getFieldType())

# Print the column headings
print('\t'.join(column_names))

# Print task details along with custom field values
for task in tasks:
    column_values = [str(task.getCachedValue(type)) for type in column_types]
    print(f"{task.getID()}\t{task.getName()}\t{'\t'.join(column_values)}")

jpype.shutdownJVM()
