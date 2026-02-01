This program is a simulation of a file compression system. You can think of it like a small factory where files come in, workers compress them, and the system keeps track of what is happening at each moment.

Each file is treated as a job. Bigger files take longer to compress, and smaller files finish faster. The system does not process files randomly. Instead, it always chooses to compress the smallest file first so that more jobs can finish quickly.

The system has a fixed number of workers. A worker can either be idle or busy working on one file at a time. Time in the system does not flow automatically; instead, it moves forward step by step using something called a “tick”. Each tick represents one unit of time passing in the system.

When time moves forward, workers continue working on their assigned jobs. The remaining time for each job goes down. If a job finishes, it is marked as completed and removed from the worker. If a job fails, it is placed in a retry queue so it can be attempted again later. Jobs can also be cancelled, but only if they have not started yet.

The system also keeps a small history of jobs that have finished or been cancelled. This history has a fixed size, so when it becomes full, the oldest record is removed to make space for new ones.

Main parts of the code

Job

A Job represents a single file that needs to be compressed. It stores basic information such as the file’s ID, its size, how much time is left to finish compressing it, and its current status. Jobs are compared by size so that smaller jobs are always processed before larger ones.

HistoryLog

This part of the code is responsible for keeping track of recently completed or cancelled jobs. It acts like a short memory. Once it reaches its maximum size, it starts forgetting the oldest jobs to make room for newer ones.

CompressionSystem

This is the core of the program. It manages workers, jobs, time, and the overall workflow. It keeps track of which workers are busy, which jobs are waiting, which jobs need to retry, and all jobs that exist in the system.

When a file is submitted, the system creates a new job and adds it to the waiting list. When time moves forward using a tick, idle workers pick up new jobs, working workers reduce the remaining time on their jobs, and finished jobs are handled properly. If a job is cancelled before it starts, it is removed and recorded in history.

The status function is used to show the current state of the system, including which jobs are running, waiting, completed, or cancelled.