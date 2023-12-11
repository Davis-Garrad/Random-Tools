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
        scr.timeout(1)

        self.displays = []
        self.boxes = []
        self.displays_shape = displays_shape
        self.written_text = ''
        self.command_callback = command_callback

        self.display_width = (curses.COLS-1)//(displays_shape[0])
        self.display_height = (curses.LINES-1)//(displays_shape[1])

        for x in range(self.displays_shape[0]):
            x_coord = x * self.display_width
            d = []
            for y in range(self.displays_shape[1]):
                y_coord = y * self.display_height
                self.boxes += [scr.subwin(self.display_height, self.display_width, y_coord, x_coord)]
                d += [scr.subwin(self.display_height-2, self.display_width-2, y_coord+1, x_coord+1)]
            self.displays += [d]

    def refresh(self):
        for i in self.boxes:
            i.box('|', '-')
            i.refresh()
        for i in [ item for sublist in self.displays for item in sublist ]:
            i.refresh()

    def clear(self):
        for i in self.boxes:
            i.erase()
        for i in [ item for sublist in self.displays for item in sublist ]:
            i.erase()

    def print(self, text, window_coords):
        '''Adds text to a window at (window_coords) (2-tuple)'''
        self.displays[window_coords[0]][window_coords[1]].addstr(text)

    def set_text(self, text, window_coords):
        self.displays[window_coords[0]][window_coords[1]].erase()
        self.displays[window_coords[0]][window_coords[1]].addstr(text)

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
