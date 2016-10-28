import comms, audio, ui
import colorsys, time, sys

def update_colors(spectrogram,vis,fps):
    current_hues = [colorsys.rgb_to_hsv(*s)[0] for s in vis.state]
    #scale = 11796480000.0/(2*fps)#2*2^16
    scale = (2*fps)
    scale_i = [0.2,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
    vel = [scale_i[i]*s*(i+1)/float(scale) for i, s in enumerate(spectrogram)]
    if not disp:
        print spectrogram
    new_hues = [(h+vel[i])%1.0 for i, h in enumerate(current_hues)]
    new_colors = [colorsys.hsv_to_rgb(h,1.0,1.0) for h in new_hues]
    vis.state = new_colors
    vis.write_state()
    return scale

if __name__ == '__main__':
    disp = False
    vis = comms.Visualizer(debug=False)
    rec = audio.Recorder()
    fps = 106.0
    spf = 1.0/fps
    if disp:
        display = ui.Display()
    while True:
        buff = ''
        sys.stdin.flush()
        while len(buff)<100:
            buff += sys.stdin.read(1)
        #if len(buff)>100:
        #    buff = buff[-100:]
        rec.update_samples(buff)
        time_0 = time.time()
        spectrogram, l = rec.get_spectrum()
        scale = update_colors(spectrogram,vis,fps)
        if disp:
            display.draw_state(fps,vis,spectrogram,l)
        #print vis.state
        #limit frame rate
        #while fps>110:
        time_1 = time.time()
        time_diff = time_1-time_0
        #if time_diff>0.0:
        #    time.sleep(spf-time_diff)
        fps = 1.0/time_diff
        #time_0 = time_1
