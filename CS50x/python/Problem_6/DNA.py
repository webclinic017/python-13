# -*- coding: utf-8 -*-
"""
@date: Mon Mar  7 10:58:33 2022

@author: Giang Nguyen
"""

#%Load module.
import numpy as np
#import matplotlib.pyplot as plt
import csv
import sys

def main():

    # TODO: Check for command-line usage
    if len(sys.argv)!=3:
        print("Error! \npython dna.py file.csv DNA.text")
        sys.exit(1)
    # TODO: Read database file into a variable
    with open(sys.argv[1], "r") as file:
        reader= csv.reader(file)
        data = list(reader)
    
    print(data)
    #header=data[:][0]
    STRs=data[0][1:]
    print("STRs= "+str(STRs))

    name=[]
    for i in range(1,len(data)):
        #print(data[i][0])
        name.append((data[i][0]))
    print("name= "+str(name))
    counter_DNA=np.zeros((len(name),len(STRs)))
    #print(counter_DNA)
    
    for i in range(len(counter_DNA)):
        for j in range(len(counter_DNA[0])):
            counter_DNA[i][j]=int(data[i+1][j+1])
    print("counter_DNA= "+str(counter_DNA))
            
    
    #int(data[i+1][j+1])
    # TODO: Read DNA sequence file into a variable
    DNA_file= open(sys.argv[2],'r')
    DNA=DNA_file.read()
    DNA_file.close()
    #print(DNA)
    # TODO: Find longest match of each STR in DNA sequence
    counter_STRs=np.zeros(len(STRs))
    for i in range(len(STRs)):
        counter_STRs[i]=longest_match(DNA, STRs[i])
    #print("counter_STRs= "+str(counter_STRs))

    for i in range(len(counter_DNA)):
        checker=1
        for j in range(len(counter_STRs)):
            if counter_DNA[i][j]!=counter_STRs[j]:
                checker=0
        if checker==1:
            print(name[i])
            break;
    if checker==0:
        print("No match")



    # TODO: Check database for matching profiles

    return
    

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run
main()

