#include <stdio.h>

int main(void)
{
    char buffer[13];

    int i = 50;
    sprintf_s(buffer, "This is CS%i\n", i);

    float f = 50.0;
    sprintf_s(buffer, "This is CS%.0f\n", f);
}