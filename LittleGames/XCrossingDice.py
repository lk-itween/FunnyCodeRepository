"""
猜骰子游戏
1. 有两个1-6的骰子，当掷出的和大于6为大，小于等于6为小。
2. 每轮游戏需要支付5个金币，没有金币不能游玩。
3. 如果猜对，奖励2个金币。
4. 当没有金币时可以提醒充值金币，没有金币退出游戏，或者主动退出游戏。
5. 退出游戏打印剩余金币及游玩次数。
"""
import random


def play_game(guess):
    a = random.randint(1, 6)
    b = random.randint(1, 6)
    if guess == '大':
        return (a + b) > 6
    else:
        return (a + b) <= 6

def get_guess():
    guess = input('请输入猜测值（大/小）：')
    if guess not in ['大', '小']:
        print('输入值不为大或小，请重新输入...')
        return get_guess()
    return guess


def add_coins(coins):
    coins_inc = input('请输入充值金额（1元换兑2个金币）：')
    coins_inc = coins_inc.rstrip('元').strip()
    if coins_inc.isdigit():
        coins_inc = int(coins_inc) * 2
    else:
        print('输入金额有误，请重新输入...')
        return add_coins(coins)
    return coins + coins_inc


if __name__ == '__main__':
    count = 0
    coins = 0
    play = input('是否开始玩游戏（Y/N）？')
    while True:
        if coins < 5 and play[0].lower() == 'y':
            coins_is_add = input(f'当前金币{coins}，是否充值金币（Y/N）？')
            if coins_is_add[0].lower() != 'y':
                play = 'n'
            else:
                coins = add_coins(coins)
                print(f'充值成功，剩余金币：{coins}。')
        if play[0].lower() != 'y':
            print(f'感谢游玩，剩余金币：{coins}，共玩了{count}局。')
            break
        coins -= 5
        your_guess = get_guess()
        result = play_game(your_guess)
        count += 1
        if result:
            coins += 2
            print(f'恭喜猜对，剩余金币：{coins}。')
        else:
            print(f'很遗憾，剩余金币：{coins}。')
        play = input('是否继续游玩（Y/N）？')
