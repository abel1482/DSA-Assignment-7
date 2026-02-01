class ExamPlatform {
    constructor() {
        this.deadline = null;
        this.heap = [];    
        this.queue = [];     
        this.currentTime = 0;
    }

    setDeadline(timestamp) {
        this.deadline = parseInt(timestamp);
        console.log(`Deadline set to: ${this.deadline}`);
    }

    submit(student, estTime, timestamp) {
        timestamp = parseInt(timestamp);
        if (!this.deadline) return console.log("Error: No deadline set");
        if (timestamp > this.deadline) return console.log("Error: Past deadline");
        this.currentTime = Math.max(this.currentTime, timestamp);
        this.heap.push({
            student,
            estTime: parseInt(estTime),
            timestamp,
            submittedAt: timestamp
        });
        this.heap.sort((a, b) => a.estTime - b.estTime);
        
        console.log(`Accepted: ${student} (${estTime}ms)`);
    }
    process() {
        const now = ++this.currentTime;
        
        this.heap = this.heap.filter(job => {
            const waitTime = now - job.submittedAt;
            if (waitTime > 5) {
                this.queue.push(job);
                console.log(`Moved to starvation: ${job.student} (waited ${waitTime})`);
                return false;
            }
            return true;
        });
        let job = this.queue.shift() || this.heap.shift();
        
        if (job) {
            console.log(`Grading: ${job.student}`);
        } else {
            console.log("No submissions to grade");
        }
    }

    status() {
        console.log("\n=== STATUS ===");
        console.log(`Time: ${this.currentTime}, Deadline: ${this.deadline || "Not set"}`);
        console.log(`Starvation Queue: ${this.queue.map(s => s.student).join(', ') || 'Empty'}`);
        console.log(`Shortest-Job Queue: ${this.heap.map(s => `${s.student}(${s.estTime})`).join(', ') || 'Empty'}`);
        console.log("=============\n");
    }
}

// Test the system
const platform = new ExamPlatform();

// Example from problem
platform.setDeadline(100);
platform.submit("S1", 500, 10);  // Long job
platform.submit("S2", 10, 11);   // Short job
platform.process();               // Grades S2 (shortest)
platform.submit("S3", 5, 101);   // Rejected - past deadline
platform.status();

// Starvation test
platform.submit("S4", 100, 15);
platform.submit("S5", 1, 16);    // Very short
for (let i = 0; i < 7; i++) {
    platform.process();           // S4 will starve after 5 waits
}