#include <stdio.h>

int main(void)
{
	long long int card_number;
	int number_digits = 0;
	char c = 'Y';
	int test = 125;
	long long int first_two_digits = 0;
	long long int first_digit = 0;
	long long int digit = 0;
	long long int sum_even_digits = 0;
	long long int sum_odd_digits = 0;
	long long int sum_digit = 0;
	while (c=='Y')
	{
		printf("Enter your credit card number: ");
		scanf_s(" %lli", &card_number);
		while (card_number != 0)
		{
			digit = card_number % 10;
			card_number = card_number / 10;
			number_digits++;
			printf("digit:%lli\n", digit);
			printf("number of digits is %lli\n", number_digits);
			if (number_digits % 2 == 0)
			{
				digit = digit * 2;
				if (digit >= 10)
				{
					digit = digit / 10 + digit % 10;
				}
				sum_even_digits = sum_even_digits + digit;
			}
			else
			{
				sum_odd_digits = sum_odd_digits + digit;
			}
			if (card_number >= 10 && card_number <= 99)
			{
				first_two_digits = card_number;
			}
			if (card_number < 10 && card_number>0)
			{
				first_digit = card_number;
			}
			sum_digit = sum_even_digits + sum_odd_digits;
		}
		printf("The first two digits are: %lli\n", first_two_digits);
		printf("The first digit is: %lli\n", first_digit);
		printf("The number of digits is:%lli\n", number_digits);
		printf("The sum of even digits is: %lli\n", sum_even_digits);
		printf("The sum of odd digits is: %lli\n", sum_odd_digits);
		printf("The sum of digits is: %lli\n", sum_digit);
		if (sum_digit % 10 == 0)
		{
			if (number_digits == 15 && (first_two_digits == 34 || first_two_digits == 37))
			{
				printf("The card is a American Express.\n");
			}
			else if (number_digits == 16&&(first_two_digits == 51 || first_two_digits == 52|| first_two_digits == 53 || first_two_digits == 54||first_two_digits == 55))
			{
				printf("The card is a MasterCard.\n");
			}
			else if ((number_digits ==13||number_digits==16)&&first_digit==4)
			{
				printf("The card is a Visa card\n");
			}
			else
			{
				printf("The card is not valid\n");
			}
		}
		else
		{
			printf("The card is not valid\n");
		}
		first_two_digits = 0;
		first_digit = 0;
		digit = 0;
		sum_even_digits = 0;
		sum_odd_digits = 0;
		sum_digit = 0;
		number_digits = 0;
		printf("Do you want to continue (Y/N)? ");
		scanf_s(" %c", &c);
		while (c != 'Y' && c != 'N')
		{
			printf("Invalid request. DO you want to continue (Y/N)? ");
			scanf_s(" %c", &c);
		}
		//to do 2 scanf_s put a space in front of %c to cause scanf skip all whitespace characters.
	}
}