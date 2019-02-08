import sys

class Task:

      def __init__(self,input_line,index):
          self.index=index
          cols=input_line.split()
          self.duration=int(cols[0])
          self.dependencies=[]
          for col in cols[1:]:
              self.dependencies.append(int(col))
          self.processed=False
          self.processing=False
          self.assigned=False

      def has_dependency_at(self,processors):
          for processor in processors:
              for index in self.dependencies:
                  if processor.has_task_index(index):
                     return True
          return False

class Processor:

      def __init__(self,index):
          self.queue=[]
          self.index=index

      def remove_task(self,task):
          self.queue.remove(task)

      def find_lightest_task(self):
          output=self.queue[0]
          for task in self.queue:
              if task.duration<output.duration:
                 output=task
          return output

      def total_time(self):
          output=0
          for task in self.queue:
              output+=task.duration
          return output

      def add_str(self,out_lines,index,barrier_time):
          start_time=barrier_time
          for task in self.queue:
              out_lines[index]+=str(task.index)+" "+str(start_time)+" "
              start_time+=task.duration
          return start_time

      def add_task(self,task):
          self.queue.append(task)
          task.assigned=True

      def has_task_index(self,index):
          for task in self.queue:
              if task.index==index:
                 return True
          return False

def has_unassigned(tasks):
    for task in tasks:
        if not task.assigned:
           return True
    return False

def has_unprocessed(tasks):
    for task in tasks:
        if not task.processed:
           return True
    return False

def process(task,tasks,queue):
    if task.processed:
       return True
    if task.processing: # Finds circular dependency
       return False
    task.processing=True
    if len(task.dependencies)==0:
       task.processing=False
       task.processed=True
       queue.append(task)
       return True
    for index in task.dependencies:
        dependency=tasks[index]
        if not process(dependency,tasks,queue): # Circular dependency found downstream
           return False
    queue.append(task)
    task.processing=False
    task.processed=True
    task.assigned=False
    return True

def find_end_time(processors):
    output=0
    for processor in processors:
        output=max(output,processor.total_time())
    return output

def find_heavier_processor(processors):
    max_time=0
    output=None
    for processor in processors:
        current_time=processor.total_time()
        if current_time>max_time:
           max_time=current_time
           output=processor
    return output

def find_lighter_processor(processors,heavier):
    min_time=heavier.total_time()
    output=None
    for processor in processors:
        current_time=processor.total_time()
        if current_time<min_time:
           min_time=current_time
           output=processor
    return processor

def load_balance(processors):
    end_time=find_end_time(processors)
    while True:
          heavier=find_heavier_processor(processors)
          lighter=find_lighter_processor(processors,heavier)
          lightest_task=heavier.find_lightest_task()
          heavier.remove_task(lightest_task)
          lighter.add_task(lightest_task)
          new_time=find_end_time(processors)
          if new_time>=end_time:
             lighter.remove_task(lightest_task)
             heavier.add_task(lightest_task)
             break
          end_time=new_time

lines=[]
for line in sys.stdin:
    lines.append(line)
cols=lines[0].split()
N=int(cols[0])
K=int(cols[1])
sys.stderr.write(str(N)+","+str(K)+"\n")
tasks=[]
index=0
for line in lines[1:]:
    tasks.append(Task(line,index))
    index+=1
queue=[]
while has_unprocessed(tasks):
      for task in tasks:
          if task.processed:
             continue
          if not process(task,tasks,queue):
             print("infeasible")
             sys.exit(0)
stages=[]
stage_index=0
while has_unassigned(tasks):
      processors=[]
      for i in range(K):
          processors.append(Processor(i))
      cycler=0
      for task in queue:
          if task.assigned:
             continue
          if task.has_dependency_at(processors):
             continue
          task.assigned=True
          processors[cycler].add_task(task)
          cycler=(cycler+1)%K
      load_balance(processors)
      stages.append(processors)
out_lines=[]
for i in range(K):
    out_lines.append("")
barrier_time=0
for processors in stages:
    new_barrier=0
    for i in range(len(processors)):
        processor_time=processors[i].add_str(out_lines,i,barrier_time)
        if processor_time>new_barrier:
           new_barrier=processor_time
    barrier_time=new_barrier
for line in out_lines:
    print(line.strip())
sys.stderr.write("Final time: "+str(barrier_time)+"\n")

