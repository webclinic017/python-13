#include <stdio.h>
#include <string.h>
#include <ctype.h>
int main(int argc, char* argv[])
{
	char plaintext[] = "hello, world";
	char  ciphertext[sizeof(plaintext)];
	char key[27];
	int new_position = 0;
	int size_argv_1 = 0;
	int i = 0, j =0;
	if (argc == 2)
	{
		while (argv[1][j] != '\0')
		{
			key[j] = argv[1][j];
			j++;
			size_argv_1++;
		}
		key[sizeof(key) - 1] = '\0';
		printf("%s\n", key);
		printf("%i\n", size_argv_1);
		if (size_argv_1 != 26)
		{
			printf("Wrong key! The key must contain 26 characters");
		}
		while (plaintext[i] != '\0')
		{
			if (islower(plaintext[i]))
			{
				new_position = (int)plaintext[i] - 97;
				ciphertext[i] = tolower(key[new_position]);
				i++;
			}

			else if (isupper(plaintext[i]))
			{
				new_position = (int)plaintext[i] - 65;
				ciphertext[i] = key[new_position];
				i++;
			}
			else
			{
				ciphertext[i] = plaintext[i];
				i++;
			}
				
			
		}
		ciphertext[sizeof(ciphertext) - 1] = '\0';
		printf("%s", ciphertext);
	}
	else
	{
		printf("Wrong input!");
	}
	return 0;
}