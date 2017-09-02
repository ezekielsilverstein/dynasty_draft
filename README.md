# dynasty_draft

Takes the standings of a given year and returns the draft order for next year's draft.

Simulator Class includes methods which give the probability of attaining a certain draft pick for each team

Instructions:
    1) Save standings as a CSV (place in standings, team name)
    2) Call `python draft_simulator.py`
        a) Pass in the filename argument containing the standings CSV using flag `--filename`
        b) Pass in the desired action (`draft` or `odds`) using the flag `--action`.  `draft` performs the draft and `odds` returns the probabilities of a team getting a certain pick or better
