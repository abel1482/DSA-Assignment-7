This project is a simple simulation of how a real database manages memory. Databases are huge, so they can’t keep all their data in RAM. Instead, they keep only a limited number of pages in memory. This limited space is called the buffer pool.

Because the buffer pool is small, the system must decide which page to remove when it becomes full. To make this decision, it uses a rule called Least Recently Used (LRU). This rule simply means: the page that hasn’t been used for the longest time is the first one to be removed.

Pages in the buffer pool can be in two conditions. A page is clean if it was only read and never changed. A page is dirty if it was written to or modified. This difference is important because dirty pages must be saved back to disk before they are removed from memory. Clean pages can be discarded immediately.

When a READ operation happens, the system checks if the page is already in memory. If it is, the page is marked as recently used. If it isn’t, the page is loaded into memory. Reading a page does not change its content, so the page remains clean.

When a WRITE operation happens, the page is also brought into memory if it isn’t already there. The page is marked as recently used, and it is marked dirty because its data has changed.

If the buffer pool is full and a new page needs to be added, the system removes the least recently used page. If that page is dirty, the system simulates saving it to disk by printing a message. If the page is clean, it is simply removed without saving.

To make all these operations fast, the system uses two main internal structures. One is a lookup table that allows the system to find pages instantly using their ID. The other is a list that keeps track of page usage order, with the most recently used pages at the front and the least recently used pages at the end.

The STATUS operation is used to display the current state of the buffer pool. Since it has to look at every page in memory, it is slower than read or write operations.

Overall, this project is not about real disk access or real databases. It is about understanding how databases manage limited memory efficiently while ensuring that modified data is not lost.