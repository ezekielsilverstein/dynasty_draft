from collections import Counter

from draft_simulator import Simulator, read_in_standings


class TestClass(object):

    def test_correct_number_of_teams(self):
        standings = read_in_standings('lottery_standings.csv')
        s = Simulator(standings)
        assert len(s.standings) == 6

    def test_correct_total_number_of_ping_pong_balls_before_selection(self):
        standings = read_in_standings('lottery_standings.csv')
        s = Simulator(standings)
        s.set_lottery()
        assert len(s.ppballs) == 21

    def test_correct_total_number_of_ping_pong_balls_after_selection(self):
        standings = read_in_standings('lottery_standings.csv')
        s = Simulator(standings)
        s.set_lottery()
        s.perform_lottery()
        assert len(s.ppballs) == 0

    def test_correctly_assigned_ping_pong_balls(self):
        standings = read_in_standings('lottery_standings.csv')
        s = Simulator(standings)
        s.set_lottery()
        expected_pp_balls = {v: k-6 for k, v in s.standings.items()}
        actual_pp_balls = dict(Counter(s.ppballs))
        assert actual_pp_balls == expected_pp_balls

    def test_ascending_cumulative_probabilities(self):
        standings = read_in_standings('lottery_standings.csv')
        s = Simulator(standings)
        s.calculate_probabilistic_odds()
        six_trues = [True] * 6
        ordered = []
        for ordered_cum_probabilities in s.cumulative_probabilistic_odds.values():
            if list(ordered_cum_probabilities.values()) == sorted(ordered_cum_probabilities.values()):
                ordered.append(True)
            else:
                ordered.append(False)

        assert six_trues == ordered

    def test_probability_sums_equal_one(self):
        standings = read_in_standings('lottery_standings.csv')
        s = Simulator(standings)
        s.calculate_probabilistic_odds()
        probability_sums = [round(sum(v.values()), 3) for v in s.probabilistic_odds.values()]
        six_ones = [1.0] * 6
        assert probability_sums == six_ones

    def test_probability_of_pick_six_or_better_equals_one(self):
        standings = read_in_standings('lottery_standings.csv')
        s = Simulator(standings)
        s.calculate_probabilistic_odds()
        six_or_better = [round(v[6], 3) for v in s.cumulative_probabilistic_odds.values()]
        six_ones = [1.0] * 6
        assert six_or_better == six_ones

    def test_no_dupes_in_lottery_order(self):
        standings = read_in_standings('lottery_standings.csv')
        s = Simulator(standings)
        s.set_lottery()
        s.perform_lottery()
        assert len(s.order.values()) == len(set(s.order.values()))
