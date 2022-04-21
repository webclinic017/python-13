# Simulate a sports tournament

import csv
import sys
import random
import math

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    counts = []
    # TODO: Read teams into memory from file
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["rating"] = int(row["rating"])
            team=row["team"]
            teams.append(row)
        for row in reader:
            row["score"]=0
            counts.append(row)
    print(teams)
    print(counts)
    a=(teams[0])
    print(a['team'])
if __name__ == "__main__":
    main()
