from unittest import TestCase
from src import ProbabilityCalculator, Unit


class TestProbabilityCalculator(TestCase):
    def test_get_next_state(self):
        assert ProbabilityCalculator.get_next_state(1, (1, 2, 3)) == (1, 3, 3)

    def test_is_final_state(self):
        units = [Unit(num_wanted=3, num_have=0, cost=3), Unit(num_wanted=2, num_have=0, cost=2)]
        p_calc = ProbabilityCalculator(units, 6)

        assert p_calc.is_final_state((3, 2)) is True
        assert p_calc.is_final_state((3, 4)) is False
        assert p_calc.is_final_state((1, 2)) is False

    def test_is_valid_state(self):
        units = [Unit(num_wanted=3, num_have=0, cost=3), Unit(num_wanted=2, num_have=0, cost=2)]
        p_calc = ProbabilityCalculator(units, 6)

        assert p_calc.is_final_state((3, 2)) is True
        assert p_calc.is_final_state((3, 4)) is False

    def test_get_num_same_cost_units(self):
        units = [Unit(num_wanted=4, num_have=1, cost=3),
                 Unit(num_wanted=2, num_have=1, cost=3),
                 Unit(num_wanted=2, num_have=0, cost=2)]
        p_calc = ProbabilityCalculator(units, 6)
        row_tuple = (2, 2, 1)
        unit = units[0]
        assert p_calc.get_num_same_cost_units(row_tuple, unit) == 1 + 1 + 2 + 2

        units = [Unit(num_wanted=4, num_have=1, cost=3)]
        p_calc = ProbabilityCalculator(units, 6)
        row_tuple = (2,)
        unit = units[0]
        assert p_calc.get_num_same_cost_units(row_tuple, unit) == 1 + 2

    # TODO: implement this
    def test_get_find_one_prob(self):
        pass


