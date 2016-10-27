import alsaaudio
from struct import unpack
import numpy as np
import math

class Recorder():
    def __init__(self,device_name=None,verbose=False):
        if device_name==None:
            device_name='default'
        if verbose:
            print "Initializing recoding device '{}'".format(device_name)
        self.device = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE,mode=alsaaudio.PCM_NONBLOCK,device=device_name)
        self.device.setchannels(1)
        self.rate = 44100
        self.sample_size = 22000#44100
        self.device.setperiodsize(100)
        self.samples = []
        self.load_data()

    def update_samples(self):
        frame = self.device.read()
        if frame[0]==0:
            return False
        data = unpack('<'+'h'*frame[0],frame[1])
        data = [d/float(2^16) for d in data]
        for datum in data:
            self.samples.append(datum)
        if len(self.samples)>self.sample_size:
            self.samples = self.samples[-1*self.rate:]
            #print len(self.samples)
        return True

    def load_data(self):
        while not len(self.samples)>=self.sample_size:
            updated = self.update_samples()

    def get_spectrum(self):
        updated = self.update_samples()
        fft = np.fft.fft(self.samples)
        #normalize
        fft = fft/float(len(self.samples))
        #drop samples less than 200Hz
        fft = fft[:len(fft)/2]
        dt = 1.0/self.rate
        df = 1.0/(dt*len(self.samples))
        fft_200_i = int(200/df)#hardcoded index of 200Hz bucket
        fft = fft[fft_200_i:]#[100:]
        fft = fft.real
        #scale
        fft = fft/10.0
        #fold the fft into the maxes of 8 buckets
        size = len(fft)/8.0
        buckets = []
        i = 0
        while i<len(fft):
            buckets.append(max(fft[i:min([i+size,len(fft)-1])]))
            i+=size
        return buckets

def test_Recorder():
    r = Recorder(verbose=True)
    d = r.get_spectrum()
    print len(d), d
    #print d
    #f = r.get_spectrum()
    #print f[0]
    #print f[1]

if __name__ == '__main__':
    test_Recorder()
