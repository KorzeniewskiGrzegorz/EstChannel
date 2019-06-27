import sys
import numpy as np 
import matplotlib.pyplot as plt




def whiteNoiseGen(Fs,R =0.99,segundos = 1,path ='/dev/shm/'):

	pulseLen = int(Fs*segundos)
	IPulse = np.zeros(int(Fs*segundos))

	IPulse[0:int(Fs*segundos- Fs*segundos*(1-R))] = np.random.randn(1,int(Fs*segundos - Fs*segundos*(1-R)))


	QPulse = np.zeros(int(Fs*segundos))

	#t=np.linspace(0, segundos, num=pulseLen)

	#plt.plot(t,IPulse,'b',t,QPulse,'r')
	#plt.show()



	IPulse.astype('float32').tofile(path + 'IPulse.dat')
	QPulse.astype('float32').tofile(path + 'QPulse.dat')
	print("whiteNoiseGen - Done")
	print("Created files to path "+path)

##############################################################3
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import correctiq
import osmosdr
import time
from threading import Timer


class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 20e6
        self.freq = freq = 2400e6
        self.bandwidth = bandwidth = 1.5e6

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_1 = osmosdr.source( args="numchan=" + str(1) + " " + "bladerf=179" )
        self.osmosdr_source_1.set_sample_rate(samp_rate)
        self.osmosdr_source_1.set_center_freq(freq, 0)
        self.osmosdr_source_1.set_freq_corr(0, 0)
        self.osmosdr_source_1.set_dc_offset_mode(0, 0)
        self.osmosdr_source_1.set_iq_balance_mode(0, 0)
        self.osmosdr_source_1.set_gain_mode(True, 0)
        self.osmosdr_source_1.set_gain(15, 0)
        self.osmosdr_source_1.set_if_gain(0, 0)
        self.osmosdr_source_1.set_bb_gain(0, 0)
        self.osmosdr_source_1.set_antenna('RX', 0)
        self.osmosdr_source_1.set_bandwidth(bandwidth, 0)

        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "bladerf=32a" )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(25, 0)
        self.osmosdr_sink_0.set_if_gain(0, 0)
        self.osmosdr_sink_0.set_bb_gain(0, 0)
        self.osmosdr_sink_0.set_antenna('TX', 0)
        self.osmosdr_sink_0.set_bandwidth(bandwidth, 0)

        self.correctiq_correctiq_0 = correctiq.correctiq()
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_float*1, '/dev/shm/QPulse.dat', True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_float*1, '/dev/shm/IPulse.dat', True)
        self.blocks_file_sink_0_0_0_0_0_0 = blocks.file_sink(gr.sizeof_float*1, '/dev/shm/ruidoR.dat', False)
        self.blocks_file_sink_0_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0_0 = blocks.file_sink(gr.sizeof_float*1, '/dev/shm/ruidoI.dat', False)
        self.blocks_file_sink_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_float*1, '/dev/shm/dataI.dat', False)
        self.blocks_file_sink_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_float*1, '/dev/shm/dataR.dat', False)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_imag_0 = blocks.complex_to_imag(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_file_sink_0_0_0_0_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_file_sink_0_0_0_0_0_0, 0))
        self.connect((self.blocks_complex_to_imag_0, 0), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.correctiq_correctiq_0, 0), (self.blocks_complex_to_imag_0, 0))
        self.connect((self.correctiq_correctiq_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.correctiq_correctiq_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_1.set_sample_rate(self.samp_rate)
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_1.set_center_freq(self.freq, 0)
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.osmosdr_source_1.set_bandwidth(self.bandwidth, 0)
        self.osmosdr_sink_0.set_bandwidth(self.bandwidth, 0)


def blader(e, top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.start()
   
    start=time.time()

    def finish(e):
        end = time.time()
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("transmission time: \t"+str(end-start)+"s")
        print("\tsamp rate: \t"+str(tb.samp_rate)+" samples/s")
        print("\tcarr freq: \t"+str(tb.freq)+"Hz")
        print("\tbandwidth: \t"+str(tb.bandwidth)+"Hz")
        tb.stop()
        tb.wait()
        e.set()
        

    t = Timer(4, finish, [e])
    t.start() # after 30 seconds, "hello, world" will be printed     


##########################################################################


from offcalc import offcalc

def dataProcess(Fs , #Sample freq
	R = 0.99, # ratio, the same as in generator script
	calibrationOffsetTime = 1,# calibration time [s] , corresponds to parameters of signal generation
	offman = 0,
	wd = 10,
	path = "/dev/shm/",
	offsetThreshold = 0.003,
	offsetTime = 0.1):


	#%%%%%%%%%5%%%%%%%%%%%%%
	ruidoR = np.fromfile(path + "ruidoR.dat",'float32')
	ruidoI = np.fromfile(path + "ruidoI.dat",'float32')
	ruidoC = ruidoR + 1j * ruidoI
	del ruidoR,ruidoI

	dataR = np.fromfile(path + "dataR.dat",'float32')
	dataI = np.fromfile(path + "dataI.dat",'float32')
	dataC = dataR + 1j * dataI
	del dataR,dataI

	lenRRaw=len(ruidoC)
	lenDRaw=len(dataC)



	offset = offcalc(dataC.real,Fs,0.003,0.05)

	#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	#Calibration processing


	F = 1/calibrationOffsetTime
	calibrationOffset = calibrationOffsetTime * Fs  #conversion from time to samples




	# signal calibration
	offset =(-1) *(offcalc(dataC.real,Fs,offsetThreshold,offsetTime))-offman  #received samples offset due to hardware & software lag [samples];

	ruidoC = ruidoC[ int(calibrationOffset)    :    int(calibrationOffset*2-(Fs/F)*(1-R)) ];
	#print(ruidoC[int(calibrationOffset)])
	#print(ruidoC[int(calibrationOffset)-1])
	#print(ruidoC[int(calibrationOffset*2-(Fs/F)*(1-R))])
	#print(ruidoC[int(calibrationOffset*2-(Fs/F)*(1-R))-1])

	dataC = dataC[int(calibrationOffset+offset)    :    int(calibrationOffset*2-(Fs/F)*(1-R) +offset)  ];

	#plt.plot(dataC.real)
	#plt.show()

	lenR=len(ruidoC)
	lenD=len(dataC)


	#TODO
	#calibrated data plotting


	N=int( wd*Fs/1000000) # conversion of window duration from miliseconds to samples

	v=int(np.floor(lenD/N)) # number of pulses recorded
	PA = np.zeros((v,N)) + 1j * np.zeros((v,N))


	for i in range(0,v):# Run cross correlation for v times
	    
		x=ruidoC[int(i*N) : int(i*N+N)] #TX
		y=dataC[int(i*N)  : int(i*N+N)] # RX
		
		rxy=np.correlate( x, np.conj(y) , 'full' ) # Cross correlation of the TX and RX conjugated data
		Ryx=np.flip(rxy[0:N],0) # Flip the correlation result and take the first N samples (Ryx(t) = Rxy(-t)
		PA[i] = Ryx

	Ryx = PA.mean(axis=0)

	plt.plot(np.abs(Ryx))
	plt.show()



