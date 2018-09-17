from tabu_search import TabuSearch
from airplane import Airplane
import copy
from datetime import datetime
import json
from operator import attrgetter


def log(message, end=None):
    print(message, flush=True, end=end)


if __name__ == '__main__':
    datasets = [
        {"name": "airland1.txt", "results": {}},
        {"name": "airland2.txt", "results": {}},
        {"name": "airland3.txt", "results": {}},
        {"name": "airland4.txt", "results": {}},
        {"name": "airland5.txt", "results": {}},
    ]

    # Loop through each data set.
    for dataset in datasets:
        # Read the data into memory
        with open('datasets/{}'.format(dataset["name"]), 'r') as file:
            line = file.readline().split()
            num_planes, freeze_time = int(line[0]), int(line[1])
            planes = []
            for idx in range(num_planes):
                params = file.readline().split()
                params = [int(x) for x in params[:-2]] + [float(params[-2]), float(params[-1])]
                separation_times = [int(x) for x in file.readline().split()]
                arrival_time, earliest_time, target_time, latest_time, early_penalty, late_penalty = params
                planes.append(Airplane(idx, arrival_time, earliest_time, target_time, latest_time, separation_times, early_penalty, late_penalty))
            log("\n\nDATASET {}: num_planes {} freeze_time {} items_read {}".format(dataset["name"], num_planes, freeze_time, len(planes)))
        planes = sorted(planes, key=attrgetter('arrival_time', 'earliest_time', 'latest_time'))
        for idx, p in enumerate(planes):
            log((p.plane_id, p.arrival_time, p.earliest_time, p.target_time, p.latest_time))
        log("  Iteration", end=" ")
        # Perform 30 independent iterations.
        for iteration in range(30):
            log(iteration+1, end=" ")
            thing = TabuSearch(copy.deepcopy(planes))

            initial_fitness = thing.fitness
            start_time = datetime.now()
            total_iterations, stagnation, combination = thing.run()
            execution_time = datetime.now() - start_time

            # Record the relevant data for analysis
            summary = {
                "execution_time": str(execution_time),
                "initial_fitness": initial_fitness,
                "fitness": thing.fitness,
                "iterations": total_iterations,
                "stagnation": stagnation,
                "combination": combination,
                "landing_times": ["{}: {}".format(p.plane_id, p.landing_time) for p in thing.planes],
            }
            dataset["results"].setdefault("TabuSearch", []).append(summary)
            # Write the captured data to disk.
            with open("results_tabu_search.json", "w") as file:
                file.write(json.dumps(datasets, indent=2))
