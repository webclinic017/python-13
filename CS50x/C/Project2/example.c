#include <stdio.h>
void meow(void);
int main(void)
{
	printf("Do you agree? ");
	char c = getchar();
	// Check whether agreed
	if (c == 'Y' || c == 'y')
	{
		printf("Agreed.\n");
	}
	else if (c == 'N' || c == 'n')
	{
		printf("Not agreed.\n");
	}
	for (int i = 0; i < 3; i++)
	{
		meow();
	}
}

void meow(void)
{
	printf("meow\n");
}