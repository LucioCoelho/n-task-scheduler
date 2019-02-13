# n-task-scheduler

A simple scheduler for tasks of known duration across n processors.

Example usage: python3 scheduler.py < sample_input_file_1000x50.txt

Input file contains number of tasks and number of available processors in the first line, separated by spaces. That's then followed by a list of tasks, one task per line, with the first number being the duration of the task and the following ones being the indexes of tasks that dependencies of the current one. The index is the ordinal number of the task, starting with 0. Small example with comments for each line:

6 2     <= seven tasks, two processors
6       <= task 0 takes 6 time units, depends on none
5       <= task 1 takes 5 time units, depends on none
7       <= task 2 takes 7 time units, depends on none
1       <= task 3 takes 1 time unit, depends on none
7 0 1   <= task 4 takes 7 time units, depends on tasks 0 and 1
3 2 3   <= task 5 takes 3 time units, depends on tasks 2 and 3

Output is written to standard output and each line represents a processor. Each line is composed of space-separated pairs of [task index] [task start time]. For instance, a solution for the input above would be:

2 0 4 12            => task 2 initing in processor 0 at time 0, task 4 at time 12
1 0 0 5 3 11 5 12   => tasks 1, 0, 3 and 5 initing in processor 1 at times 0, 5, 11 and 
                       12, respectively.