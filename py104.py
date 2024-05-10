from ortools.linear_solver import pywraplp

print("Script 104")

def create_data_model():
    """Create the data for the example."""
    data = {}
    # Box dimensions: length, width, height, and quantity from ds1
    box_data = [
        (58, 58, 58, 150),
        (92, 50, 30, 100),
        (120, 80, 60, 50),
        (30, 30, 45, 200),
        (75, 75, 100, 25),
    ]
    # Container dimensions from c001
    container_dimensions = (1180, 230, 265)
    
    # Calculate the volumes of the boxes and the container
    data['volumes'] = [l * w * h for l, w, h, _ in box_data]
    data['quantities'] = [q for _, _, _, q in box_data]
    container_volume = container_dimensions[0] * container_dimensions[1] * container_dimensions[2]

    # Flatten the items list to account for multiple quantities
    data['items'] = []
    data['item_types'] = []
    for i, q in enumerate(data['quantities']):
        data['items'].extend([i] * q)
        data['item_types'].append(i)
    data['bins'] = [0]  # Only one container in this case
    data['bin_capacity'] = container_volume
    return data

def main():
    data = create_data_model()

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SCIP")

    if not solver:
        return

    # Variables
    # x[i] = 1 if item i is packed in the container.
    x = {}
    for i in data['items']:
        x[i] = solver.IntVar(0, 1, 'x[%i]' % i)

    # Constraints
    # The total volume of items packed cannot exceed the container's capacity.
    solver.Add(
        sum(x[i] * data['volumes'][data['item_types'][i]] for i in data['items']) <= data['bin_capacity']
    )

    # Each type of item can only be packed up to its available quantity.
    for j in data['item_types']:
        solver.Add(
            sum(x[i] for i in data['items'] if data['item_types'][i] == j) <= data['quantities'][j]
        )

    # Objective: maximize the total number of items packed.
    solver.Maximize(solver.Sum([x[i] for i in data['items']]))

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        total_items_packed = sum(x[i].solution_value() for i in data['items'])
        total_volume_packed = sum(x[i].solution_value() * data['volumes'][data['item_types'][i]] for i in data['items'])
        volume_occupancy_rate = (total_volume_packed / data['bin_capacity']) * 100
        print("\nContainer c001")
        print("Total number of items packed:", total_items_packed)
        for j in set(data['item_types']):  # Set to remove duplicates
            items_packed_of_type = sum(x[i].solution_value() for i in data['items'] if data['item_types'][i] == j)
            print(f"Items of type {j} packed: {items_packed_of_type}")
        print(f"Total volume of items packed: {total_volume_packed}")
        print(f"Volume occupancy rate: {volume_occupancy_rate:.2f}%")
        print(f"Time = {solver.WallTime()} milliseconds")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == "__main__":
    main()
