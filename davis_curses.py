import curses
import sys

class StdOutWrapper:
    text = ''
    def write(self,txt):
        self.text += txt
        self.text = '\n'.join(self.text.split('\n')[-30:])
    def get_text(self,beg,end):
        return '\n'.join(self.text.split('\n')[beg:end])

class Curses_Wrapper:
    def __init__(self, scr, displays_shape=(1,1), command_callback=None):
        self.displays = []
        self.displays_shape = displays_shape
        self.written_text = ''
        self.command_callback = command_callback

        self.display_width = (curses.COLS-1)/(displays_shape[0])
        self.display_height = (curses.LINES-1)/(displays_shape[1])

        for x in self.displays_shape[0]:
            x_coord = x * self.display_width
            d = []
            for y in self.displays_shape[1]:
                y_coord = y * display_height
                d += [scr.dewin(display_height, display_width, y, x)]
            self.displays += d

        mystdout = StdOutWrapper()
        sys.stdout = mystdout
        sys.stderr = mystdout

    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def refresh(self):
        for i in displays:
            i.refresh()

    def clear(self):
        for i in displays:
            i.clear()

    def getkey(self):
        while(True):
            try:
                char = scr.getkey()
                if(ord(char) == 8):
                    # delete
                    self.written_text = self.written_text[:-1]
                elif(char == '\n' and command_callback):
                    self.command_callback(self.written_text)
                    self.written_text = ''
                else:
                    self.written_text += char
            except:
                break
