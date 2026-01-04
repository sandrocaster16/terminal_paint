import os
import time
import random
import sys
import tty
import termios

class Game():
    def __init__(self):
        #               off|cursor|on|cursor&on
        self.pixel_symbols = ["░░","▒▒","▓▓","  "]
        self.pixel_on = set()

        self.cursor_x = 0
        self.cursor_y = 0
        self.cursor_on = True    # cursor visible
        self.isRunning = True    # while true

        self.max_X, self.max_Y = self.get_terminal_size()
        # slicing
        self.max_Y=self.max_Y
        self.max_X=int(self.max_X/2)

    # unix only
    def get_terminal_size(self):
        try:
            size = os.get_terminal_size()
            return size.columns, size.lines
        except OSError:
            return None

    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def print_pixels(self):
        for i in range(0, self.max_Y):
            for j in range(0, self.max_X):
                if j == self.cursor_x and i == self.cursor_y and self.cursor_on and (j, i) in self.pixel_on:
                    print(self.pixel_symbols[3], end="")
                elif j == self.cursor_x and i == self.cursor_y and self.cursor_on:
                    print(self.pixel_symbols[1], end="")
                elif (j, i) in self.pixel_on:
                    print(self.pixel_symbols[2], end="")
                else:
                    print(self.pixel_symbols[0], end="")

    def parse_input(self, qwe):
        # movement
        if (qwe == 'w'):
            if (self.cursor_y-1 < 0):
                self.cursor_y = self.max_Y-1
            else:
                self.cursor_y = self.cursor_y-1
        elif (qwe == 'a'):
            if (self.cursor_x-1 < 0):
                self.cursor_x = self.max_X-1
            else:
                self.cursor_x = self.cursor_x-1
        elif (qwe == 's'):
            if (self.cursor_y+1 > self.max_Y-1):
                self.cursor_y = 0
            else:
                self.cursor_y = self.cursor_y+1
        elif (qwe == 'd'):
            if (self.cursor_x+1 > self.max_X-1):
                self.cursor_x = 0
            else:
                self.cursor_x = self.cursor_x+1

        # hide/show cursor
        elif (qwe == 'f'):
            self.cursor_on = not self.cursor_on

        # set pixel
        elif (qwe == ' '):
            if ((self.cursor_x, self.cursor_y) in self.pixel_on):
                self.pixel_on.remove((self.cursor_x, self.cursor_y))
            else:
                self.pixel_on.add((self.cursor_x, self.cursor_y))

        # exit
        elif (qwe == 'q'):
            sys.stdout.write('\033[?25h')   # show terminal's cursor
            sys.stdout.write('\033[0m')
            sys.stdout.flush()
            self.isRunning = False


    def run(self):
        sys.stdout.write('\033[2J\033[H')   # hide terminal's cursor
        sys.stdout.write('\033[?25l')
        sys.stdout.flush()

        while self.isRunning:
            # print
            self.print_pixels()

            sys.stdout.write('\033[H')
            sys.stdout.flush()

            # input
            c = self.getch()

            self.parse_input(c)


#start
if __name__ == "__main__":
    game = Game()
    game.run()
