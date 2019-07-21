""" coin change problem """

def change(n, coins_available, coins_so_far):
    if sum(coins_so_far) == n:
        yield coins_so_far
    elif sum(coins_so_far) > n:
        pass
    elif coins_available == []:
        pass
    else:
        for c in change(n, coins_available[:], coins_so_far+[coins_available[0]]):
            yield c
        for c in change(n, coins_available[1:], coins_so_far):
            yield c


if __name__ == '__main__':
    n = input('An amount to make change for: ')
    coins = input('An array of integers representing available denominations: ')
    solutions = [s for s in change(n, coins, [])]
    for s in solutions:
        print s
