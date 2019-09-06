#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri Jun 21 12:43:33 2019
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import correctiq
import osmosdr
import sip
import sys
import time
from gnuradio import qtgui
from threading import Timer

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self,sr,bw):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = sr
        self.freq = freq = 2400e6
        self.bandwidth = bandwidth = bw

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)

        self.qtgui_sink_x_0.enable_rf_freq(False)



        self.osmosdr_source_1 = osmosdr.source( args="numchan=" + str(1) + " " + "bladerf=179" )
        self.osmosdr_source_1.set_sample_rate(samp_rate)
        self.osmosdr_source_1.set_center_freq(freq, 0)
        self.osmosdr_source_1.set_freq_corr(0, 0)
        self.osmosdr_source_1.set_dc_offset_mode(0, 0)
        self.osmosdr_source_1.set_iq_balance_mode(0, 0)
        self.osmosdr_source_1.set_gain_mode(True, 0)
        self.osmosdr_source_1.set_gain(10, 0)
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
        self.connect((self.osmosdr_source_1, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_complex_to_imag_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_complex_to_imag_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)
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


def blader_Rx(sr,bw,top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(sr,bw)
    tb.start()
    tb.show()
    start=time.time()

    def finish():
        end = time.time()
        print("\n")
        print "%"*40
        print("transmission time: \t"+str(end-start)+"s")
        print("\tsamp rate: \t"+str(tb.samp_rate)+" samples/s")
        print("\tcarr freq: \t"+str(tb.freq)+"Hz")
        print("\tbandwidth: \t"+str(tb.bandwidth)+"Hz")

        tb.stop()
        
        QtCore.QCoreApplication.instance().quit()

    t = Timer(2, finish)
    t.start() # after 30 seconds, "hello, world" will be printed     

    qapp.exec_()


if __name__ == '__main__':
    blader_Rx()
