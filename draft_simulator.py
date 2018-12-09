import random
import csv
from time import sleep
from argparse import ArgumentParser
import datetime
from itertools import permutations
from functools import reduce


class Simulator:
    """
    Draft Lottery Simulation Class
    """
    def __init__(self, standings):
        # self.filename = filename
        self.standings = standings

    def set_lottery(self):
        self.counts = self.set_ball_count()
        self.ppballs = self.create_balls()

    def perform_lottery(self):
        self.order = self.selection()

    def set_ball_count(self):
        """
        Sets the number of ping-pong balls for each team
        :return: dictionary of counts 
        """
        counts = {}
        for t in sorted(self.standings.keys()):
            counts[self.standings[t]] = t - (min(self.standings.keys()) - 1)
        return counts

    def create_balls(self):
        """
        Create a list of ping-pong balls.
        Each ball is labelled by a team name.
        The number of balls for each team is set
        by the ball count dict
        :return: list of ping-pong balls
        """
        ppballs = []
        for k, v in self.counts.items():
            for i in range(v):
                ppballs.append(k)
        return ppballs

    def selection(self):
        """
        Select ping-pong balls and create a draft order

        Continue selecting teams which have not been chosen yet
        Result is a dictionary with the pick number and the team
        :return: Lottery order dict
        """
        order = {}
        while len(order) < len(self.standings):
            pick = random.choice(self.ppballs)
            order[len(order) + 1] = pick
            self.ppballs = [ball for i, ball in enumerate(self.ppballs) if ball != pick]

        return order

    def print_draft_results(self):
        """
        Printout to create suspension :)
        """
        current_year = datetime.datetime.now().year
        print("\nWelcome to the {} Dynasty Rookie and Free Agent Draft\n".format(current_year))

        keys = list(self.order.keys())
        for k in reversed(keys):
            print("With Pick Number {}:".format(k))
            sleep(0.5)
            print(self.order[k])
            print("")
            sleep(0.5)
        return None

    ###
    # Methods to calculate the odds of draft pick for each team
    # PROBABILISTIC
    ###

    def calculate_probabilistic_odds(self):
        """
        Calculate both individual probabilities for a team getting a certain pick
        AND getting a certain pick OR BETTER
        :return: 
        """
        self.probabilistic_odds = self._calculate_individual_probabilities_statistical()
        self.cumulative_probabilistic_odds = self._calculate_cumulative_probabilities_statistical()
        return None

    def _calculate_individual_probabilities_statistical(self):
        """
        Calculate the chance that each team gets a certain pick
        :return: Nested probability dictionary
        """
        self.counts = self.set_ball_count()
        standings_permutations = permutations(self.standings.values())
        probabilistic_odds_dict = self._cycle_through_permutations(standings_permutations)
        return probabilistic_odds_dict

    def _calculate_cumulative_probabilities_statistical(self):
        """
        Calculate the chance that each team gets a certain pick OR BETTER
        :return: Nested cumulative probability dictionary
        """

        # Create empty nested dictionary
        pick_slot_dict = {i: 0 for i in range(1, 1+len(self.standings))}
        cumulative_probabilistic_odds_dict = {team: pick_slot_dict.copy() for team in self.standings.values()}

        # For each team
        for team in self.standings.values():
            # Get the probabilistic values dict
            pick_dict = self.probabilistic_odds[team]
            for pick in pick_dict.keys():
                cumulative_probabilistic_odds_dict[team][pick] = round(sum(
                    [self.probabilistic_odds[team][i] for i in pick_dict.keys() if i <= pick]), 4)

        return cumulative_probabilistic_odds_dict

    def _cycle_through_permutations(self, permutations_gen):
        """
        Run through the permutations generator

        :param permutations_gen: 
        :return: A nested dictionary for each team and the chance of getting each pick
        """

        pick_slot_dict = {i: 0 for i in range(1, 1+len(self.standings))}
        choice_odds_dict = {team: pick_slot_dict.copy() for team in self.standings.values()}

        # For each possible permutation
        for permutation in permutations_gen:
            # Get the chance of it occurring
            chance = self._permutation_selection_chance(permutation)
            # For each pick
            for pick_num in range(len(permutation)):
                # Increment the appropriate nested dict team-pick:chance-of-occurrence
                team = permutation[pick_num]
                choice_odds_dict[team][pick_num + 1] += chance

        # Round the nested dict values
        for team, pick_dict in choice_odds_dict.items():
            for pick in pick_dict.keys():
                choice_odds_dict[team][pick] = round(choice_odds_dict[team][pick], 4)

        return choice_odds_dict

    def _permutation_selection_chance(self, permutation):
        """
        Returns the odds that a certain draft order
        permutation will occur
        :param permutation: A single draft order permutation
        :return: Chance of selection
        """
        chance_list = []
        denominator = sum(self.counts.values())

        for t in permutation:
            numerator = self.counts[t]
            chance_of_selection = float(numerator)/denominator
            chance_list.append(chance_of_selection)
            denominator -= numerator

        chance_of_this_permutation = reduce(lambda x, y: x*y, chance_list)
        return chance_of_this_permutation

    def print_probabilities(self):
        """
        Print the team-pick probabilities
        Both for a certain pick and for a certain pick OR BETTER
        :return: None
        """
        for place in sorted(self.standings.keys()):
            team = self.standings[place]
            statement = (
                "--- {} --- ({}th place) has these probabilities:".format(team, place)
            )
            print(statement)
            print("Pick\tThis pick\tThis pick or better")
            for pick in sorted(self.probabilistic_odds[team].keys()):
                print(
                    "{}:\t{}\t\t{}".format(pick,
                                           self.probabilistic_odds[team][pick],
                                           self.cumulative_probabilistic_odds[team][pick]))
                print("")
        return None


def read_in_standings(filename):
    """
    Takes a filename, parses it
    :return: standings dictionary
    """
    with open(filename, 'r') as f:
        standings = {}
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            place = int(row[0])
            team = str(row[1])
            standings[place] = team
    return standings


def build_standings(num_teams_lottery, num_teams_league):
    """
    Asks for command line entry of standings
    """
    standings = {}
    place_ranks = range(num_teams_league - num_teams_lottery + 1, num_teams_league + 1)

    for pr in place_ranks:
        team = input("Please input team in {}th place:\n".format(pr))
        standings[pr] = team

    return standings


def main(filename, nofile, action):
    """
    Set the Simulator Class and perform the lottery
    :param filename: name of the standings txtfile
    :param nofile: if this flag, ask for standings via input
    :param action: Perform the draft or calculate and print the odds
    :return: completed Simulator Class 
    """

    if nofile:
        num_teams_league = int(input("Please input number of teams in league:\n"))
        num_teams_lottery = int(input("Please input number of teams in lottery:\n"))
        standings = build_standings(num_teams_lottery, num_teams_league)
    else:
        standings = read_in_standings(filename)

    sim = Simulator(standings)

    if action == 'draft':
        sim.set_lottery()
        sim.perform_lottery()
        sim.print_draft_results()
    elif action == 'odds':
        sim.calculate_probabilistic_odds()
        sim.print_probabilities()

    return sim


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', '--filename', default="lottery_standings.csv",
                        type=str, help='Name of file containing lottery standings')
    parser.add_argument('--nofile', action="store_true",
                        help='No file containing standings is available -- Manual entry of standings is required')
    parser.add_argument('-a', '--action', default='draft', choices=['draft', 'odds'],
                        type=str, help='Perform draft (default) or determine odds')
    args = parser.parse_args()

    s = main(args.filename, args.nofile, args.action)


