
r = [1, 0, 0, 0, 0, 0]


def init(r):
    r[2] = 2            # [17]
    r[2] = r[2] * r[2]  # [18]
    r[2] = 19 * r[2]    # [19]
    r[2] = r[2] * 11    # [20]
    r[5] = r[5] + 3     # [21]
    r[5] = r[5] * 22    # [22]
    r[5] = r[5] + 3     # [23]
    r[2] = r[2] + r[5]  # [24]

    if not r[0]:        # [25]
        return          # [26]

    r[5] = 27           # [27]
    r[5] = r[5] * 28    # [28]
    r[5] = r[5] + 29    # [29]
    r[5] = r[5] * 30    # [30]
    r[5] = r[5] * 14    # [31]
    r[5] = r[5] * 32    # [32]
    r[2] = r[5] + r[2]  # [33]
    r[0] = 0            # [34]


def loop(r):

    r[1] = 1                        # [1]
    while True:
        #print(r)
        r[4] = 1                    # [2]

        while True:
            r[5] = r[1] * r[4]      # [3]
            if r[5] == r[2]:        # [4-6]
                r[0] = r[1] + r[0]  # [7]

            r[4] += 1               # [8]

            if r[4] > r[2]:         # [9-10]
                break               # [11]

        r[1] += 1                   # [12]

        if r[1] > r[2]:
            break


try:
    # Brute-force part 2 solution, this will never finish...
    init(r)
    loop(r)
except KeyboardInterrupt:
    pass
finally:
    print(r)
