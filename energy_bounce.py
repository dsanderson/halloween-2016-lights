import comms, audio, ui
import colorsys, time, sys

def update_colors(is_beat,i,direc,vis,fps):
    if is_beat:
        if i==0 or i==7:
            direc = direc*-1
        i+=direc
    current_hue = max([colorsys.rgb_to_hsv(*s)[0] for s in vis.state])
    v = 1.0/fps
    new_hue = (current_hue+v)%1.0
    new_colors = [(0.0,0.0,0.0) for h in xrange(8)]
    new_colors[i]=colorsys.hsv_to_rgb(new_hue,1.0,1.0)
    vis.state = new_colors
    if not disp:
		print vis.state
    vis.write_state()
    return i, direc

def is_beat(energies, energy):
    thresh = 2
    avg_energy = sum(energies)/float(len(energies))
    var_energy = sum((e-avg_energy)**2 for e in energies)/float(len(energies))
    var_e = (energy-avg_energy)**2
    var_prev = (energies[-1]-avg_energy)**2
    if var_energy == 0.0:
        return False
    #if not disp:
    #    print var_energy,var_e/var_energy,var_prev/var_energy
    if ((var_prev/var_energy)<thresh) and ((var_e/var_energy)>thresh):
        if not disp:
            print True
        return True
    else:
        return False

if __name__ == '__main__':
    disp = True
    vis = comms.Visualizer(debug=False)
    rec = audio.Recorder(sample_size=100)
    fps = 106.0
    spf = 1.0/fps
    bar_i = 1
    direc = 1
    n_energies = 20
    energies = [0.0 for i in xrange(n_energies)]
    if disp:
        display = ui.Display()
    while True:
        buff = ''
        sys.stdin.flush()
        while len(buff)<1000:
            buff += sys.stdin.read(1)
        #if len(buff)>100:
        #    buff = buff[-100:]
        rec.update_samples(buff)
        time_0 = time.time()
        avg_energy = sum(energies)/float(n_energies)
        var_energy = sum((e-avg_energy)**2 for e in energies)/float(n_energies)
        energy = rec.get_energy()

        b = is_beat(energies, energy)
        bar_i, direc = update_colors(b,bar_i,direc,vis,fps)

        var_e = (energy-avg_energy)**2
        energies = energies[1:]
        energies.append(energy)
        spectrogram = [0.5,var_e/(0.001+2.0*var_energy),0,0,0,0,0,0]
        l=0
        if disp:
            display.draw_state(fps,vis,spectrogram,l,bar_i)
        #print vis.state
        #limit frame rate
        #while fps>110:
        time_1 = time.time()
        time_diff = time_1-time_0
        #if time_diff>0.0:
        #    time.sleep(spf-time_diff)
        fps = 1.0/time_diff
        #time_0 = time_1
