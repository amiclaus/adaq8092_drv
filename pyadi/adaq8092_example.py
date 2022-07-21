# Copyright (C) 2022 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys

import matplotlib.pyplot as plt

import numpy as np
from adi import adaq8092

# Optionally passs URI as command line argument,
# else use default ip:analog.local
my_uri = sys.argv[1] if len(sys.argv) >= 2 else "ip:analog.local"
print("uri: " + str(my_uri))

my_adc = adaq8092(uri=my_uri)
my_adc.rx_buffer_size = 256
my_adc.rx_output_type = "raw"

print("Sampling frequency:", my_adc.sampling_frequency)
print("Enabled Channels: ", my_adc.rx_enabled_channels)
print("Alternate Bit Polarity Mode Control: ", my_adc.alt_bit_pol_en)
print("Clock Duty Cycle Stabilizer: ", my_adc.clk_dc_mode)
print("Output Clock Phase Delay: ", my_adc.clk_phase_mode)
print("CLKOUT Polarity: ", my_adc.clk_pol_mode)
print("Data Randomizer: ", my_adc.data_rand_en)
print("Digital Outputs: ", my_adc.dout_en)
print("Digital Output Mode: ", my_adc.dout_mode)
print("LVDS Output Current: ", my_adc.lvds_cur_mode)
print("LVDS Internal Termination: ", my_adc.lvds_term_mode)
print("Paraller/Serial Gpio Value: ", my_adc.par_ser_gpio)
print("Power Down GPIO Configuration: ", my_adc.pd_gpio)
print("Power Down Mode: ", my_adc.pd_mode)
print("Digital Output Test Pattern: ", my_adc.test_mode)
print("Two's Complement Modes: ", my_adc.twos_complement)

plt.clf()
data = my_adc.rx()
for ch in my_adc.rx_enabled_channels:
    plt.plot(range(0, len(data[0])), data[ch], label="channel" + str(ch))
plt.xlabel("Data Point")
plt.ylabel("ADC counts")
plt.legend(
    bbox_to_anchor=(0.0, 1.02, 1.0, 0.102),
    loc="lower left",
    ncol=4,
    mode="expand",
    borderaxespad=0.0,
)
plt.show()

del my_adc
