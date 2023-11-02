from set_info import SetInfo
import pydtmc as m
import numpy as np
from typing import List, Tuple
import itertools

# inputs
# 1. number of each unit we want
# 2. cost of each unit we want
# 3. starting number of the unit
# 2. level we're at


class Unit:
    def __init__(self, num_wanted, num_have, cost):
        self.num_wanted = num_wanted
        self.num_have = num_have
        self.cost = cost


# TODO: also consider units that are out of the pool
class ProbabilityCalculator:

    def __init__(self, units: List[Unit], level: int):
        self.units = units
        self.level = level
        self.set_info = SetInfo()

        self.unit_states = list(itertools.product(*[range(unit.num_wanted + 1) for unit in self.units]))
        self.idx_to_states_mapping = {idx: state for idx, state in zip(range(len(self.unit_states)), self.unit_states)}
        self.states_to_idx_mapping = {y: x for x, y in self.idx_to_states_mapping.items()}

        self.prob_matrix = self.create_prob_matrix()

    @staticmethod
    def get_next_state(idx: int, state: Tuple) -> Tuple:
        return tuple([state[i] if i != idx else state[i] + 1 for i in range(len(state))])

    def is_final_state(self, state: Tuple) -> bool:
        return all(state_unit == unit.num_wanted for state_unit, unit in zip(state, self.units))

    def is_valid_state(self, state) -> bool:
        return all(state_unit <= unit.num_wanted for state_unit, unit in zip(state, self.units))

    def get_num_same_cost_units(self, row_tuple: Tuple[int], unit: Unit) -> int:
        same_cost = 0
        for unit_idx, num_have in enumerate(row_tuple):
            other_unit = self.units[unit_idx]
            if other_unit.cost == unit.cost:  # we're okay with counting the original unit
                same_cost += num_have + other_unit.num_have
        return same_cost

    def get_find_one_prob(self, changed_unit_idx: int, state: Tuple) -> float:
        changed_unit = self.units[changed_unit_idx]
        num_changed_unit = state[changed_unit_idx]
        cost = changed_unit.cost

        num_same_cost = self.get_num_same_cost_units(state, changed_unit)
        base_probability = self.set_info.get_unit_prob(self.level, cost)
        pool_total = self.set_info.get_pool_total(cost)
        num_copies_changed_unit = self.set_info.get_num_copies(cost) - changed_unit.num_have - num_changed_unit

        final_probability = base_probability * num_copies_changed_unit / (pool_total - num_same_cost)
        return final_probability

    def create_prob_matrix(self) -> np.array:
        num_rows_col = len(self.idx_to_states_mapping)
        prob_matrix = np.zeros((num_rows_col, num_rows_col))
        for state in self.unit_states:
            current_state_idx = self.states_to_idx_mapping[state]
            if self.is_final_state(state):
                prob_matrix[current_state_idx][current_state_idx] = 1
                continue
            cumulative_prob = 0
            for i in range(len(state)):
                next_state = self.get_next_state(i, state)
                prob = self.get_find_one_prob(i, state)
                if self.is_valid_state(next_state):
                    next_state_idx = self.states_to_idx_mapping[next_state]
                    prob_matrix[current_state_idx][next_state_idx] = prob
                cumulative_prob += prob
            prob_matrix[current_state_idx][current_state_idx] = 1 - cumulative_prob  # probability of staying at current
        return prob_matrix


if __name__ == '__main__':
    sample_input = [Unit(num_wanted=3, num_have=0, cost=3), Unit(num_wanted=2, num_have=0, cost=2)]
    p_calc = ProbabilityCalculator(sample_input, 6)
    print(p_calc.prob_matrix)
    