/***************************************************************************//**
 *   @file   adaq8092.c
 *   @brief  Implementation of ADAQ8092 Driver.
 *   @author Antoniu Miclaus (antoniu.miclaus@analog.com)
********************************************************************************
 * Copyright 2022(c) Analog Devices, Inc.
 *
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *  - Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *  - Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *  - Neither the name of Analog Devices, Inc. nor the names of its
 *    contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *  - The use of this software may or may not infringe the patent rights
 *    of one or more patent holders.  This license does not release you
 *    from the requirement that you obtain separate licenses from these
 *    patent holders to use this software.
 *  - Use of the software either in source or binary form, must be run
 *    on or directly connected to an Analog Devices Inc. component.
 *
 * THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT,
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, INTELLECTUAL PROPERTY RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*******************************************************************************/

/******************************************************************************/
/***************************** Include Files **********************************/
/******************************************************************************/
#include <stdlib.h>
#include <errno.h>
#include "adaq8092.h"
#include "delay.h"

/******************************************************************************/
/************************ Functions Definitions *******************************/
/******************************************************************************/
/******************************************************************************/

int adaq8092_init(struct adaq8092_dev **device, struct adaq8092_init_param init_param)
{
	struct adaq8092_dev *dev;
	int ret;

	dev = (struct adxl355_dev *)calloc(1, sizeof(*dev));
	if (!dev)
		return -ENOMEM;

	/* SPI Initialization*/
	ret = spi_init(&dev->spi_desc, init_param.spi_init));
	if (ret)
		goto error_dev;

	/* GPIO Initialization */
	ret = gpio_get(&dev->gpio_adc_pd1, init_param.gpio_adc_pd1);
	if (ret)
		goto error_spi;
	
	ret = gpio_get(&dev->gpio_adc_pd2, init_param.gpio_adc_pd2);
	if (ret)
		goto error_adc_pd1;
	
	ret = gpio_get(&dev->gpio_en_1p8, init_param.gpio_en_1p8);
	if (ret)
		goto error_adc_pd2;

	ret = gpio_get(&dev->gpio_par_ser, init_param.gpio_par_ser);
	if (ret)
		goto error_en_1p8;

	/* Powerup Sequence */
	ret = gpio_direction_output(dev->gpio_adc_pd1, GPIO_LOW);
	if (ret)
		goto error_par_ser;

	ret = gpio_direction_output(dev->gpio_adc_pd2, GPIO_LOW);
	if (ret)
		goto error_par_ser;

	ret = gpio_direction_output(dev->gpio_en_1p8, GPIO_LOW);
	if (ret)
		goto error_par_ser;

	ret = gpio_direction_output(dev->gpio_par_ser, GPIO_LOW);
	if (ret)
		goto error_par_ser;

	mdelay(1000);

	ret = gpio_set_value(dev->gpio_en_1p8, GPIO_HIGH);
	if (ret)
		goto error_par_ser;

	mdelay(1000);

	ret = gpio_set_value(dev->gpio_adc_pd1, GPIO_HIGH);
	if (ret)
		goto error_par_ser;

	ret = gpio_set_value(dev->gpio_adc_pd2, GPIO_HIGH);
	if (ret)
		goto error_par_ser;

	/* Software Reset */
	ret = adaq8092_write(dev,  ADAQ8092_REG_RESET, field_prep(ADAQ8092_RESET, 1));
	if (ret)
		goto error_par_ser;

	mdelay(100);

	/* Device Initialization */
	ret = adaq8092_set_pd_mode(dev, init_param.pd_mode);
	if (ret)
		goto error_par_ser;

	ret = adaq8092_set_clk_pol_mode(dev, init_param.clk_pol_mode);
	if (ret)
		goto error_par_ser;

	ret = adaq8092_set_clk_phase_mode(dev, init_param.clk_phase_mode);
	if (ret)
		goto error_par_ser;

	ret = adaq8092_set_clk_dc_mode(dev, init_param.clk_dc_mode);
	if (ret)
		goto error_par_ser;

	ret = adaq8092_set_lvds_cur_mode(dev, init_param.lvds_cur_mode);
	if (ret)
		goto error_par_ser;

	ret = adaq8092_set_lvds_term_mode(dev, init_param.lvds_term_mode);
	if (ret)
		goto error_par_ser;

	ret = adaq8092_set_dout_en(dev, init_param.dout_en);
	if (ret)
		goto error_par_ser;

	ret = adaq8092_set_dout_mode(dev, init_param.dout_mode);
	if (ret)
		goto error_par_ser;

	ret = adaq8092_set_test_mode(dev, init_param.test_mode);
	if (ret)
		goto error_par_ser;

	ret = adaq8092_set_alt_pol_en(dev, init_param.alt_bit_pol_en);
	if (ret)
		goto error_par_ser;

	ret = adaq8092_set_data_rand_en(dev, init_param.data_rand_en);
	if (ret)
		goto error_par_ser;

	ret = adaq8092_set_twos_comp(dev, init_param.twos_comp);
	if (ret)
		goto error_par_ser;

	*device = dev;

	return 0;

error_par_ser:
	gpio_remove(dev->gpio_par_ser);
error_adc_en_1p8:
	gpio_remove(dev->gpio_en_1p8);
error_adc_pd2:
	gpio_remove(dev->gpio_adc_pd2);
error_adc_pd1:
	gpio_remove(dev->gpio_adc_pd1);
error_spi:
	spi_remove(dev->spi_desc);
error_dev:
	free(dev);

	return ret;
}

int adaq8092_remove(struct adaq8092_dev *dev)
{
	int ret;

	ret = spi_remove(dev->spi_desc);
	if (ret)
		return ret;

	ret = gpio_remove(dev->gpio_adc_pd1);
	if (ret)
		return ret;

	ret = gpio_remove(dev->gpio_adc_pd2);
	if (ret)
		return ret;

	ret = gpio_remove(dev->gpio_en_1p8);
	if (ret)
		return ret;

	ret = gpio_remove(dev->gpio_par_ser);
	if (ret)
		return ret;

	free(dev);

	return ret;
}

int adaq8092_set_pd_mode(struct adaq8092_dev *dev, enum adaq8092_powerdown_modes mode)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);
	int ret;

	ret = adaq8092_update_bits(dev->spi_desc, ADAQ8092_REG_POWERDOWN,
				 ADAQ8092_POWERDOWN_MODE,
				 field_prep(ADAQ8092_POWERDOWN_MODE, mode));
	if (ret)
		return ret;

	dev->pd_mode = mode;

	return 0;
}

int adaq8092_get_pd_mode(struct adaq8092_dev *dev)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);

	return dev->pd_mode;
}

int adaq8092_set_clk_pol_mode(struct adaq8092_dev *dev, enum adaq8092_clk_invert mode)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);
	int ret;

	ret = adaq8092_update_bits(dev->spi_desc, ADAQ8092_REG_TIMING,
				 ADAQ8092_CLK_INVERT,
				 field_prep(ADAQ8092_CLK_INVERT, mode));
	if (ret)
		return ret;

	dev->clk_pol_mode = mode;

	return 0;
}

int adaq8092_get_clk_pol_mode(struct adaq8092_dev *dev)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);

	return dev->clk_pol_mode;
}

int adaq8092_set_clk_phase_mode(struct adaq8092_dev *dev, enum adaq8092_clk_phase_delay mode)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);
	int ret;

	ret = adaq8092_update_bits(dev->spi_desc, ADAQ8092_REG_TIMING,
				 ADAQ8092_CLK_PHASE,
				 field_prep(ADAQ8092_CLK_PHASE, mode));
	if (ret)
		return ret;

	dev->clk_phase_mode = mode;

	return 0;
}

int adaq8092_get_clk_phase_mode(struct adaq8092_dev *dev)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);

	return dev->clk_phase_mode;
}

int adaq8092_set_clk_dc_mode(struct adaq8092_dev *dev, enum adaq8092_clk_dutycycle mode)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);
	int ret;

	ret = adaq8092_update_bits(dev->spi_desc, ADAQ8092_REG_TIMING,
				 ADAQ8092_CLK_DUTYCYCLE,
				 field_prep(ADAQ8092_CLK_DUTYCYCLE, mode));
	if (ret)
		return ret;

	dev->clk_dc_mode = mode;

	return 0;
}

int adaq8092_get_clk_dc_mode(struct adaq8092_dev *dev)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);

	return dev->clk_dc_mode;
}

int adaq8092_set_lvds_cur_mode(struct adaq8092_dev *dev, enum adaq8092_lvds_out_current mode)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);
	int ret;

	ret = adaq8092_update_bits(dev->spi_desc, ADAQ8092_REG_OUTPUT_MODE,
				 ADAQ8092_ILVDS,
				 field_prep(ADAQ8092_ILVDS, mode));
	if (ret)
		return ret;

	dev->lvds_cur_mode = mode;

	return 0;
}

int adaq8092_get_lvds_cur_mode(struct adaq8092_dev *dev)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);

	return dev->lvds_cur_mode;
}

int adaq8092_set_lvds_term_mode(struct adaq8092_dev *dev, enum adaq8092_internal_term mode)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);
	int ret;

	ret = adaq8092_update_bits(dev->spi_desc, ADAQ8092_REG_OUTPUT_MODE,
				 ADAQ8092_TERMON,
				 field_prep(ADAQ8092_TERMON, mode));
	if (ret)
		return ret;

	dev->lvds_term_mode = mode;

	return 0;
}

int adaq8092_get_lvds_term_mode(struct adaq8092_dev *dev)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);

	return dev->lvds_term_mode;
}

int adaq8092_set_dout_en(struct adaq8092_dev *dev, enum adaq8092_dout_enable mode)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);
	int ret;

	ret = adaq8092_update_bits(dev->spi_desc, ADAQ8092_REG_OUTPUT_MODE,
				 ADAQ8092_OUTOFF,
				 field_prep(ADAQ8092_OUTOFF, mode));
	if (ret)
		return ret;

	dev->dout_en = mode;

	return 0;
}

int adaq8092_get_dout_en(struct adaq8092_dev *dev)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);

	return dev->dout_en;
}

int adaq8092_set_dout_mode(struct adaq8092_dev *dev, enum adaq8092_dout_modes mode)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);
	int ret;

	ret = adaq8092_update_bits(dev->spi_desc, ADAQ8092_REG_OUTPUT_MODE,
				 ADAQ8092_OUTMODE,
				 field_prep(ADAQ8092_OUTMODE, mode));
	if (ret)
		return ret;

	dev->dout_mode = mode;

	return 0;
}

int adaq8092_get_dout_mode(struct adaq8092_dev *dev)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);

	return dev->dout_mode;
}

int adaq8092_set_test_mode(struct adaq8092_dev *dev, enum adaq8092_out_test_modes mode)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);
	int ret;

	ret = adaq8092_update_bits(dev->spi_desc, ADAQ8092_REG_DATA_FORMAT,
				 ADAQ8092_OUTTEST,
				 field_prep(ADAQ8092_OUTTEST, mode));
	if (ret)
		return ret;

	dev->test_mode = mode;

	return 0;
}

int adaq8092_get_test_mode(struct adaq8092_dev *dev)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);

	return dev->test_mode;
}

int adaq8092_set_alt_pol_en(struct adaq8092_dev *dev, enum adaq8092_alt_bit_pol mode)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);
	int ret;

	ret = adaq8092_update_bits(dev->spi_desc, ADAQ8092_REG_DATA_FORMAT,
				 ADAQ8092_ABP,
				 field_prep(ADAQ8092_ABP, mode));
	if (ret)
		return ret;

	dev->alt_bit_pol_en = mode;

	return 0;
}

int adaq8092_get_alt_pol_en(struct adaq8092_dev *dev)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);

	return dev->alt_bit_pol_en;
}

int adaq8092_set_data_rand_en(struct adaq8092_dev *dev, enum adaq8092_data_rand	mode)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);
	int ret;

	ret = adaq8092_update_bits(dev->spi_desc, ADAQ8092_REG_DATA_FORMAT,
				 ADAQ8092_RAND,
				 field_prep(ADAQ8092_RAND, mode));
	if (ret)
		return ret;

	dev->data_rand_en = mode;

	return 0;
}

int adaq8092_get_data_rand_en(struct adaq8092_dev *dev)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);

	return dev->data_rand_en;
}

int adaq8092_set_twos_comp(struct adaq8092_dev *dev, enum adaq8092_twoscomp mode)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);
	int ret;

	ret = adaq8092_update_bits(dev->spi_desc, ADAQ8092_REG_DATA_FORMAT,
				 ADAQ8092_TWOSCOMP,
				 field_prep(ADAQ8092_TWOSCOMP, mode));
	if (ret)
		return ret;

	dev->twos_comp = mode;

	return 0;
}

int adaq8092_get_twos_comp(struct adaq8092_dev *dev)
{
	struct adaq8092_state *st = adaq8092_get_data(indio_dev);

	return dev->twos_comp;
}