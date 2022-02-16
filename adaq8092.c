// SPDX-License-Identifier: GPL-2.0-only
/*
 * ADAQ8092 driver
 *
 * Copyright 2022 Analog Devices Inc.
 */

#include <linux/bitfield.h>
#include <linux/bits.h>
#include <linux/device.h>
#include <linux/iio/iio.h>
#include <linux/module.h>
#include <linux/regmap.h>
#include <linux/regulator/consumer.h>
#include <linux/spi/spi.h>

/* ADAQ8092 Register Map */
#define ADAQ8092_REG_RESET		0x00
#define ADAQ8092_REG_POWERDOWN		0x01
#define ADAQ8092_REG_TIMING		0x02
#define ADAQ8092_REG_OUTPUT_MODE	0x03
#define ADAQ8092_REG_DATA_FORMAT	0x04

/* ADAQ8092_REG_RESET Bit Definition */
#define ADAQ8092_REG_RESET		BIT(7)

/* ADAQ8092_REG_POWERDOWN Bit Definition */
#define ADAQ8092_POWERDOWN_MODE		GENMASK(1, 0)

/* ADAQ8092_REG_TIMING Bit Definition */
#define ADAQ8092_CLK_INVERT		BIT(3)
#define ADAQ8092_CLK_PHASE		GENMASK(2, 1)
#define ADAQ8092_CLK_DUTYCYCLE		BIT(0)

/* ADAQ8092_REG_OUTPUT_MODE Bit Definition */
#define ADAQ8092_ILVDS			GENMASK(6, 4)
#define ADAQ8092_TERMON			BIT(3)
#define ADAQ8092_OUTOFF			BIT(2)
#define ADAQ8092_OUTMODE		GENMASK(1, 0)

/* ADAQ8092_REG_DATA_FORMAT Bit Definition */
#define ADAQ8092_OUTTEST		GENMASK(5, 3)
#define ADAQ8092_ABP			BIT(2)
#define ADAQ8092_RAND			BIT(1)
#define ADAQ8092_TWOSCOMP		BIT(0)
