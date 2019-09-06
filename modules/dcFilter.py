#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu Sep  5 14:43:22 2019
##################################################


from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import correctiq


class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
   

        ##################################################
        # Blocks
        ##################################################
        self.correctiq_correctiq_0 = correctiq.correctiq()
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_float*1, '/dev/shm/dataI.dat', False)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_float*1, '/dev/shm/dataR.dat', False)
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_float*1, '/dev/shm/fdataI.dat', False)
        self.blocks_file_sink_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_float*1, '/dev/shm/fdataR.dat', False)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_imag_0 = blocks.complex_to_imag(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_imag_0, 0), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_float_to_complex_0, 0), (self.correctiq_correctiq_0, 0))
        self.connect((self.correctiq_correctiq_0, 0), (self.blocks_complex_to_imag_0, 0))
        self.connect((self.correctiq_correctiq_0, 0), (self.blocks_complex_to_real_0, 0))



def dcFilter(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    dcFilter()
