import time
from ortools.linear_solver import pywraplp

print("Script 132")
"calculate volume, calculate and pring 3D positioning summary"
"print volume calculation summary"

def read_box_data(filename):
    """Read box data from a file."""
    box_data = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 4:
                l, w, h, q = map(int, parts)
                box_data.append((l, w, h, q))
    return box_data

def calculate_maximum_packing(box_data, container_volume):
    start_time = time.time()  # Start the timing for execution

    # Create solver
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        print("Could not create solver.")
        return None

    # Variables for each type of box
    x = [solver.IntVar(0, q, f'x[{i}]') for i, (_, _, _, q) in enumerate(box_data)]

    # Total volume constraint
    total_volume = sum((l * w * h) * x[i] for i, (l, w, h, q) in enumerate(box_data))
    solver.Add(total_volume <= container_volume)

    # Objective: maximize the number of items packed.
    solver.Maximize(solver.Sum(x))

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        results = [int(x[i].solution_value()) for i in range(len(x))]
        total_items = sum(results)
        total_packed_volume = sum((l * w * h) * results[i] for i, (l, w, h, _) in enumerate(box_data))
        volume_occupancy_percentage = (total_packed_volume / container_volume) * 100
        
        execution_time = time.time() - start_time  # Calculate execution time

        print(f"Total items packed: {total_items}")
        for i, qty in enumerate(results):
            print(f"Items from category {i} packed: {qty}")
        print(f"Total volume packed: {total_packed_volume}")
        print(f"Volume occupancy percentage: {volume_occupancy_percentage:.2f}%")
        print(f"Execution time: {execution_time:.3f} seconds")  # Print execution time

        return results
    else:
        execution_time = time.time() - start_time  # Calculate execution time if not optimal
        print(f"Execution time: {execution_time:.3f} seconds")  # Print execution time

    return None

def fit_box(container_dims, box_dims, occupied_positions):
    start_time = time. time();
    """Attempt to place the box in the first available position in the container."""
    for x in range(0, container_dims[0] - box_dims[0] + 1, box_dims[0]):
        for y in range(0, container_dims[1] - box_dims[1] + 1, box_dims[1]):
            for z in range(0, container_dims[2] - box_dims[2] + 1, box_dims[2]):
                new_pos = (x, y, z)
                if can_place_box(new_pos, box_dims, occupied_positions, container_dims):
                    """execution_time = time.time() - start_time
                    with open("Output.txt", "w") as text_file:
                        #text_file.write(new_pos, box_dims)
                        #text_file.write(execution_time)
                        print(new_pos, box_dims, file=text_file)
                        print(f"Execution time: {execution_time:.2f} seconds", file=text_file)"""
                    #print(box_dims)
                    return new_pos
    return None

def can_place_box(position, box_dims, occupied_positions, container_dims):
    (x, y, z) = position
    (bx, by, bz) = box_dims
    if x + bx > container_dims[0] or y + by > container_dims[1] or z + bz > container_dims[2]:
        return False
    for pos, dims in occupied_positions.items():
        if not (x >= pos[0] + dims[0] or x + bx <= pos[0] or
                y >= pos[1] + dims[1] or y + by <= pos[1] or
                z >= pos[2] + dims[2] or z + bz <= pos[2]):
            return False
    return True

def main():
    start_time = time.time()
    container_dims = (1180, 230, 265)  # Container dimensions

    filename = "data_sets/ds7.txt"
    box_data = read_box_data(filename)
    if box_data:
        print("Box data loaded successfully:")
        for data in box_data:
            print(data)
    else:
        print("No box data loaded.")

    container_volume = container_dims[0] * container_dims[1] * container_dims[2]
    max_packing = calculate_maximum_packing(box_data, container_volume)

    occupied_positions = {}
    box_type_counts = [0] * len(box_data)
    total_volume = 0

    for index, (l, w, h, _) in enumerate(box_data):
        box_dims = (l, w, h)
        quantity_to_place = max_packing[index] if max_packing else 0
        for _ in range(quantity_to_place):
            position = fit_box(container_dims, box_dims, occupied_positions)
            if position:
                occupied_positions[position] = box_dims
                box_type_counts[index] += 1
                total_volume += l * w * h
                #print(f"Box {box_dims} placed at {position}")
            #else:
                #print(f"Failed to place box {box_dims}")

    volume_occupancy_rate = (total_volume / container_volume) * 100
    execution_time = time.time() - start_time
    print("\nSummary:")
    print(f"Total number of items packed: {sum(box_type_counts)}")
    for i, count in enumerate(box_type_counts):
        print(f"Items of type {i} packed: {count}")
    print(f"Total volume of items packed: {total_volume}")
    print(f"Volume occupancy rate: {volume_occupancy_rate:.2f}%")
    print(f"Execution time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    main()
