import random
import copy
import csv
from argparse import ArgumentParser
from itertools import permutations

def set_standings():
    with open("../lottery_teams_2016.csv", 'rU') as f:
        standings = {}
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            place = int(row[0])
            team = row[1]
            standings[place] = team
    return standings

def set_ball_count_dict():
    counts = {}
    for t in sorted(standings.keys()):
        counts[standings[t]] = t - 6
    return counts

def permutation_odds(p):
    chance_list = []
    denominator = 21
    for t in p:
        numerator = counts[t]
        chance_of_selection = float(numerator)/denominator
        chance_list.append(chance_of_selection)
        denominator -= numerator
    chance_of_this_permutation = reduce(lambda x, y: x*y, chance_list)
    return chance_of_this_permutation

def create_prob_dict():
    odds = {}
    for t in standings.values():
        odds[t] = {i:0 for i in range(1,7)}
    perms = permutations(standings.values())
    for p in perms:
        chance = permutation_odds(p)
        for pick in range(len(p)):
            odds[p[pick]][1+pick] += chance
    for k,v in odds.iteritems():
        for pick, chance in v.iteritems():
            odds[k][pick] = round(odds[k][pick],4)
    return odds

def cumulative_PD(prob_dict):
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

def main():
    global standings
    standings = set_standings()
    global counts
    counts = set_ball_count_dict()
    prob_dict = create_prob_dict()
    cum_prob_dict = cumulative_PD(prob_dict)
    printout(prob_dict, cum_prob_dict)
    return None

if __name__ == "__main__":
    main()

