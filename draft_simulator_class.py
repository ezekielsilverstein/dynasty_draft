import random
import csv
from time import sleep
from argparse import ArgumentParser
import datetime

class Simulator:
    """
    Draft Lottery Simulation Class
    """
    def __init__(self, filename):
        self.filename = filename
        self.standings = self.read_in_standings()

    def perform_lottery(self):
        self.counts = self.set_ball_count()
        self.ppballs = self.create_balls()
        self.order = self.selection()

    def read_in_standings(self):
        """
        Takes a filename, parses it
        :return: standings dictionary
        """
        with open(self.filename, 'rU') as f:
            standings = {}
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                place = int(row[0])
                team = str(row[1])
                standings[place] = team
        return standings

    def set_ball_count(self):
        """
        Sets the number of ping-pong balls for each team
        :return: dictionary of counts 
        """
        counts = {}
        for t in sorted(self.standings.keys()):
            counts[self.standings[t]] = t - 6
        return counts

    def create_balls(self):
        """
        Create a list of ping-pong balls.
        Each ball is labelled by a team name.
        The nubmer of balls for each team is set
        by the ball count dict
        :return: list of ping-pong balls
        """
        ppballs = []
        for k, v in self.counts.iteritems():
            for i in range(v):
                ppballs.append(k)
        return ppballs

    def selection(self):
        """
        Select ping-pong balls and create a draft order
        
        Continue selecting teams which have not been chosen yet
        Result is adictionary with the pick number and the team
        :return: Lottery order dict
        """
        order = {}
        while len(order) < 6:
            pick = random.choice(self.ppballs)
            if pick not in order.values():
                order[len(order)+1]=pick
        return order

    def printout(self):
        """
        Printout to create suspension :)
        """
        for k in reversed(self.order.keys()):
            print "With Pick Number {}:".format(k)
            sleep(1)
            print self.order[k]
            print ""
            sleep(1)
        return None

def main(fname):
    """
    Set the Simulator Class and perform the lottery
    :param fname: name of the standings txtfile
    :return: completed Simulator Class 
    """
    s = Simulator(fname)
    s.perform_lottery()
    return s

def printout(s):
    """
    Print the lottery results
    :param s: Simulator Class
    :return: 
    """
    current_year = datetime.datetime.now().year
    print ("\nWelcome to the {} Hyuk Dynasty Rookie Draft\n"
    .format(current_year))
    s.printout()
    return None

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', '--filename', default="lottery_standings_2016.csv",
                        type=str, help='Name of file containing lottery standings')
    args = parser.parse_args()

    s = main(args.filename)
    printout(s)


