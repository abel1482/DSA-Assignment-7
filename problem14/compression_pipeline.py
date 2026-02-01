import heapq
from collections import deque


class Job:
    def __init__(self, file_id, size, submit_time):
        self.file_id = file_id
        self.size = size
        self.submit_time = submit_time
        self.remaining_time = size // 10
        self.status = "Pending"
        self.fail = False

    def __lt__(self, other):
        return self.size < other.size


class HistoryLog:
    def __init__(self, capacity):
        self.capacity = capacity
        self.log = [None] * capacity
        self.index = 0
        self.count = 0

    def add(self, job_id):
        self.log[self.index] = job_id
        self.index = (self.index + 1) % self.capacity
        if self.count < self.capacity:
            self.count += 1

    def get(self):
        result = []
        for i in range(self.count):
            result.append(self.log[(self.index - self.count + i) % self.capacity])
        return result


class CompressionSystem:
    def __init__(self, history_size=10):
        self.time = 0
        self.workers = []
        self.pending_jobs = []
        self.retry_queue = deque()
        self.history = HistoryLog(history_size)
        self.jobs = {}

    def set_workers(self, w):
        self.workers = [None] * w
        print("Workers set to", w)

    def submit(self, file_id, size):
        job = Job(file_id, size, self.time)
        heapq.heappush(self.pending_jobs, job)
        self.jobs[file_id] = job
        print("Submitted", file_id)

    def cancel(self, file_id):
        if file_id not in self.jobs:
            print("Error: Job not found")
            return

        job = self.jobs[file_id]
        if job.status != "Pending":
            print("Error:", file_id, "is processing and cannot be cancelled")
            return

        self.pending_jobs = [j for j in self.pending_jobs if j.file_id != file_id]
        heapq.heapify(self.pending_jobs)

        job.status = "Cancelled"
        self.history.add(file_id)
        del self.jobs[file_id]

        print("Cancelled", file_id)

    def tick(self):
        print("\nTICK", self.time, "->", self.time + 1)

        for i in range(len(self.workers)):
            if self.workers[i] is None:
                if self.pending_jobs:
                    job = heapq.heappop(self.pending_jobs)
                elif self.retry_queue:
                    job = self.retry_queue.popleft()
                else:
                    continue

                job.status = "Processing"
                self.workers[i] = job
                print("Worker", i + 1, "picked", job.file_id)

        for i in range(len(self.workers)):
            job = self.workers[i]
            if job:
                job.remaining_time -= 1

                if job.remaining_time <= 0:
                    if job.fail:
                        job.status = "Pending"
                        job.remaining_time = job.size // 10
                        self.retry_queue.append(job)
                        print(job.file_id, "failed, moved to retry queue")
                    else:
                        job.status = "Completed"
                        self.history.add(job.file_id)
                        del self.jobs[job.file_id]
                        print(job.file_id, "completed")

                    self.workers[i] = None

        self.time += 1

    def status(self):
        print("\nSTATUS")
        print("Pending:", [j.file_id for j in self.pending_jobs])
        print("Workers:",
              [str(i + 1) + ":" + (w.file_id if w else "Idle")
               for i, w in enumerate(self.workers)])
        print("Retry:", [j.file_id for j in self.retry_queue])
        print("History:", self.history.get())


if __name__ == "__main__":
    system = CompressionSystem(history_size=5)

    system.set_workers(2)
    system.submit("F1", 50)
    system.submit("F2", 20)
    system.submit("F3", 10)

    system.tick()
    system.tick()

    system.cancel("F1")
    system.status()
