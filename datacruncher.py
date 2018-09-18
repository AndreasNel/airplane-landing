import json
import datetime
from scipy.stats import mannwhitneyu


if __name__ == '__main__':
    datasets = [
        {"name": "airland1", "optimum": 700, "results": {}},
        {"name": "airland2", "optimum": 1480, "results": {}},
        {"name": "airland3", "optimum": 820, "results": {}},
        {"name": "airland4", "optimum": 2520, "results": {}},
        {"name": "airland5", "optimum": 3100, "results": {}},
    ]

    final_results = {}
    with open("results_tabu_search.json", "r") as f:
        data = json.load(f)
    for dataset in datasets:
        summary = next(d for d in data if d["name"] == dataset["name"] + ".txt")["results"]
        for key, results in summary.items():
            stats = {
                "best_value": min(results, key=lambda x: x["fitness"])["fitness"],
                "avg_value": sum(x["fitness"] for x in results) / len(results),
            }
            stats["deviation"] = stats["best_value"] - dataset["optimum"]
            seconds = 0
            for obj in results:
                try:
                    execution_time = datetime.datetime.strptime(obj["execution_time"], "%H:%M:%S.%f")
                except Exception as ex:
                    execution_time = datetime.datetime.strptime(obj["execution_time"], "%H:%M:%S")
                delta = datetime.timedelta(hours=execution_time.hour, minutes=execution_time.minute, seconds=execution_time.second, microseconds=execution_time.microsecond)
                seconds += delta.total_seconds()
            stats["avg_execution_time"] = seconds / len(results)
            final_results.setdefault(key, {})[dataset["name"]] = stats

    data = final_results
    print(data)

    for algorithm_name, results in data.items():
        print(algorithm_name)
        data1 = [data["avg_value"] for data in results.values()]
        data2 = [data["optimum"] for data in datasets]
        stat, p = mannwhitneyu(data1, data2)
        print('Statistics=%.3f, p=%.3f' % (stat, p))
        # interpret
        alpha = 0.05
        if p > alpha:
            print('Same distribution (fail to reject H0)')
        else:
            print('Different distribution (reject H0)')
        print("=" * 200)
        for dataset, data in results.items():
            print(" & ".join([dataset.replace("_", "\_"), str(round(data["avg_execution_time"], 7)), str(round(data["avg_value"], 7)), str(round(data["best_value"], 7)), str(round(data["deviation"], 7))]) + "\\\\")
        print("=" * 200)
