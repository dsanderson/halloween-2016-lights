import comms, audio, ui
import colorsys, time, sys

def strobe(rate,t_old,vis,cols,mode):
	t_new = time.time()
	if t_new-t_old>1.0/float(rate):
		mode += 1
		mode = mode%len(cols)
		c = cols[mode]
		vis.state = [c for i in xrange(8)]
		vis.write_state()
		return t_new, mode
	else:
		return t_old, mode

if __name__ == '__main__':
    disp = False
    vis = comms.Visualizer(debug=False)
    t_old = time.time()
    rate = 2000/60#Hz
    cols = [(0.0,0.0,1.0),(1.0,0.0,0.0)]
    mode = 0
    while True:
        t_old, mode = strobe(rate,t_old,vis,cols,mode)
        #time_0 = time_1

