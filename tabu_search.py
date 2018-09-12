from airplane import Airplane
import heuristics
import move_operators
import copy
import random


class TabuSearch:
    MAX_COMBINATION_LENGTH = 10
    MAX_ITERATIONS = 5000
    MAX_NO_CHANGE = 1000

    def __init__(self, planes):
        """
        Creates an instance that can run the tabu search algorithm.
        :param planes: The initial solution to the problem.
        """
        self.planes = planes
        self.fitness = 0
        self.tabu_list = set()

    def run(self):
        """
        Runs the tabu search algorithm and returns the results at the end of the process.
        :return: (num_iterations, num_no_changes, chosen_combination)
        """
        # TODO generate a new base combination each time the solution is improved
        combination = "".join(
            [random.choice(list(heuristics.HEURISTIC_MAP.keys())) for _ in range(random.randrange(self.MAX_COMBINATION_LENGTH) or 1)])
        self.fitness = sum(p.fitness() for p in self.planes)
        self.tabu_list.add(combination)
        current_iteration = 0
        num_no_change = 0
        while num_no_change < self.MAX_NO_CHANGE and current_iteration < self.MAX_ITERATIONS:
            new_combination = self.apply_move_operator(combination)
            if new_combination not in self.tabu_list:
                self.tabu_list.add(new_combination)
                solution = self.generate_solution(new_combination)
                fitness = sum(p.fitness() for p in solution)
                if fitness > self.fitness:
                    self.planes = solution
                    self.fitness = fitness
                    num_no_change = 0
                    combination = new_combination
            current_iteration += 1
            num_no_change += 1
        return current_iteration, num_no_change, combination

    def generate_solution(self, pattern):
        """
        Generates a candidate solution based on the pattern given.
        :param pattern: A pattern indicating the order in which heuristics need to be applied to get the solution.
        :return: A list of bins to serve as a solution.
        """
        solution = copy.deepcopy(self.planes)
        pattern_length = len(pattern)
        for idx, plane in enumerate(solution):
            h = pattern[idx % pattern_length]
            original_landing_time = plane.landing_time
            try:
                heuristics.HEURISTIC_MAP[h](plane, solution)
            #     TODO sort the solution and determine whether it is valid
            except:
                plane.landing_time = original_landing_time
        return sorted(solution, key=lambda p: p.landing_time)

    def apply_move_operator(self, pattern):
        """
        Applies a random move operator to the given pattern.
        :param pattern: The pattern to apply the move operator to.
        :return: The pattern after the move operator has been applied.
        """
        return random.choice(list(move_operators.MOVE_OP_MAP.values()))(pattern, list(heuristics.HEURISTIC_MAP.keys()))
