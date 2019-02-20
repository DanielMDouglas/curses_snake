import curses as crs
from time import sleep
import numpy as np

stdscr = crs.initscr()
crs.start_color()
crs.noecho()
crs.cbreak()
stdscr.keypad(1)
stdscr.nodelay(1)
crs.curs_set(0)

crs.init_pair(1, crs.COLOR_RED, crs.COLOR_WHITE)
crs.init_pair(2, crs.COLOR_GREEN, crs.COLOR_BLACK)
crs.init_pair(3, crs.COLOR_BLUE, crs.COLOR_GREEN)
crs.init_pair(4, crs.COLOR_GREEN, crs.COLOR_RED)

maxHeight, maxWidth = stdscr.getmaxyx()

gameOver = False
gameQuit = False

class coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return coord(self.x + other.x, self.y + other.y)
    def __mul__(self, other):
        return coord(other*self.x, other*self.y)
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)
    
class snake:
    def __init__(self, pos, length=1):
        self.length = length
        self.segments = [pos]
    def update(self, direction, ate=False):
        global gameOver
        head = self.segments[0] + direction
        if ate:
            tail = self.segments[:]
            self.length += 1
        else:
            tail = self.segments[:-1]
        if (head in tail) or head.x < 0 or head.y < 0 or head.x >= maxWidth or head.y >= maxHeight-3 :
            gameOver = True
        else:
            self.segments = [head] + tail

    def draw(self):
        for i, seg in enumerate(self.segments):
            if i:
                char = '/'
            else:
                char = '8'
            stdscr.addstr(seg.y, seg.x, char, crs.color_pair(1))
            
class food:
    def __init__(self):
        self.pos = coord(np.random.randint(maxWidth), np.random.randint(maxHeight-3))
    def draw(self):
        stdscr.addstr(self.pos.y, self.pos.x, '*', crs.color_pair(4))
    def respawn(self, snake):
        randPoint = coord(np.random.randint(maxWidth), np.random.randint(maxHeight-3))
        while randPoint in snake.segments:
            randPoint = coord(np.random.randint(maxWidth), np.random.randint(maxHeight-3))
        
        self.pos = randPoint

def formatString(string, pad = " "):
    if int(string) / 100 == 0:
        string = pad + string
        if int(string) / 10 == 0:
            string = pad + string
    return string
        
class scoreboard:
    def draw(self, snake, time):
        score = formatString(str(snake.length - 1))
        tcount = formatString(str(int(time)))
                
        stdscr.addstr(maxHeight-3, 0, maxWidth*"=", crs.color_pair(2))
        stdscr.addstr(maxHeight-2, 0, "Score: " + score + (maxWidth-20)*" " + "Time: " + tcount + " ", crs.color_pair(3))
        stdscr.addstr(maxHeight-1, 0, (maxWidth-1)*"_", crs.color_pair(3))
        
if __name__ == '__main__':
    while not gameQuit:
        player = snake(coord(maxWidth/2, maxHeight/2))
        direction = coord(1, 0)

        nom = food()
        sc = scoreboard()

        t = 0
        dt = 0.1

        while not gameOver:
            ate = False
        
            c = stdscr.getch()
            if c == ord('w'):
                if not direction == coord(0, 1):
                    direction = coord(0, -1)
                    dt = 0.1
            elif c == ord('a'):
                if not direction == coord(1, 0):
                    direction = coord(-1, 0)
                    dt = 0.07
            elif c == ord('s'):
                if not direction == coord(0, -1):
                    direction = coord(0, 1)
                    dt = 0.1
            elif c == ord('d'):
                if not direction == coord(-1, 0):
                    direction = coord(1, 0)
                    dt = 0.07
            elif c == ord('q'):
                crs.nocbreak()
                stdscr.keypad(0)
                crs.echo()
                crs.endwin()
                gameQuit = True
                break
                
            if nom.pos == player.segments[0]:
                nom.respawn(player)
                ate = True
            
            stdscr.erase()
            player.update(direction, ate)
            player.draw()
            nom.draw()
            sc.draw(player, t)
            stdscr.refresh()
        
            sleep(dt)
            
            t += dt

        while gameOver:
            stdscr.addstr(maxHeight/2 - 2, maxWidth/2 - 5, "GAME OVER", crs.color_pair(3))
            stdscr.addstr(maxHeight/2 - 1, maxWidth/2 - 7, "r -  new game", crs.color_pair(3))
            stdscr.addstr(maxHeight/2, maxWidth/2 - 5, "q -  quit", crs.color_pair(3))
            stdscr.refresh()

            c = stdscr.getch()
            if c == ord('r'):
                gameOver = False
            elif c == ord('q'):
                crs.nocbreak()
                stdscr.keypad(0)
                crs.echo()
                crs.endwin()
                gameQuit = True
                break
                
            sleep(dt)
