#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Gsm
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gsm
import pmt
from gnuradio import network
import osmosdr
import time
import sip



class GSM(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Gsm", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Gsm")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "GSM")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.shiftoff = shiftoff = 400000
        self.samp_rate = samp_rate = 2000000
        self.pi = pi = 3.141592654
        self.osr = osr = 4
        self.PPM_GUI = PPM_GUI = 0
        self.Gain_GUI = Gain_GUI = 50
        self.Freq_GUI = Freq_GUI = 925e6

        ##################################################
        # Blocks
        ##################################################

        self.tab_index = Qt.QTabWidget()
        self.tab_index_widget_0 = Qt.QWidget()
        self.tab_index_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_index_widget_0)
        self.tab_index_grid_layout_0 = Qt.QGridLayout()
        self.tab_index_layout_0.addLayout(self.tab_index_grid_layout_0)
        self.tab_index.addTab(self.tab_index_widget_0, 'FFT')
        self.tab_index_widget_1 = Qt.QWidget()
        self.tab_index_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_index_widget_1)
        self.tab_index_grid_layout_1 = Qt.QGridLayout()
        self.tab_index_layout_1.addLayout(self.tab_index_grid_layout_1)
        self.tab_index.addTab(self.tab_index_widget_1, 'Waterfall')
        self.top_layout.addWidget(self.tab_index)
        self._PPM_GUI_range = qtgui.Range(-150, 150, 1, 0, 200)
        self._PPM_GUI_win = qtgui.RangeWidget(self._PPM_GUI_range, self.set_PPM_GUI, "PPM", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tab_index_grid_layout_0.addWidget(self._PPM_GUI_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.tab_index_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.tab_index_grid_layout_0.setColumnStretch(c, 1)
        self._Gain_GUI_range = qtgui.Range(0, 50, 0.5, 50, 200)
        self._Gain_GUI_win = qtgui.RangeWidget(self._Gain_GUI_range, self.set_Gain_GUI, "Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tab_index_grid_layout_0.addWidget(self._Gain_GUI_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.tab_index_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tab_index_grid_layout_0.setColumnStretch(c, 1)
        self._Freq_GUI_range = qtgui.Range(925e6, 1.99e9, 200e3, 925e6, 200)
        self._Freq_GUI_win = qtgui.RangeWidget(self._Freq_GUI_range, self.set_Freq_GUI, "Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tab_index_grid_layout_0.addWidget(self._Freq_GUI_win, 1, 1, 1, 2)
        for r in range(1, 2):
            self.tab_index_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 3):
            self.tab_index_grid_layout_0.setColumnStretch(c, 1)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq((Freq_GUI-shiftoff), 0)
        self.rtlsdr_source_0.set_freq_corr(PPM_GUI, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(Gain_GUI, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth((250e3+abs(shiftoff)), 0)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.tab_index_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win, 2, 1, 2, 2)
        for r in range(2, 4):
            self.tab_index_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 3):
            self.tab_index_grid_layout_0.setColumnStretch(c, 1)
        self.network_socket_pdu_0 = network.socket_pdu('UDP_CLIENT', '127.0.0.1', '4729', 10000, False)
        self.gsm_sdcch8_demapper_0 = gsm.gsm_sdcch8_demapper(
            timeslot_nr=1,
        )
        self.gsm_receiver_0 = gsm.receiver(4, [0], [], False)
        self.gsm_message_printer_0 = gsm.message_printer(pmt.intern(''), False,
            False, False)
        self.gsm_input_0 = gsm.gsm_input(
            ppm=PPM_GUI,
            osr=osr,
            fc=Freq_GUI,
            samp_rate_in=samp_rate,
        )
        self.gsm_decryption_0 = gsm.decryption([], 1)
        self.gsm_control_channels_decoder_0_0 = gsm.control_channels_decoder()
        self.gsm_control_channels_decoder_0 = gsm.control_channels_decoder()
        self.gsm_clock_offset_control_0 = gsm.clock_offset_control(Freq_GUI-shiftoff, samp_rate, osr)
        self.gsm_bcch_ccch_demapper_0 = gsm.gsm_bcch_ccch_demapper(
            timeslot_nr=0,
        )
        self.blocks_rotator_cc_0 = blocks.rotator_cc((-2*pi*shiftoff/samp_rate), False)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gsm_bcch_ccch_demapper_0, 'bursts'), (self.gsm_control_channels_decoder_0, 'bursts'))
        self.msg_connect((self.gsm_clock_offset_control_0, 'ctrl'), (self.gsm_input_0, 'ctrl_in'))
        self.msg_connect((self.gsm_control_channels_decoder_0, 'msgs'), (self.gsm_message_printer_0, 'msgs'))
        self.msg_connect((self.gsm_control_channels_decoder_0, 'msgs'), (self.network_socket_pdu_0, 'pdus'))
        self.msg_connect((self.gsm_control_channels_decoder_0_0, 'msgs'), (self.network_socket_pdu_0, 'pdus'))
        self.msg_connect((self.gsm_decryption_0, 'bursts'), (self.gsm_control_channels_decoder_0_0, 'bursts'))
        self.msg_connect((self.gsm_receiver_0, 'C0'), (self.gsm_bcch_ccch_demapper_0, 'bursts'))
        self.msg_connect((self.gsm_receiver_0, 'measurements'), (self.gsm_clock_offset_control_0, 'measurements'))
        self.msg_connect((self.gsm_receiver_0, 'C0'), (self.gsm_sdcch8_demapper_0, 'bursts'))
        self.msg_connect((self.gsm_sdcch8_demapper_0, 'bursts'), (self.gsm_decryption_0, 'bursts'))
        self.connect((self.blocks_rotator_cc_0, 0), (self.gsm_input_0, 0))
        self.connect((self.blocks_rotator_cc_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.gsm_input_0, 0), (self.gsm_receiver_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_rotator_cc_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "GSM")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_shiftoff(self):
        return self.shiftoff

    def set_shiftoff(self, shiftoff):
        self.shiftoff = shiftoff
        self.blocks_rotator_cc_0.set_phase_inc((-2*self.pi*self.shiftoff/self.samp_rate))
        self.gsm_clock_offset_control_0.set_fc(self.Freq_GUI-self.shiftoff)
        self.rtlsdr_source_0.set_center_freq((self.Freq_GUI-self.shiftoff), 0)
        self.rtlsdr_source_0.set_bandwidth((250e3+abs(self.shiftoff)), 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_rotator_cc_0.set_phase_inc((-2*self.pi*self.shiftoff/self.samp_rate))
        self.gsm_input_0.set_samp_rate_in(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_pi(self):
        return self.pi

    def set_pi(self, pi):
        self.pi = pi
        self.blocks_rotator_cc_0.set_phase_inc((-2*self.pi*self.shiftoff/self.samp_rate))

    def get_osr(self):
        return self.osr

    def set_osr(self, osr):
        self.osr = osr
        self.gsm_input_0.set_osr(self.osr)

    def get_PPM_GUI(self):
        return self.PPM_GUI

    def set_PPM_GUI(self, PPM_GUI):
        self.PPM_GUI = PPM_GUI
        self.gsm_input_0.set_ppm(self.PPM_GUI)
        self.rtlsdr_source_0.set_freq_corr(self.PPM_GUI, 0)

    def get_Gain_GUI(self):
        return self.Gain_GUI

    def set_Gain_GUI(self, Gain_GUI):
        self.Gain_GUI = Gain_GUI
        self.rtlsdr_source_0.set_gain(self.Gain_GUI, 0)

    def get_Freq_GUI(self):
        return self.Freq_GUI

    def set_Freq_GUI(self, Freq_GUI):
        self.Freq_GUI = Freq_GUI
        self.gsm_clock_offset_control_0.set_fc(self.Freq_GUI-self.shiftoff)
        self.gsm_input_0.set_fc(self.Freq_GUI)
        self.rtlsdr_source_0.set_center_freq((self.Freq_GUI-self.shiftoff), 0)




def main(top_block_cls=GSM, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()