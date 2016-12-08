import random
import copy
import csv
from argparse import ArgumentParser

def set_standings(fname):
    """
    Import a textfile containing the standings of teams 
    to be entered into the lottery
    """
    with open(fname, 'rU') as f:
        standings = {}
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            place = int(row[0])
            team = row[1]
            standings[place] = team
    return standings

def set_ball_count_dict():
    """
    Create a dictionary:

    keys: team names
    values: number of ping-pong balls
    """
    counts = {}
    for t in sorted(standings.keys()):
        counts[standings[t]] = t - 6
    return counts

def create_balls():
    """
    Create a list of ping-pong balls.
    Each ball is labelled by a team name.
    The number of balls for each team is set
    by set_ball_count_dict()
    """
    balls = []
    for k,v in counts.iteritems():
        for i in range(v):
            balls.append(k)
    return balls

def selection():
    """
    Select ping-pong balls and create a draft order

    Continue selecting teams which have not been chosen yet.
    Result is a dictionary with the pick number and the team
    """
    order = []
    while len(order) < 6:
        pick = random.choice(balls)
        if pick not in order:
            order.append(pick)
    return order

def CD(selection):
    """
    Create a dictionary to keep track of each simulation

    keys: team name
    values: another dictionary
        v/k: pick number
        v/v: occurences
    """
    choices_dict = {}
    for t in sorted(standings.values()):
        choices_dict[t] = {i:0 for i in range(1,7)}
    for i in range(args.simulations):
        order = selection()
        for t in range(len(order)):
            choices_dict[order[t]][t+1] += 1
    return choices_dict

def PD(choices_dict):
    """
    Copy the choices_dict from CD

    Divide by the number of simulations
    Returns a dictionary anologous to choices_dict,
    but with the probabilities for each team receiving each pick
    rather than the number of occurences throughout the simulations
    """
    prob_dict = copy.deepcopy(choices_dict)
    for k,v in prob_dict.iteritems():
        for placement, count in v.iteritems():
            prob_dict[k][placement] = round(count / float(args.simulations),4)
    return prob_dict

def cumulative_PD(prob_dict):
    """
    Create a dictionary of cumulative probabilities

    Similar structure of prob_dict from PD

    values of each sub-dictionary contain
    the probabilities of a team getting THAT PICK OR BETTER
    """
    cum_prob_dict = {}
    for t in sorted(standings.values()):
        cum_prob_dict[t] = {i:0 for i in range(1,7)}
    for k,v in prob_dict.iteritems():
        for placement in v.keys():
            cumulative_placements = range(1,placement+1)
            cum_prob_dict[k][placement] = round(sum((prob_dict[k][cp] for cp in cumulative_placements)),4)
    return cum_prob_dict

def printout(prob_dict, cum_prob_dict):
    print "Using a Probabilistic Method:\n"
    for s in sorted(standings.keys()):
        team = standings[s]
        statement = (
            "---{}--- ({}th place) has these probabilities:".format(team, s)
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

def main():
    """
    Craft the total function
    """
    global standings
    standings = set_standings(args.filename)
    global counts
    counts = set_ball_count_dict()
    global balls
    balls = create_balls()
    choices_dict = CD(selection)
    prob_dict = PD(choices_dict)
    cum_prob_dict = cumulative_PD(prob_dict)
    printout(prob_dict, cum_prob_dict)
    return None

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-s', '--simulations', default=100000, type=int, 
        help='Number of Monte Carlo simulations')
    parser.add_argument('-f', '--filename', default="lottery_standings_2016.csv", type=str, 
        help='Name of file containing lottery standings')
    args = parser.parse_args()

    main()


