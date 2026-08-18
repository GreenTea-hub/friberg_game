import random
import sqlite3

def get_all_players():
    conn = sqlite3.connect('players.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("select * from players")
        players = cursor.fetchall()
        return players
    finally:
        conn.close()

def pick_target(players):
    return random.choice(players)

def compare(guess, target):
    result = {}
    #姓名相同为绿 不同为灰
    if guess['name'] == target['name']:
        result['name'] = 'green'
    else:
        result['name'] = 'grey'

    #国家相同为绿 国家不同地区相同为黄 地区不同为灰
    if guess['country'] == target['country']:
        result['country'] = 'green'
    elif guess['region'] == target['region']:
        result['country'] = 'yellow'
    else:
        result['country'] = 'grey'

    #队伍相同为绿 不同为灰
    if guess['team'] == target['team']:
        result['team'] = 'green'
    else:
        result['team'] = 'grey'

    #年龄相同为绿 +-2为黄 其他为灰
    result['age'] = compare_number(guess['age'], target['age'])

    #位置相同为绿 不同为灰
    if guess['position'] == target['position']:
        result['position'] = 'green'
    else :
        result['position'] = 'grey'

    #major冠军数相同为绿 +-1为黄 其他为灰
    result['champions'] = compare_number(guess['champions'], target['champions'],1)

    #major参加次数相同为绿 +-2为黄 其他为灰
    result['majors'] = compare_number(guess['majors'], target['majors'])

    return result

def compare_number(guess_val,target_val,tolerance = 2):#tolerance默认值为2 可以改
    if guess_val == target_val:
        return{'digit':guess_val,'color':'green','direction':None}
    return {
        #绝对值不大于tolerance为黄 其他为灰
        'digit': guess_val,
        'color': 'yellow' if abs(guess_val - target_val) <= tolerance else 'grey',
        'direction': 'down' if guess_val > target_val else 'up',
    }

def is_win(guess,target):
    return guess['name'] == target['name']

def find_player_by_name(players, name):
    #在选手列表里按名字查找，找不到返回 None
    for p in players:
        if p['name'].lower() == name.lower():   # lower() 忽略大小写
            return p
    return None

def game():
    players = get_all_players()
    target = pick_target(players)
    count = 0
    while count < 8:
        guess_name = input('Guess Player: ')
        guess = find_player_by_name(players, guess_name)
        if guess is None:
            print("Invalid Name")
            continue
        if is_win(guess,target):
            print('You Win')
            break
        result = compare(guess, target)
        print(result)
        print(f'你还有{7-count}次机会')
        count += 1
    if count == 8:
        print(f"Game Over,the true answer is:{target['name']}")

if __name__ == '__main__':
    game()