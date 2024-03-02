import curses
import random
import time

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)
curses.curs_set(0)

maxl = curses.LINES - 1
maxc = curses.COLS - 1
world = []
food = []
player_c = player_l = 0
enemy = []

score = 0
testing = False



def random_place():
    a = random.randint(0, maxl)
    b = random.randint(0, maxc)
    while world[a][b] != " ":
        a = random.randint(0, maxl)
        b = random.randint(0, maxc)
    
    return a, b

def init():
    global player_l , player_c

    for i in range(-1, maxl + 1):
        world.append([])
        for j in  range(-1, maxc + 1):
            world[i].append(' ' if random.random() > 0.018 else ".")

    for i in range(10):
        fl, fc = random_place()
        fa = random.randint(1000, 10000)
        food.append((fl, fc, fa))

    for i in range(4):
        el, ec = random_place()
        enemy.append((el, ec))

    player_l , player_c = random_place()

def draw():
    global score
    
    for i in range(maxl):
        for j in range(maxc):
            stdscr.addch(i, j, world[i][j])

    stdscr.addstr(1, 1, f"Score: {score}")
    # Showing the food
    for f in food:
        fl, fc, fa = f
        stdscr.addch(fl, fc, "★")

    # Showing the food
    for e in enemy:
        el, ec = e
        stdscr.addch(el, ec, "🐿")

    # Showing the Player
    stdscr.addstr(player_l, player_c, '✈')

    stdscr.refresh()

def in_range(a, min, max):
    if a > max:
        return max
    if a < min:
        return min
    return a


def move(c):
    """get one of aswd and moved toward that direction"""
    global player_l
    global player_c

    if c == 'w' and world[player_l - 1][player_c] != ".":
        player_l -= 1
    elif c == 's' and world[player_l + 1][player_c] != ".":
        player_l += 1
    elif c == 'a' and world[player_l][player_c - 1] != ".":
        player_c -= 1
    elif c == 'd' and world[player_l][player_c + 1] != ".":
        player_c += 1

    player_l = in_range(player_l, 0, maxl -1)
    player_c = in_range(player_c, 0, maxc - 1)


def check_food():
    global score 

    for i in range(len(food)):
        fl, fc, fa = food[i]
        fa -= 1
        if fl == player_l and fc == player_c:
            score += 10
            fl, fc = random_place()
            fa = random.randint(1000, 10000)
        if fa <= 0:
            fl, fc = random_place()
            fa = random.randint(1000, 10000)
        food[i] = (fl, fc, fa)


def move_enemy():
    global playing
    for i in range(len(enemy)):
        el, ec = enemy[i]
        if random.random() > 0.976:
            if el > player_l:
                el -= 1
        if random.random() > 0.976:
            if ec > player_c:
                ec -= 1
        if random.random() > 0.976:
            if el < player_l:
                el += 1
        if random.random() > 0.976:
            if ec < player_c:
                ec += 1

            el = in_range(el, 0, maxl - 1)
            ec = in_range(ec, 0, maxc - 1)
            enemy[i] = (el, ec)

        if el == player_l and ec == player_c and testing:
            stdscr.addstr(maxl//2, maxc//2, "YOU DIED")
            stdscr.refresh()
            time.sleep(5)
            playing = False
init()

playing= True
while playing:
    try:
        c = stdscr.getkey()
    except:
        c = ""

    if c in "awsd":
        move(c)
    elif c == 'q':
        playing = False  # Exit the while loop

    check_food()
    move_enemy()
    draw()

stdscr.clear()
stdscr.refresh()
