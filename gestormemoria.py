import sys
import re

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
        if allocation_algorithm == 'first_fit':
            partition = self.first_fit(process)
        elif allocation_algorithm == 'next_fit':
            partition = self.next_fit(process)
        else:
            raise ValueError("Unknown allocation algorithm")

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
        visual_representations = [] 
        for process in sorted(processes, key=lambda x: x.arrival_time):
            while current_time < process.arrival_time:
                self.free_memory(current_time)
                self.merge_free_partitions()
                if any(partition.process for partition in self.partitions):
                    state, visual_representation = self.get_memory_state(current_time)
                    memory_states.append(state)
                    visual_representations.append(visual_representation)
                current_time += 1

            self.free_memory(current_time)
            self.merge_free_partitions()
            self.allocate_memory(process, allocation_algorithm)
            state, visual_representation = self.get_memory_state(current_time)
            memory_states.append(state)
            visual_representations.append(visual_representation)
            current_time += 1

        while any(p.process for p in self.partitions):
            self.free_memory(current_time)
            self.merge_free_partitions()
            state, visual_representation = self.get_memory_state(current_time)
            memory_states.append(state)
            visual_representations.append(visual_representation)
            current_time += 1

        return memory_states, visual_representations

    def get_memory_state(self, current_time):
        line_length = 40 
        visual_representation = "*" * line_length + "\n"
        for partition in self.partitions:
            if partition.process:
                process_number = re.search(r'\d+', partition.process.name)
                block = f"P{process_number.group()}" if process_number else "P"
            else:
                block = "L"
            size_str = f"({partition.size})"
            partition_info = f"{block} {size_str}"
            centered_partition_info = partition_info.center(line_length - 2)
            line = f"*{centered_partition_info}*"
            visual_representation += line + "\n"
        visual_representation += "*" * line_length
        state = f"{current_time} " + " ".join(str(partition) for partition in self.partitions)
        return state, visual_representation


def read_input_file(file_path):
    processes = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            parts = line.split()
            if parts[0] != '<Proceso>':
                name, arrival_time, memory_required, execution_time = parts
                processes.append(Process(name, int(arrival_time), int(memory_required), int(execution_time)))
    return processes

def write_output_file(file_path, memory_states):
    with open(file_path, 'w') as file:
        for state in memory_states:
            file.write(state + '\n')

def main(input_file, output_file):
    processes = read_input_file(input_file)
    memory_manager = MemoryManager()

    print("Elige el algoritmo de asignación de memoria:")
    print("1. Primer Hueco (First Fit)")
    print("2. Siguiente Hueco (Next Fit)")
    choice = input("Introduce el número del algoritmo: ")

    if choice == '1':
        allocation_algorithm = 'first_fit'
    elif choice == '2':
        allocation_algorithm = 'next_fit'
    else:
        print("Selección inválida. Usando Primer Hueco por defecto.")
        allocation_algorithm = 'first_fit'

    memory_states, visual_representations = memory_manager.run_simulation(processes, allocation_algorithm)
    write_output_file(output_file, memory_states)

    for visual_representation in visual_representations:
        print(visual_representation)
        print()

# Ejecución python gestormemoria.py entrada.txt particiones.txt

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python script.py <archivo_entrada> <archivo_salida>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    main(input_file_path, output_file_path)
