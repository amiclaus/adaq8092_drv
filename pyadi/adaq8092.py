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

import numpy as np
from adi.context_manager import context_manager
from adi.rx_tx import rx

# def _cast32(sample):
#             sample = sample & 0xFFFFFF
#             return (sample if not (sample & 0x800000) else sample - 0x1000000)


class adaq8092(rx, context_manager):

    """ADAQ8092 14-Bit, 105MSPS, Dual-Channel uModule Data Acquisition Solution"""

    _device_name = "adaq8092"

    def __init__(
        self, uri="",
    ):
        """Initialize."""
        context_manager.__init__(self, uri, self._device_name)

        self._ctrl = self._ctx.find_device("adaq8092")
        self._rxadc = self._ctx.find_device("adaq8092")
        self._device_name = "adaq8092"
        if not self._rxadc:
            self._ctrl = self._ctx.find_device("cf_axi_adc")
            self._rxadc = self._ctx.find_device("cf_axi_adc")
            self._device_name = "cf_axi_adc"

        rx._rx_stack_interleaved = True  # DMA config. dependent. True for ad7768.
        rx._rx_data_type = np.int16
        for ch in self._rxadc.channels:
            name = ch._id
            self._rx_channel_names.append(name)
        rx.__init__(self)

    @property
    def alt_bit_pol_en_available(self):
        """Get available Alternate Bit Polarity Mode Control."""
        return self._get_iio_dev_attr_str("alt_bit_pol_en_available")

    @property
    def alt_bit_pol_en(self):
        """Get Alternate Bit Polarity Mode Control."""
        return self._get_iio_dev_attr_str("alt_bit_pol_en")

    @alt_bit_pol_en.setter
    def alt_bit_pol_en(self, rate):
        """Set Alternate Bit Polarity Mode Control."""
        if rate in self.alt_bit_pol_en_available:
            self._set_iio_dev_attr_str("alt_bit_pol_en", rate)
        else:
            raise ValueError(
                "Error: Alternate Bit Polarity Mode Control not supported \nUse one of: "
                + str(self.alt_bit_pol_en_available)
            )

    @property
    def clk_dc_mode_available(self):
        """Get available Clock Duty Cycle Stabilizer."""
        return self._get_iio_dev_attr_str("clk_dc_mode_available")

    @property
    def clk_dc_mode(self):
        """Get Clock Duty Cycle Stabilizer."""
        return self._get_iio_dev_attr_str("clk_dc_mode")

    @clk_dc_mode.setter
    def clk_dc_mode(self, rate):
        """Set Clock Duty Cycle Stabilizer."""
        if rate in self.clk_dc_mode_available:
            self._set_iio_dev_attr_str("clk_dc_mode", rate)
        else:
            raise ValueError(
                "Error: Clock Duty Cycle Stabilizer not supported \nUse one of: "
                + str(self.clk_dc_mode_available)
            )

    @property
    def clk_phase_mode_available(self):
        """Get available Output Clock Phase Delay."""
        return self._get_iio_dev_attr_str("clk_phase_mode_available")

    @property
    def clk_phase_mode(self):
        """Get Output Clock Phase Delay."""
        return self._get_iio_dev_attr_str("clk_phase_mode")

    @clk_phase_mode.setter
    def clk_phase_mode(self, rate):
        """Set Output Clock Phase Delay."""
        if rate in self.clk_phase_mode_available:
            self._set_iio_dev_attr_str("clk_phase_mode", rate)
        else:
            raise ValueError(
                "Error: Output Clock Phase Delay not supported \nUse one of: "
                + str(self.clk_phase_mode_available)
            )

    @property
    def clk_pol_mode_available(self):
        """Get available CLKOUT Polarity."""
        return self._get_iio_dev_attr_str("clk_pol_mode_available")

    @property
    def clk_pol_mode(self):
        """Get CLKOUT Polarity."""
        return self._get_iio_dev_attr_str("clk_pol_mode")

    @clk_pol_mode.setter
    def clk_pol_mode(self, rate):
        """Set CLKOUT Polarity."""
        if rate in self.clk_pol_mode_available:
            self._set_iio_dev_attr_str("clk_pol_mode", rate)
        else:
            raise ValueError(
                "Error: CLKOUT Polarity not supported \nUse one of: "
                + str(self.clk_pol_mode_available)
            )

    @property
    def data_rand_en_available(self):
        """Get available Data Randomizer."""
        return self._get_iio_dev_attr_str("data_rand_en_available")

    @property
    def data_rand_en(self):
        """Get Data Randomizer."""
        return self._get_iio_dev_attr_str("data_rand_en")

    @data_rand_en.setter
    def data_rand_en(self, rate):
        """Set Data Randomizer."""
        if rate in self.data_rand_en_available:
            self._set_iio_dev_attr_str("data_rand_en", rate)
        else:
            raise ValueError(
                "Error: Data Randomizer not supported \nUse one of: "
                + str(self.data_rand_en_available)
            )

    @property
    def dout_en_available(self):
        """Get available Digital Outputs."""
        return self._get_iio_dev_attr_str("dout_en_available")

    @property
    def dout_en(self):
        """Get Digital Outputs."""
        return self._get_iio_dev_attr_str("dout_en")

    @dout_en.setter
    def dout_en(self, rate):
        """Set Digital Outputs."""
        if rate in self.dout_en_available:
            self._set_iio_dev_attr_str("dout_en", rate)
        else:
            raise ValueError(
                "Error: Digital Outputs not supported \nUse one of: "
                + str(self.dout_en_available)
            )

    @property
    def dout_mode_available(self):
        """Get available Digital Output Mode."""
        return self._get_iio_dev_attr_str("dout_mode_available")

    @property
    def dout_mode(self):
        """Get Digital Output Mode."""
        return self._get_iio_dev_attr_str("dout_mode")

    @dout_mode.setter
    def dout_mode(self, rate):
        """Set Digital Output Mode."""
        if rate in self.dout_mode_available:
            self._set_iio_dev_attr_str("dout_mode", rate)
        else:
            raise ValueError(
                "Error: Digital Output Mode not supported \nUse one of: "
                + str(self.dout_mode_available)
            )

    @property
    def lvds_cur_mode_available(self):
        """Get available LVDS Output Current."""
        return self._get_iio_dev_attr_str("lvds_cur_mode_available")

    @property
    def lvds_cur_mode(self):
        """Get LVDS Output Current."""
        return self._get_iio_dev_attr_str("lvds_cur_mode")

    @lvds_cur_mode.setter
    def lvds_cur_mode(self, rate):
        """Set LVDS Output Current."""
        if rate in self.lvds_cur_mode_available:
            self._set_iio_dev_attr_str("lvds_cur_mode", rate)
        else:
            raise ValueError(
                "Error: LVDS Output Current not supported \nUse one of: "
                + str(self.lvds_cur_mode_available)
            )

    @property
    def lvds_term_mode_available(self):
        """Get available LVDS Internal Termination."""
        return self._get_iio_dev_attr_str("lvds_term_mode_available")

    @property
    def lvds_term_mode(self):
        """Get LVDS Internal Termination."""
        return self._get_iio_dev_attr_str("lvds_term_mode")

    @lvds_term_mode.setter
    def lvds_term_mode(self, rate):
        """Set LVDS Internal Termination."""
        if rate in self.lvds_term_mode_available:
            self._set_iio_dev_attr_str("lvds_term_mode", rate)
        else:
            raise ValueError(
                "Error: LVDS Internal Termination not supported \nUse one of: "
                + str(self.lvds_term_mode_available)
            )

    @property
    def par_ser_gpio(self):
        """Get Paraller/Serial Gpio Value."""
        return self._get_iio_dev_attr_str("par_ser_gpio")

    @property
    def pd_gpio_available(self):
        """Get available Power Down GPIO Configuration."""
        return self._get_iio_dev_attr_str("pd_gpio_available")

    @property
    def pd_gpio(self):
        """Get Power Down GPIO Configuration."""
        return self._get_iio_dev_attr_str("pd_gpio")

    @pd_gpio.setter
    def pd_gpio(self, rate):
        """Set Power Down GPIO Configuration."""
        if rate in self.pd_gpio_available:
            self._set_iio_dev_attr_str("pd_gpio", rate)
        else:
            raise ValueError(
                "Error: Power Down GPIO Configuration not supported \nUse one of: "
                + str(self.pd_gpio_available)
            )

    @property
    def pd_mode_available(self):
        """Get available Power Down Modes."""
        return self._get_iio_dev_attr_str("pd_mode_available")

    @property
    def pd_mode(self):
        """Get Power Down Mode."""
        return self._get_iio_dev_attr_str("pd_mode")

    @pd_mode.setter
    def pd_mode(self, rate):
        """Set Power Down Mode."""
        if rate in self.pd_mode_available:
            self._set_iio_dev_attr_str("pd_mode", rate)
        else:
            raise ValueError(
                "Error: Digital Output Test Pattern not supported \nUse one of: "
                + str(self.pd_mode_available)
            )

    @property
    def sampling_frequency(self):
        """Get Sampling Frequency."""
        return self._get_iio_dev_attr("sampling_frequency")

    @sampling_frequency.setter
    def sampling_frequency(self, rate):
        """Set Sampling Frequency."""
        self._set_iio_dev_attr("sampling_frequency", rate)

    @property
    def test_mode_available(self):
        """Get available Digital Output Test Pattern."""
        return self._get_iio_dev_attr_str("test_mode_available")

    @property
    def test_mode(self):
        """Get Digital Output Test Pattern."""
        return self._get_iio_dev_attr_str("test_mode")

    @test_mode.setter
    def test_mode(self, rate):
        """Set Digital Output Test Pattern."""
        if rate in self.test_mode_available:
            self._set_iio_dev_attr_str("test_mode", rate)
        else:
            raise ValueError(
                "Error: Digital Output Test Pattern not supported \nUse one of: "
                + str(self.test_mode_available)
            )

    @property
    def twos_complement_available(self):
        """Get available Two's Complement Modes."""
        return self._get_iio_dev_attr_str("twos_complement_available")

    @property
    def twos_complement(self):
        """Get Two's Complement Modes."""
        return self._get_iio_dev_attr_str("twos_complement")

    @twos_complement.setter
    def twos_complement(self, rate):
        """Set Two's Complement Modes."""
        if rate in self.twos_complement_available:
            self._set_iio_dev_attr_str("twos_complement", rate)
        else:
            raise ValueError(
                "Error: Two's Complement Modes not supported \nUse one of: "
                + str(self.twos_complement_available)
            )
