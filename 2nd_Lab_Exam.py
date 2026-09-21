class CPUScheduler:
    def __init__(self):
        pass

    def fcfs(self, n, processes, arrival_time, burst_time):
        """First-Come, First-Served (Non-Preemptive)"""
        # Sort processes based on arrival time
        combined = sorted(zip(processes, arrival_time, burst_time), key=lambda x: x[1])
        p, at, bt = zip(*combined)

        wt = [0] * n
        tat = [0] * n
        completion_time = [0] * n
        gantt_chart = []

        current_time = 0
        for i in range(n):
            if current_time < at[i]:
                current_time = at[i]  # CPU sits idle if process hasn't arrived
            
            start_time = current_time
            current_time += bt[i]
            completion_time[i] = current_time
            tat[i] = completion_time[i] - at[i]
            wt[i] = tat[i] - bt[i]
            
            gantt_chart.append((p[i], start_time, completion_time[i]))

        self._print_scheduling_results("FCFS (Non-Preemptive)", p, at, bt, wt, tat, gantt_chart)

    def round_robin(self, n, processes, arrival_time, burst_time, time_quantum):
        """Round Robin (Preemptive)"""
        rem_bt = list(burst_time)
        wt = [0] * n
        tat = [0] * n
        completion_time = [0] * n
        gantt_chart = []

        current_time = 0
        completed = 0
        queue = []
        visited = [False] * n

        # Sort by arrival time initially
        processes_data = sorted(zip(processes, arrival_time, burst_time, range(n)), key=lambda x: x[1])
        
        while completed < n:
            # Add newly arrived processes to the queue
            for p_name, at, bt, idx in processes_data:
                if at <= current_time and not visited[idx] and rem_bt[idx] > 0:
                    queue.append(idx)
                    visited[idx] = True

            if not queue:
                # If CPU is idle, advance time to the next arriving process
                current_time += 1
                continue

            idx = queue.pop(0)
            p_name = processes_data[idx][0]
            at = processes_data[idx][1]

            start_time = current_time
            if rem_bt[idx] > time_quantum:
                current_time += time_quantum
                rem_bt[idx] -= time_quantum
                gantt_chart.append((p_name, start_time, current_time))
            else:
                current_time += rem_bt[idx]
                rem_bt[idx] = 0
                completion_time[idx] = current_time
                tat[idx] = completion_time[idx] - at
                wt[idx] = tat[idx] - burst_time[idx]
                completed += 1
                gantt_chart.append((p_name, start_time, current_time))

            # Check for newly arrived processes during the execution slice
            for p_name_inner, at_inner, bt_inner, idx_inner in processes_data:
                if at_inner <= current_time and not visited[idx_inner] and rem_bt[idx_inner] > 0:
                    queue.append(idx_inner)
                    visited[idx_inner] = True

            # If the current process still needs time, push it back to the queue
            if rem_bt[idx] > 0:
                queue.append(idx)

        # Reorder outputs to match original process index order
        orig_wt = [0] * n
        orig_tat = [0] * n
        for p_name, at, bt, idx in processes_data:
            orig_wt[idx] = wt[idx]
            orig_tat[idx] = tat[idx]

        self._print_scheduling_results("Round Robin (Preemptive)", processes, arrival_time, burst_time, orig_wt, orig_tat, gantt_chart)

    def _print_scheduling_results(self, algo_name, processes, at, bt, wt, tat, gantt):
        print(f"\n--- {algo_name} Results ---")
        print(f"{'Process':<10}{'Arrival':<10}{'Burst':<10}{'Waiting':<10}{'Turnaround':<10}")
        for i in range(len(processes)):
            print(f"{str(processes[i]):<10}{at[i]:<10}{bt[i]:<10}{wt[i]:<10}{tat[i]:<10}")
        
        print(f"\nAverage Waiting Time: {sum(wt)/len(wt):.2f}")
        print(f"Average Turnaround Time: {sum(tat)/len(tat):.2f}")

        # Gantt Chart Display
        print("\nGantt Chart:")
        timeline = " | ".join([f"{item[0]} ({item[1]}-{item[2]})" for item in gantt])
        print(f"| {timeline} |")


def bankers_algorithm():
    print("\n--- Banker's Algorithm Simulation ---")
    n = int(input("Enter number of processes: "))
    m = int(input("Enter number of resource types: "))

    print("Enter Allocation Matrix (row by row, space-separated):")
    allocation = []
    for i in range(n):
        allocation.append(list(map(int, input(f"Process {i}: ").split())))

    print("Enter Max Matrix (row by row, space-separated):")
    max_matrix = []
    for i in range(n):
        max_matrix.append(list(map(int, input(f"Process {i}: ").split())))

    available = list(map(int, input("Enter Available Resources (space-separated): ").split()))

    # Calculate Need Matrix
    need = [[max_matrix[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]

    # Print Need Matrix to match professor's formatting
    print("\nNeed Matrix:")
    for i in range(n):
        print(f"P{i}: {need[i]}")
    print() # Adds the blank line before the final result

    finish = [False] * n
    safe_sequence = []
    work = list(available)

    while len(safe_sequence) < n:
        found = False
        for i in range(n):
            if not finish[i]:
                # Check if need of process <= work
                if all(need[i][j] <= work[j] for j in range(m)):
                    for j in range(m):
                        work[j] += allocation[i][j]
                    safe_sequence.append(f"P{i}")
                    finish[i] = True
                    found = True
                    break
        if not found:
            break

    # Adjusted capitalization and spacing to match the screenshot perfectly
    if len(safe_sequence) == n:
        print("System is in a Safe State.")
        print(f"Safe Sequence: {' -> '.join(safe_sequence)}")
    else:
        print("System is in an Unsafe State.")


def main():
    scheduler = CPUScheduler()
    
    while True:
        print("\n==============================")
        print(" OPERATING SYSTEM SIMULATOR ")
        print("==============================")
        print("1. FCFS Scheduling (Non-Preemptive)")
        print("2. Round Robin Scheduling (Preemptive)")
        print("3. Banker's Algorithm")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ")
        
        if choice == '1' or choice == '2':
            n = int(input("Enter number of processes: "))
            processes = [f"P{i}" for i in range(n)]
            arrival_time = list(map(int, input("Enter Arrival Times (space-separated): ").split()))
            burst_time = list(map(int, input("Enter Burst Times (space-separated): ").split()))
            
            if choice == '1':
                scheduler.fcfs(n, processes, arrival_time, burst_time)
            elif choice == '2':
                time_quantum = int(input("Enter Time Quantum: "))
                scheduler.round_robin(n, processes, arrival_time, burst_time, time_quantum)
                
        elif choice == '3':
            bankers_algorithm()
        elif choice == '4':
            print("Exiting simulator. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()