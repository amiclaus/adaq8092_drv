import pytest

hardware = ["adaq8092"]
classname = "adi.adaq8092"

#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0, 1])
def test_adaq8092_rx_data(test_dma_rx, iio_uri, classname, channel):
    test_dma_rx(iio_uri, classname, channel)


#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize(
    "attr, val",
    [
        ("sampling_frequency", [105000000,],),
        (
            "alt_bit_pol_en",
            ["alternate_bit_polarity_off", "alternate_bit_polarity_on"],
        ),
        ("clk_pol_mode", ["clk_pol_normal", "clk_pol_inverted"],),
        ("data_rand_en", ["data_randomizer_off", "data_randomizer_on"],),
        ("dout_en", ["digital_output_on", "digital_output_off"],),
        (
            "lvds_cur_mode",
            [
                "lvds_current_3m5A",
                "lvds_current_4mA",
                "lvds_current_4m5A",
                "lvds_current_3mA",
                "lvds_current_2m5A",
                "lvds_current_3m1A",
                "lvds_current_1m75A",
            ],
        ),
        (
            "lvds_term_mode",
            ["lvds_internal_termination_off", "lvds_internal_termination_on"],
        ),
        (
            "pd_gpio",
            ["pd1_on_pd2_on", "pd1_off_pd2_on", "pd1_on_pd2_off", "pd1_off_pd2_off"],
        ),
        ("pd_mode", ["normal", "ch2_nap", "ch1_ch2_nap", "sleep"],),
        (
            "test_mode",
            [
                "test_pattern_off",
                "test_all_digital_zero",
                "test_all_digital_one",
                "test_checkerboard",
                "test_alternating",
            ],
        ),
        ("twos_complement", ["offset_binary", "twos_complement"],),
    ],
)
def test_ad4630_attr(test_attribute_multipe_values, iio_uri, classname, attr, val):
    test_attribute_multipe_values(iio_uri, classname, attr, val, 0)
