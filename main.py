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

    def best_fit(self, process):
        suitable_partition = None
        for partition in self.partitions:
            if not partition.process and partition.size >= process.memory_required:
                if suitable_partition is None or partition.size < suitable_partition.size:
                    suitable_partition = partition
        return suitable_partition

    def worst_fit(self, process):
        largest_partition = None
        for partition in self.partitions:
            if not partition.process and partition.size >= process.memory_required:
                if largest_partition is None or partition.size > largest_partition.size:
                    largest_partition = partition
        return largest_partition

    def allocate_memory(self, process, allocation_algorithm):
        if allocation_algorithm == 'best_fit':
            partition = self.best_fit(process)
        elif allocation_algorithm == 'worst_fit':
            partition = self.worst_fit(process)
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
        visual_representations = []  # Almacenar las representaciones visuales
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

        # Free all remaining processes and merge partitions
        while any(p.process for p in self.partitions):
            self.free_memory(current_time)
            self.merge_free_partitions()
            state, visual_representation = self.get_memory_state(current_time)
            memory_states.append(state)
            visual_representations.append(visual_representation)
            current_time += 1

        return memory_states, visual_representations

    def get_memory_state(self, current_time):
        line_length = 40  # Define la longitud total de cada línea
        visual_representation = "*" * line_length + "\n"
        for partition in self.partitions:
            block = "P" if partition.process else "L"
            size_str = f"({partition.size})"
            line = f"* {block} {size_str}".ljust(line_length - 1) + "*"  # Alinea a la izquierda y añade asterisco al final
            visual_representation += line + "\n"
        visual_representation += "*" * line_length
        state = f"{current_time} " + " ".join(str(partition) for partition in self.partitions)
        return state, visual_representation

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

def main(input_file, output_file):
    processes = read_input_file(input_file)
    memory_manager = MemoryManager()

    print("Elige el algoritmo de asignación de memoria:")
    print("1. Mejor Hueco (Best Fit)")
    print("2. Peor Hueco (Worst Fit)")
    choice = input("Introduce el número del algoritmo: ")

    if choice == '1':
        allocation_algorithm = 'best_fit'
    elif choice == '2':
        allocation_algorithm = 'worst_fit'
    else:
        print("Selección inválida. Usando Mejor Hueco por defecto.")
        allocation_algorithm = 'best_fit'

    memory_states, visual_representations = memory_manager.run_simulation(processes, allocation_algorithm)
    write_output_file(output_file, memory_states)

    # Imprimir la representación visual
    for visual_representation in visual_representations:
        print(visual_representation)
        print()  # Agregar espacio entre cada estado de memoria

# Ajusta las rutas de los archivos según sea necesario
input_file_path = 'entrada.txt'
output_file_path = 'particiones.txt'

main(input_file_path, output_file_path)
