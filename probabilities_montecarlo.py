from draft_simulator_class import Simulator
from argparse import ArgumentParser
import copy


def run_lotteries(s, simulations):
    """
    Create a dictionary to keep track of each simulation
    :param s: Simulator Class 
    :param simulations: number of simulations
    :return: dictionary of occurrences
    """

    # Set the empty nested dictionary
    # empty dict for each pick set to 0
    pick_slot_dict = {i: 0 for i in range(1, 7)}
    # empty nested dict for each team and pick
    # saves counts of a team getting a certain pick
    choices_dict = {team: pick_slot_dict.copy() for team in s.standings.values()}
    # empty nested dict for each team and pick
    # save counts of a team getting a certain pick OR BETTER
    cumulative_choices_dict = {team: pick_slot_dict.copy() for team in s.standings.values()}

    # Run the Simulator simulations
    for i in range(simulations):
        s.perform_lottery()
        # for the pick number and team in this lottery's order
        for pick, team in s.order.iteritems():
            # increment the team's appropriate pick number: counter pair
            choices_dict[team][pick] += 1
            # increment the team's appropriate pick number: counter pairs
            # increment if the counter if this lottery's order
            # gave the team this pick in question or better
            # i.e. if the lottery gave team A pick 3
            # increment picks 3,4,5,6 += 1
            for cum_pick in range(pick, 7):
                cumulative_choices_dict[team][cum_pick] += 1

    return choices_dict, cumulative_choices_dict


def get_probabilities(s, simulations):
    """
    Create a dictionary to find the probabilities that 
    a team gets a certain pick
    :param s: Simulator Class
    :param simulations: number of simulations
    :return: 
    """
    choices_dict, cumulative_choices_dict = run_lotteries(s, simulations)

    prob_dict = copy.deepcopy(choices_dict)
    for team, pick_dict in prob_dict.iteritems():
        for pick, num_picked in pick_dict.iteritems():
            prob_dict[team][pick] /= float(simulations)

    cumulative_prob_dict = copy.deepcopy(cumulative_choices_dict)
    for team, pick_dict in cumulative_prob_dict.iteritems():
        for pick, num_picked in pick_dict.iteritems():
            cumulative_prob_dict[team][pick] /= float(simulations)

    return (choices_dict, prob_dict,
            cumulative_choices_dict, cumulative_prob_dict)


def main(fname, simulations):
    """
    
    :return: 
    """
    s = Simulator(fname)
    choices_dict, prob_dict, cumulative_choices_dict, cumulative_prob_dict = get_probabilities(s, simulations)
    printout(prob_dict, cumulative_prob_dict)

    return None


def printout(prob_dict, cum_prob_dict):
    print "Using a Probabilistic Method:\n"
    for team in sorted(prob_dict.keys()):
        statement = (
            "---{}--- has these probabilities:".format(team)
            )
        print statement
        print "Pick\tThis pick\tThis pick or better"
        for pick in prob_dict[team].keys():
            print (
                "{}:\t{}\t\t{}".format(pick,
                                       prob_dict[team][pick],
                                       cum_prob_dict[team][pick]))
        print ("")
    return None

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-s', '--simulations', default=100000, type=int,
                        help='Number of Monte Carlo simulations')
    parser.add_argument('-f', '--filename', default="lottery_standings_2016.csv", type=str,
                        help='Name of file containing lottery standings')
    args = parser.parse_args()

    main(args.filename, args.simulations)
