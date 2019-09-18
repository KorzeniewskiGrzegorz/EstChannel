#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri Jun 21 12:43:33 2019
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time
from threading import Timer
import threading



class top_block(gr.top_block):

    def __init__(self,sr,fr,bw):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = sr
        self.freq = freq = fr
        self.bandwidth = bandwidth = bw
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
        self.osmosdr_source_1.set_gain(25, 0)
        self.osmosdr_source_1.set_if_gain(0, 0)
        self.osmosdr_source_1.set_bb_gain(0, 0)
        self.osmosdr_source_1.set_antenna('RX', 0)
        self.osmosdr_source_1.set_bandwidth(bandwidth, 0)

        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_float*1, '/dev/shm/dataI.dat', False)
        self.blocks_file_sink_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_float*1, '/dev/shm/dataR.dat', False)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_imag_0 = blocks.complex_to_imag(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_imag_0, 0), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_complex_to_imag_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_complex_to_real_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_1.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_1.set_center_freq(self.freq, 0)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.osmosdr_source_1.set_bandwidth(self.bandwidth, 0)



def blader_Rx(sr,fr,bw,e,top_block_cls=top_block, options=None):

    tb = top_block_cls(sr,fr,bw)
    tb.start()

    start=time.time()

    def finish(e):
        end = time.time()
        print "\n"
        print "%"*40
        print("transmission time: \t"+str(end-start)+"s")
        print("\tsamp rate: \t"+str(tb.samp_rate)+" samples/s")
        print("\tcarr freq: \t"+str(tb.freq)+"Hz")
        print("\tbandwidth: \t"+str(tb.bandwidth)+"Hz")
        print "%"*40
        print "\n"
        tb.stop()
        tb.wait()
        e.set()
        

    t = Timer(3, finish, [e])
    t.start() # after 30 seconds, "hello, world" will be printed    


if __name__ == '__main__':
    
    Fs = 20e6
    Fr = 2.17e9
    bw = 1.5e6

    

    result_available = threading.Event()
    thread = threading.Thread(target=blader_Rx, args=(Fs,Fr,bw,result_available,))
    thread.start()
    print("transmitting...")
    result_available.wait()