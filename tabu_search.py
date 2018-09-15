from airplane import Airplane
import heuristics
import move_operators
import copy
import random


class TabuSearch:
    MAX_COMBINATION_LENGTH = 10
    MAX_ITERATIONS = 5000
    MAX_NO_CHANGE = 5000

    def __init__(self, planes):
        """
        Creates an instance that can run the tabu search algorithm.
        :param planes: The initial solution to the problem.
        """
        self.planes = planes
        for idx in range(1, len(planes)):
            self.planes[idx].landing_time = max(random.randint(self.planes[idx].earliest_time, self.planes[idx].latest_time), self.planes[idx - 1].next_available_time(self.planes[idx].plane_id))
        self.fitness = sum(p.fitness() for p in self.planes)
        self.tabu_list = set()

    def run(self):
        """
        Runs the tabu search algorithm and returns the results at the end of the process.
        :return: (num_iterations, num_no_changes, chosen_combination)
        """
        combination = self.generate_combination()
        self.fitness = sum(p.fitness() for p in self.planes)
        self.tabu_list.add(combination)
        current_iteration = 0
        num_no_change = 0
        while num_no_change < self.MAX_NO_CHANGE and current_iteration < self.MAX_ITERATIONS:
            new_combination = self.apply_move_operator(combination)[:len(self.planes)]
            if new_combination not in self.tabu_list:
                self.tabu_list.add(new_combination)
                solution = self.generate_solution(new_combination)
                fitness = sum(p.fitness() for p in solution)
                if fitness < self.fitness:
                    self.planes = solution
                    self.fitness = fitness
                    num_no_change = 0
                    combination = self.generate_combination()
            current_iteration += 1
            num_no_change += 1
        return current_iteration, num_no_change, combination

    def generate_combination(self):
        return "".join(
            [random.choice(list(heuristics.HEURISTIC_MAP.keys())) for _ in
             range(random.randrange(self.MAX_COMBINATION_LENGTH) or 1)])

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
            original_time = plane.landing_time
            try:
                heuristics.HEURISTIC_MAP[h](plane)
            except:
                plane.landing_time = original_time
        return sorted(solution, key=lambda p: p.landing_time) if self.is_valid(solution) else self.planes

    @staticmethod
    def apply_move_operator(pattern):
        """
        Applies a random move operator to the given pattern.
        :param pattern: The pattern to apply the move operator to.
        :return: The pattern after the move operator has been applied.
        """
        return random.choice(list(move_operators.MOVE_OP_MAP.values()))(pattern, list(heuristics.HEURISTIC_MAP.keys()))

    @staticmethod
    def is_valid(proposed_solution):
        """
        Determines whether the proposed solution is a valid solution.
        :param proposed_solution: A sequence of airplanes.
        :return: bool
        """
        proposed_solution = sorted(proposed_solution, key=lambda x: x.landing_time)
        return proposed_solution[0].valid() and all(
            proposed_solution[i].valid() and
            proposed_solution[i].is_after(proposed_solution[i - 1]) and
            proposed_solution[i].is_before(proposed_solution[i + 1])
            for i in range(1, len(proposed_solution) - 1)
        )
