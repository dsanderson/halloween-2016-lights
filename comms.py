import serial, copy
import serial.tools.list_ports

class Visualizer():
    def __init__(self,debug=False):
        self.debug = debug
        if not self.debug:
            ports = list(serial.tools.list_ports.comports())
            for p in ports:
                print p
                if "Arduino" in p[2] or "2341:0042" in p[2]:
                    port_str = p[0]
            self.ser = serial.Serial(port_str, 38400)#'/dev/ttyACM0', 38400)
        else:
            print "Launching with debug comms"
        self.state = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
        self.old_state = copy.deepcopy(self.state)

    def write_state(self):
        to_write = self.diff_state()
        for bar in to_write:
            self.write_bar(bar[0],bar[1])
        self.show()

    def diff_state(self):
        diff = []
        for i in xrange(0, len(self.state)):
            if self.state[i] != self.old_state[i]:
                diff.append((i,self.state[i]))
        self.old_state = copy.deepcopy(self.state)
        return diff

    def write_bar(self,i,color):
        if not self.debug:
            self.ser.write(chr(i))
            self.ser.write(chr(int(255*color[0])))
            self.ser.write(chr(int(255*color[1])))
            self.ser.write(chr(int(255*color[2])))

    def zero_state(self):
        self.state = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]

    def show(self):
        if not self.debug:
            self.ser.write(chr(255))
            self.ser.write(chr(255))
            self.ser.write(chr(255))
            self.ser.write(chr(255))
