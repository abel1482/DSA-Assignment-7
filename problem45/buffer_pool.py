
class PageNode:
    def __init__(self, page_id, data=None):
        self.page_id = page_id
        self.data = data
        self.is_dirty = False
        self.prev = None
        self.next = None



class BufferPool:
    def __init__(self):
        self.capacity = 0
        self.pages = {}      # Hash map: page_id -> PageNode
        self.head = None     # MRU
        self.tail = None     # LRU

    def init(self, n):
        self.capacity = n
        self.pages.clear()
        self.head = None
        self.tail = None
        print(f"Buffer pool initialized with size {n}")

    def _move_to_front(self, node):
        if node == self.head:
            return

        # Remove node
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev

        if node == self.tail:
            self.tail = node.prev

        # Insert at front
        node.prev = None
        node.next = self.head
        if self.head:
            self.head.prev = node
        self.head = node

        if not self.tail:
            self.tail = node

    def _evict(self):
        if not self.tail:
            return

        node = self.tail
        if node.is_dirty:
            print(f"Evicting {node.page_id} (Dirty). FLUSHING {node.page_id} TO DISK... Dropped.")
        else:
            print(f"Evicting {node.page_id} (Clean). Dropped.")

        del self.pages[node.page_id]

        if node.prev:
            node.prev.next = None
        self.tail = node.prev

        if self.tail is None:
            self.head = None

    def read(self, page_id):
        if page_id in self.pages:
            node = self.pages[page_id]
            self._move_to_front(node)
        else:
            if len(self.pages) >= self.capacity:
                self._evict()

            node = PageNode(page_id)
            self.pages[page_id] = node
            self._move_to_front(node)

        print(f"READ {page_id}")
        self.status()

    def write(self, page_id, data):
        if page_id in self.pages:
            node = self.pages[page_id]
        else:
            if len(self.pages) >= self.capacity:
                self._evict()

            node = PageNode(page_id)
            self.pages[page_id] = node

        node.data = data
        node.is_dirty = True
        self._move_to_front(node)

        print(f'WRITE {page_id} "{data}"')
        self.status()

 
    def status(self):
        result = []
        curr = self.head
        while curr:
            state = "dirty" if curr.is_dirty else "clean"
            result.append(f"{curr.page_id}({state})")
            curr = curr.next

        print("Pool:", "[" + ", ".join(result) + "]")



if __name__ == "__main__":
    pool = BufferPool()

    pool.init(2)
    pool.read("P1")
    pool.write("P2", "Data")
    pool.read("P3")
    pool.read("P4")
