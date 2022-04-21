#include <stdio.h>
#include <string.h>
#include <stdbool.h>
// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    char *name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(char name[]);
void print_winner(void);

int main(int argc, char *argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        printf(" %s", candidates[i].name);
    }
    printf("\n");
    int voter_count;
    printf("Number of voters: ");
    scanf_s(" %d", &voter_count);
    // SCANF_S WILL LEAVE A \N EVERYTIME IT EXECUTES.
    char clean_scanf_mess[1];
    gets(clean_scanf_mess);

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        printf("Vote: ");
        char name[20];
        gets(name);

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }
    /*
        for(int i = 0; i < candidate_count; i++)
        {
            printf("%i ",candidates[i].votes);
        }
    */
    // Display winner of election
    print_winner();
    return 0;
}

// Update vote totals given a new vote
bool vote(char name[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes++;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    int max = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        if (max <= candidates[i].votes)
        {
            max = candidates[i].votes;
        }
    }
    //printf("%i",max);
    for (int i = 0; i < candidate_count; i++)
    {
        if (max == candidates[i].votes)
        {
            printf("%s ", candidates[i].name);
        }
    }
    return;
}