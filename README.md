# dynasty_draft

Takes the standings of a given year, performs a weighted lottery selection and returns the draft order.

The `Simulator` Class includes methods which give the probability of attaining a certain draft pick for each team

Instructions:
    1) Save standings as a CSV (place in standings, team name) (Optional)
    2) Call `python draft_simulator.py` on the command line
        a) Pass in the filename argument containing the standings CSV using flag `--filename` or indicate there is no file and input the standings dynamically using flag `--nofile`.
        b) Pass in the desired action (`draft` or `odds`) using the flag `--action`.  `draft` performs the draft and `odds` returns the probabilities of a team getting a certain pick or better
    3) Call `python draft_simulator.py --help` for detailed instructions
