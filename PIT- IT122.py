def is_empty(queue):
    return len(queue) == 0

def is_full(queue, capacity):
    return len(queue) >= capacity

def enqueue(queue, capacity):
    if is_full(queue, capacity):
        print("Queue is full. Cannot add more customers.")
    else:
        customer = input("Enter customer name to add: ")
        queue.append(customer)
        print(f"{customer} has entered the queue.")

def dequeue(queue):
    if is_empty(queue):
        print("No customers in queue to serve.")
    else:
        served = queue.pop(0)
        print(f"{served} has been served and removed from the queue.")5

def peek(queue):
    if is_empty(queue):
        print("No customers to peek at.")
    else:
        print(f"Next customer to be served: {queue[0]}")

def display(queue):
    if is_empty(queue):
        print("The queue is currently empty.")
    else:
        print("Current queue: " + " -> ".join(queue))

def main():
    capacity = int(input("Enter maximum capacity of the queue: "))
    queue = []
    
    while True:
        print("\n--- Customer Service Queue Menu ---")
        print("1. Add customer to queue (Enqueue)")
        print("2. Serve customer (Dequeue)")
        print("3. View next customer (Peek)")
        print("4. Display queue")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == '1':
            enqueue(queue, capacity)
        elif choice == '2':
            dequeue(queue)
        elif choice == '3':
            peek(queue)
        elif choice == '4':
            display(queue)
        elif choice == '5':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a number from 1 to 5.")

if __name__ =="__main__":
    main()
