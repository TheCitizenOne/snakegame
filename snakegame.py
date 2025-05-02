# Snake game by citizen
import curses
import time
import random

class Menu:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.title = "SnakeGame by citizen"
        self.comment = "Press '1' to play, '2' to quit"

        stdscr.clear()
        curses.curs_set(0)
        self.interface()

    def interface(self):
        self.stdscr.addstr((self.height - 6)//2, (self.width - len(self.title))//2, self.title)
        self.stdscr.addstr((self.height - 6)//2 + 1, (self.width - len(self.comment))//2, self.comment)
        self.stdscr.refresh()
        
        while True:
            key = self.stdscr.getch()

            if key == ord('1'):
                Gameplay(self.stdscr)
                break
            elif key == ord('2'):
                break

class Gameplay:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.y = self.height // 2
        self.x = self.width // 2
        self.direction = "RIGHT"
        self.bait = "@"
        self.options = "'p': Pause, 'q': Quit"
        self.score = 0
        self.snake_body = [(self.y, self.x)]
        self.prev_body = []
        self.speed = 120
        self.paused = False

        curses.curs_set(0)
        stdscr.nodelay(1)
        stdscr.timeout(self.speed)
        self.gameplay()

    def game_interface(self):
        self.stdscr.addstr(0, 2, f"Score: {self.score} points")
        self.stdscr.addstr(0, self.width - (len(self.options)) - 2, self.options)
        try:
            for i in range(2, self.width - 2):
                self.stdscr.addstr(1, i, "═")
                self.stdscr.addstr(self.height - 2, i, "═")

            for i in range(2, self.height - 2):
                self.stdscr.addstr(i, 1, "║")
                self.stdscr.addstr(i, self.width - 2, "║")
        except curses.error:
            pass

    def baitgen(self):
        self.baity = random.randrange(2, self.height - 2)
        self.baitx = random.randrange(2, self.width - 2)

        while (self.baity, self.baitx) in self.snake_body:
            self.baity = random.randrange(2, self.height - 2)
            self.baitx = random.randrange(2, self.width - 2)

        self.stdscr.addstr(self.baity, self.baitx, self.bait)
        
    def draw_snake(self):
        if len(self.snake_body) > len(self.prev_body):
            pass
        elif len(self.snake_body) > 0 and len(self.prev_body) > 0:
            last_y, last_x = self.prev_body[-1]
            self.stdscr.addstr(last_y, last_x, " ")

        if self.snake_body:
            head_y, head_x = self.snake_body[0]
            self.stdscr.addstr(head_y, head_x, "#")

        self.stdscr.addstr(0, 2, f"Score: {self.score} points")

    def handle_pause(self):
        self.paused = not self.paused

        if self.paused:
            pause_msg = "GAME PAUSED - Press 'p' to resume or 'q' to quit"
            self.stdscr.addstr(self.height//2, (self.width-len(pause_msg))//2, pause_msg)
            self.stdscr.refresh()

            self.stdscr.nodelay(0)

            while True:
                key = self.stdscr.getch()
                if key == ord('p'):
                    self.stdscr.addstr(self.height//2, (self.width-len(pause_msg))//2, " "*len(pause_msg))
                    break
                elif key == ord('q'):
                    return False

            self.stdscr.nodelay(1)
            self.stdscr.timeout(self.speed)

        return True
        
    def gameplay(self):
        self.stdscr.clear()
        self.game_interface()
        self.baitgen()

        for segment in self.snake_body:
            self.stdscr.addstr(segment[0], segment[1], "#")
        self.stdscr.refresh()
        
        while True:
            key = self.stdscr.getch()

            if key == ord('w') and self.direction != 'DOWN':
                self.direction = 'UP'
            elif key == ord('s') and self.direction != 'UP':
                self.direction = 'DOWN'
            elif key == ord('a') and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            elif key == ord('d') and self.direction != 'LEFT':
                self.direction = 'RIGHT'
            elif key == ord('q'):
                break
            elif key == ord('p'):
                if not self.handle_pause():
                    break
                

            self.prev_body = self.snake_body.copy()

            if self.direction == 'UP':
                self.y -= 1
            elif self.direction == 'DOWN':
                self.y += 1 
            elif self.direction == 'LEFT':
                self.x -= 1
            elif self.direction == 'RIGHT':
                self.x += 1

            if  self.y <= 1 or self.y >= self.height - 2 or self.x <= 1 or self.x >= self.width - 2:
                AfterGame(self.stdscr, self.score)
                break

            if (self.y, self.x) in self.snake_body:
                AfterGame(self.stdscr, self.score)
                break

            self.snake_body.insert(0, (self.y, self.x))
            
            if self.y == self.baity and self.x == self.baitx:
                self.score += 5
                self.speed = max(80, self.speed - 10)
                self.stdscr.timeout(self.speed)
                self.baitgen()
            else:
                self.snake_body.pop()

            self.draw_snake()
            
            self.stdscr.refresh()

class AfterGame:
    def __init__(self, stdscr, score):
        self.score = score
        self.hscore = 0
        self.game_over = "Game over"
        self.is_new_hscore = self.save_high_score()
        self.score_msg = f"Your score: {self.score} points"
        self.hscore_msg = f"Highest score: {self.hscore} points"
        self.new_hscore_msg = "NEW HIGH SCORE!" if self.is_new_hscore else ""
        
        self.stdscr = stdscr
        self.height, self.width = self.stdscr.getmaxyx()

        self.stdscr.addstr((self.height - 2)//2, (self.width-len(self.game_over))//2, self.game_over)
        self.stdscr.addstr((self.height - 2)//2 + 1, (self.width-len(self.score_msg))//2, self.score_msg)
        self.stdscr.addstr((self.height - 2)//2 + 2, (self.width-len(self.hscore_msg))//2, self.hscore_msg)

        if self.is_new_hscore:
            self.stdscr.addstr((self.height - 3)//2 + 4, (self.width-len(self.new_hscore_msg))//2, self.new_hscore_msg)
    
        self.stdscr.refresh()
        time.sleep(3)

    def save_high_score(self):
        try:
            with open("hscore.txt", "r") as f:
                self.hscore = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            self.hscore = 0

        if self.score > self.hscore:
            self.hscore = self.score
            with open("hscore.txt", "w") as f:
                f.write(str(self.hscore))
            return True
        return False
    

if __name__ == "__main__":
    curses.wrapper(Menu)
