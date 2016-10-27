import curses, atexit, colorsys

class Display():
    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self.screen.keypad(1)
        #set up colors-go with increments of 60
        hues = {0.0:curses.COLOR_RED, 180.0/360.0:curses.COLOR_CYAN, 120.0/360.0:curses.COLOR_GREEN,
            60.0/360.0:curses.COLOR_YELLOW, 240.0/360.0:curses.COLOR_BLUE, 300.0/360.0:curses.COLOR_MAGENTA, 1.0:curses.COLOR_RED}
        #hues = {}
        hue_keys = hues.keys()
        hue_keys.sort()
        for i,h in enumerate(hue_keys):
            pass
            curses.init_pair(i+1,curses.COLOR_BLACK,hues[h])
        atexit.register(curses.endwin)
        atexit.register(curses.echo)
        atexit.register(self.screen.keypad, 0)
        atexit.register(curses.nocbreak)

    def draw_state(self, fps, vis, spectrogram, frame_len):
        #self.screen.clear()
        #self.screen.border()
        self.screen.addstr(2,2,"Spectrogram Visualizer")
        self.screen.addstr(3,2,"Currently at {} fps".format(int(fps)))
        self.screen.addstr(4,2,"Frame len {}".format(frame_len))
        bar_x = 2
        bar_spacing = 3
        bar_y = 15
        bar_height = 10
        for i, c in enumerate(vis.state):
            h = colorsys.rgb_to_hsv(*c)[0]
            #round color to nearest existing shade
            hi = int(h*6+0.5)
            for j in xrange(bar_height):
                #pass
                y = int(bar_y-j)
                x = int(bar_x+bar_spacing*i)
                self.screen.addstr(y,x," ",curses.color_pair(hi+1))
            spec_height = int(bar_height*min([spectrogram[i],1.0]))
            for k in xrange(bar_height):
                y = int(bar_y-k)
                x = int(bar_x+bar_spacing*i+1)
                if k<spec_height:
                    self.screen.addstr(y,x," ",curses.color_pair(3))
                else:
                    self.screen.addstr(y,x," ",curses.color_pair(0))
        self.screen.refresh()
