import random
import csv
from time import sleep

def set_standings():
    with open("lottery_standings_2016.csv", 'rU') as f:
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

def create_balls():
    balls = []
    for k,v in counts.iteritems():
        for i in range(v):
            balls.append(k)
    return balls

def selection():
    order = {}
    while len(order) < 6:
        pick = random.choice(balls)
        if pick not in order.values():
            order[len(order)+1]=pick
    return order

def printout(draft_order):
    for k in reversed(draft_order.keys()):
        print "With Pick Number {}:".format(k)
        sleep(2)
        print draft_order[k]
        print ""
        sleep(2)
    return None

def main():
    global standings
    standings = set_standings()
    global counts
    counts = set_ball_count_dict()
    global balls
    balls = create_balls()
    draft_order = selection()
    printout(draft_order)
    
if __name__ == '__main__':
    main()
