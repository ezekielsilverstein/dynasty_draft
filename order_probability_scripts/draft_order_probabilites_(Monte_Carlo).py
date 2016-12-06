import random
import copy
from argparse import ArgumentParser

def set_teams():
    teams = ['A','B','C','D','E','F']
    return teams

def set_ball_count_dict():
    counts = {}
    for t in range(len(teams)):
        counts[teams[t]] = 6 - t
    return counts

def create_balls():
    balls = []
    for k,v in counts.iteritems():
        for i in range(v):
            balls.append(k)
    return balls

def selection():
    order = []
    while len(order) < 6:
        pick = random.choice(balls)
        if pick not in order:
            order.append(pick)
    return order

def CD(selection):
    choices_dict = {}
    for t in teams:
        choices_dict[t] = {i:0 for i in range(1,7)}
    for i in range(args.simulations):
        order = selection()
        for t in range(len(order)):
            choices_dict[order[t]][t+1] += 1
    return choices_dict

def PD(choices_dict):
    prob_dict = copy.deepcopy(choices_dict)
    for k,v in prob_dict.iteritems():
        for placement, count in v.iteritems():
            prob_dict[k][placement] = round(count / float(args.simulations),4)
    return prob_dict

def cumulative_PD(prob_dict):
    cum_prob_dict = {}
    for t in teams:
        cum_prob_dict[t] = {i:0 for i in range(1,7)}
    for k,v in prob_dict.iteritems():
        for placement in v.keys():
            cumulative_placements = range(1,placement+1)
            cum_prob_dict[k][placement] = round(sum((prob_dict[k][cp] for cp in cumulative_placements)),4)
    return cum_prob_dict

def printout(prob_dict, cum_prob_dict):
    standings = {'A':12,'B':11,'C':10,'D':9,'E':8,'F':7}
    print "Using a Monte Carlo simulation where n = {}:\n".format(args.simulations)
    for s in sorted(standings.keys()):
        statement = (
            "The {}th place team has these probabilities:".format(standings[s])
            )
        print statement
        print "Pick\tThis pick\tThis pick or better"
        for pick in prob_dict[s].keys():
            print (
                "{}:\t{}\t\t{}".format(pick,
                	prob_dict[s][pick],
                	cum_prob_dict[s][pick]))
        print ("")
    return None

def main():
    global teams
    teams = set_teams()
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
    parser.add_argument('-s', '--simulations', default=100000, type=int, help='Number of Monte Carlo simulations')
    args = parser.parse_args()

    main()


