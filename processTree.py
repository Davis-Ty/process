import multiprocessing
import random

# Number of random integers to make
array_size = 1000

# make array of random integers that between 1 and 1 (can be changed)
array = [random.randint(1, 1) for i in range(array_size)]

# (Function) for slave processes to sum a range of values in the array
def sum_range(start, end):
    return sum(array[start:end])

# (Function) for slave processes to spawn new processes and sum half segment of the array
def spawn_processes(start, end, parent_conn, results):
    #get mid-point of segment
    mid = (start + end) // 2
    # sums up the array if it is smaller than 101
    if end - start <= 100:
        result = sum_range(start, end)
        parent_conn.send(result)
        return
    
    
    # Spawn two new processes to sum the two halves of the segment if its bigger than 100
    left_child_conn, right_child_conn = multiprocessing.Pipe()
    left_child = multiprocessing.Process(target=spawn_processes, args=(start, mid, left_child_conn, results))
    right_child = multiprocessing.Process(target=spawn_processes, args=(mid, end, right_child_conn, results))
    left_child.start()
    right_child.start()
    # Wait for both child processes to finish to keep code clean
    left_child.join()
    right_child.join()
    # Adds the total of left and right child and store result in parent process
    parent_result = left_child_conn.recv() + right_child_conn.recv()
    parent_conn.send(parent_result)

    #must print after the blocks above to avoid messy print out
    print("Child L: ",results[left_child.pid],"Child R: ",results[right_child.pid])
    print("Parent: ",parent_result)



# (Function) to create master process
def master():
    # Create master process and pass it the entire array segment to sum
    results = {}
    parent_conn, child_conn = multiprocessing.Pipe()
    master_process = multiprocessing.Process(target=spawn_processes, args=(0, array_size, child_conn, results))
    return master_process, parent_conn, results

# Create master process
master_process, parent_conn, results = master()

# Start master process
master_process.start()

# Wait for master process to finish
master_process.join()

# Get result from master process
result = parent_conn.recv()

# results
print("The sum of the array is:", result)