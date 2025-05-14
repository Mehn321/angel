class QueueArray:
    def __init__(self, capacity):
        self.queue = [None] * capacity
        self.front = self.rear = -1
        self.capacity = capacity

    def is_empty(self):
        return self.front == -1

    def is_full(self):
        return self.rear == self.capacity - 1

    def enqueue(self, item):
        if self.is_full():
            print("Queue is full")
            return

        if self.front == -1:
            self.front = 0
        else:
            self.rear += 1

        self.queue[self.rear] = item

    def dequeue(self):
        if self.is_empty():
            print("Queue is empty")
            return

        item = self.queue[self.front]
        self.queue[self.front] = None

        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front += 1

        return item


# Create a queue with capacity of 5
my_queue = QueueArray(5)

# Add elements to the queue
my_queue.enqueue(10)
my_queue.enqueue(20)
my_queue.enqueue(30)
my_queue.enqueue(40)
my_queue.enqueue(50)

# Try to add one more element (should print "Queue is full")
my_queue.enqueue(60)

# Remove and print elements from the queue
print(my_queue.dequeue())  # Should print: 10
print(my_queue.dequeue())  # Should print: 20
print(my_queue.dequeue())  # Should print: 30

# Add a new element after removing some
my_queue.enqueue(70)

# Print the remaining elements
while not my_queue.is_empty():
    print(my_queue.dequeue())  # Should print: 40, 50, 70v