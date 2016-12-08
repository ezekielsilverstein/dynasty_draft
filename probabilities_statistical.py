import random
import copy
import csv
from argparse import ArgumentParser
from itertools import permutations

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

def permutation_odds(p):
    """
    Set the odds of a given permutation occuring

    arg: an n=6 permutation of teams in the lottery

    return: probability of permutation occuring
    """
    chance_list = []
    denominator = 21
    """
    roll through each team in order
    and calculate the probability of the next team getting chosen
    multiply all at the end for a total probability for this permutation
    """
    for t in p:
        numerator = counts[t]
        chance_of_selection = float(numerator)/denominator
        chance_list.append(chance_of_selection)
        denominator -= numerator
    chance_of_this_permutation = reduce(lambda x, y: x*y, chance_list)
    return chance_of_this_permutation

def create_prob_dict():
    """
    Create probability dictionary
    of each team getting each pick
    """
    odds = {}
    for t in standings.values():
        odds[t] = {i:0 for i in range(1,7)}
    perms = permutations(standings.values()) #Find permutations
    for p in perms: #For each permutation
        chance = permutation_odds(p) #Find the chance of each occuring
        for pick in range(len(p)): #For each pick in the permutation
            odds[p[pick]][1+pick] += chance #Add the probability the team getting the pick
    for k,v in odds.iteritems(): #Round each probability
        for pick, chance in v.iteritems():
            odds[k][pick] = round(odds[k][pick],4)
    return odds

def cumulative_PD(prob_dict):
    """
    Create a dictionary of cumulative probabilities

    Similar structure of prob_dict from PD

    values of each sub-dictionary contain
    the probabilities of a team getting THAT PICK OR BETTER
    """
    cum_prob_dict = {}
    for t in standings.values():
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

def main(fname):
    """
    Craft the total function
    """
    global standings
    standings = set_standings(fname)
    global counts
    counts = set_ball_count_dict()
    prob_dict = create_prob_dict()
    cum_prob_dict = cumulative_PD(prob_dict)
    printout(prob_dict, cum_prob_dict)
    return None

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-f', '--filename', default="lottery_standings_2016.csv",
    type=str, help='Name of file containing lottery standings')
    args = parser.parse_args()

    main(args.filename)
