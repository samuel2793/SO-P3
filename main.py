class Process:
    def __init__(self, name, arrival_time, memory_required, execution_time):
        self.name = name
        self.arrival_time = arrival_time
        self.memory_required = memory_required
        self.execution_time = execution_time
        self.end_time = arrival_time + execution_time

class MemoryPartition:
    def __init__(self, start, size, process=None):
        self.start = start
        self.size = size
        self.process = process

    def __str__(self):
        if self.process:
            return f"[{self.start} {self.process.name} {self.size}]"
        else:
            return f"[{self.start} Libre {self.size}]"

class MemoryManager:
    def __init__(self, total_memory=2000):
        self.total_memory = total_memory
        self.partitions = [MemoryPartition(0, total_memory)]
        self.last_assigned_partition = 0

    def first_fit(self, process):
        for partition in self.partitions:
            if not partition.process and partition.size >= process.memory_required:
                return partition
        return None

    def next_fit(self, process):
        for i in range(self.last_assigned_partition, len(self.partitions)):
            if not self.partitions[i].process and self.partitions[i].size >= process.memory_required:
                self.last_assigned_partition = i
                return self.partitions[i]
        for i in range(0, self.last_assigned_partition):
            if not self.partitions[i].process and self.partitions[i].size >= process.memory_required:
                self.last_assigned_partition = i
                return self.partitions[i]
        return None

    def allocate_memory(self, process, allocation_algorithm):
        partition = self.first_fit(process) if allocation_algorithm == 'first_fit' else self.next_fit(process)

        if partition:
            if partition.size > process.memory_required:
                new_partition = MemoryPartition(partition.start + process.memory_required,
                                                partition.size - process.memory_required)
                self.partitions.insert(self.partitions.index(partition) + 1, new_partition)
            partition.size = process.memory_required
            partition.process = process

    def free_memory(self, current_time):
        for partition in self.partitions:
            if partition.process and partition.process.end_time <= current_time:
                partition.process = None

    def merge_free_partitions(self):
        i = 0
        while i < len(self.partitions) - 1:
            current = self.partitions[i]
            next_partition = self.partitions[i + 1]
            if current.process is None and next_partition.process is None:
                current.size += next_partition.size
                del self.partitions[i + 1]
            else:
                i += 1

    def run_simulation(self, processes, allocation_algorithm):
        current_time = 0
        memory_states = []
        for process in sorted(processes, key=lambda x: x.arrival_time):
            while current_time < process.arrival_time:
                self.free_memory(current_time)
                self.merge_free_partitions()
                memory_states.append(self.get_memory_state(current_time))
                current_time += 1

            self.free_memory(current_time)
            self.merge_free_partitions()
            self.allocate_memory(process, allocation_algorithm)
            memory_states.append(self.get_memory_state(current_time))
            current_time += 1

        # Free all remaining processes and merge partitions
        while any(p.process for p in self.partitions):
            self.free_memory(current_time)
            self.merge_free_partitions()
            memory_states.append(self.get_memory_state(current_time))
            current_time += 1

        return memory_states

    def get_memory_state(self, current_time):
        state = f"{current_time} " + " ".join(str(partition) for partition in self.partitions)
        return state

def read_input_file(file_path):
    processes = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            parts = line.split()
            if parts[0] != '<Proceso>':  # Skip the header or any other non-data lines
                name, arrival_time, memory_required, execution_time = parts
                processes.append(Process(name, int(arrival_time), int(memory_required), int(execution_time)))
    return processes

def write_output_file(file_path, memory_states):
    with open(file_path, 'w') as file:
        for state in memory_states:
            file.write(state + '\n')

def main(input_file, output_file, allocation_algorithm):
    processes = read_input_file(input_file)
    memory_manager = MemoryManager()
    memory_states = memory_manager.run_simulation(processes, allocation_algorithm)
    write_output_file(output_file, memory_states)

# Assuming the input file is named 'entrada.txt' and the output file is 'particiones.txt'
# The path should be adjusted to the actual input file location
input_file_path = 'entrada.txt'
output_file_path = 'particiones.txt'
allocation_algorithm = 'first_fit'  # or 'next_fit'

# Call the main function with the input file, output file, and the allocation algorithm
main(input_file_path, output_file_path, allocation_algorithm)
