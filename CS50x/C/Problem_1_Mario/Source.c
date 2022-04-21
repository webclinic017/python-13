#include <stdio.h>

int main(void)
{
	int steps=0;
	while (steps < 1 || steps>8)
	{
		printf("Enter the number of steps (between 1 and 8): ");
		scanf_s("%d", &steps);
	}
	for (int i = 0; i < steps+1; i++)
	{
		for (int j = steps-i; j > 0; j--)
		{
			printf(" ");
		}
		for (int k = 0; k < i; k++)
		{
			printf("#");
		}
		for (int k_2 = 0; k_2 < 2; k_2++)
		{
			printf(" ");
		}
		for (int k = 0; k < i; k++)
		{
			printf("#");
		}
		for (int j = steps - i; j > 0; j--)
		{
			printf(" ");
		}
		printf("\n");
	}
	

}