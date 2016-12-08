import random
import csv
from time import sleep
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
    order = {}
    while len(order) < 6:
        pick = random.choice(balls)
        if pick not in order.values():
            order[len(order)+1]=pick
    return order

def printout(draft_order):
	"""
	Printout to create suspension :)
	"""
    for k in reversed(draft_order.keys()):
        print "With Pick Number {}:".format(k)
        sleep(2)
        print draft_order[k]
        print ""
        sleep(2)
    return None

def main(fname):
	"""
	Craft the total function
	"""
    global standings
    standings = set_standings(fname)
    global counts
    counts = set_ball_count_dict()
    global balls
    balls = create_balls()
    draft_order = selection()
    printout(draft_order)
    return draft_order
    
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', '--filename', default="lottery_standings_2016.csv",
    type=str, help='Name of file containing lottery standings')
    args = parser.parse_args()

    main(args.filename)
