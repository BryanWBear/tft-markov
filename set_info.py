class SetInfo:
    def __init__(self) -> None:
        self.unit_probs_by_level = {                    # probability distribution of units by player level
            3: [0.75, 0.25, 0.00, 0.00, 0.00],
            4: [0.55, 0.30, 0.15, 0.00, 0.00],
            5: [0.45, 0.33, 0.20, 0.02, 0.00],
            6: [0.25, 0.40, 0.30, 0.05, 0.00],
            7: [0.19, 0.30, 0.35, 0.15, 0.01],
            8: [0.16, 0.20, 0.35, 0.25, 0.04],
            9: [0.09, 0.15, 0.30, 0.30, 0.16]
        }

        self.num_copies_by_cost = [29, 22, 18, 12, 10]  # number of each unique unit per cost
        self.num_unique_by_cost = [13, 13, 13, 12, 10]  # number of each unit cost

        assert all(sum(dist) == 1 for dist in self.unit_probs_by_level.values())

    def get_unit_prob(self, level: int, cost: int) -> float:
        return self.unit_probs_by_level[level - 1][cost - 1]

    def get_num_copies(self, cost: int) -> int:
        return self.num_copies_by_cost[cost - 1]

    def get_num_unique(self, cost: int) -> int:
        return self.num_unique_by_cost[cost - 1]

    def get_pool_total(self, cost: int) -> int:
        return self.get_num_copies(cost) * self.get_num_unique(cost)

