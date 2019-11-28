#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <time.h>

void init(uint32_t *r)
{
    r[2] = 2;
    r[2] = r[2] * r[2];
    r[2] = 19 * r[2];
    r[2] = r[2] * 11;
    r[5] = r[5] + 3;
    r[5] = r[5] * 22;
    r[5] = r[5] + 3;
    r[2] = r[2] + r[5];

    if (!r[0])
    {
        return;
    }

    r[5] = 27;
    r[5] = r[5] * 28;
    r[5] = r[5] + 29;
    r[5] = r[5] * 30;
    r[5] = r[5] * 14;
    r[5] = r[5] * 32;
    r[2] = r[5] + r[2];
    r[0] = 0;
}

void loop(uint32_t *r)
{
    r[1] = 1;
    while (1)
    {
        r[4] = 1;

        while (1)
        {
            r[5] = r[1] * r[4];
            if (r[5] == r[2])
            {
                r[0] = r[1] + r[0];
            }
            r[4] += 1;

            if (r[4] > r[2])
            {
                break;
            }
        }
        r[1] += 1;

        if (r[1] > r[2])
        {
            break;
        }
    }
}

void print(uint32_t *r)
{
    printf("[%u, %u, %u, %u, %u, %u]\r\n",
        r[0],
        r[1],
        r[2],
        r[3],
        r[4],
        r[5]
        );
}

uint32_t divisor_sum(uint32_t input)
{
    uint32_t sum = 0;
    for (uint32_t i = 1; i <= input; ++i)
    {
        if (!(input %  i))
        {
            sum += i;
        }
    }
    printf("%s: %u\r\n", __func__, sum);
}

int main()
{
    // Calculate part 2 solution
    divisor_sum(10551305);

    // Brute-force solution, should complete in ~11 hours
    uint32_t r[6] = {0};

    time_t start;
    start = time(NULL);

    init(r);
    loop(r);

    time_t end;
    end = time(NULL);

    printf("Time: %ld\n", end - start);
    print(r);

    return 0;
}
