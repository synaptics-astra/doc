# Astra MCU SDK Integration Guide

## Overview

This document provides guidance on setting up, building, and integrating
the Astra MCU SDK for SL2610.

For complete details, refer to: [Astra MCU SDK Developer Guide](https://synaptics-astra-mcu.github.io/doc/v/latest/developer_guide/index.html)
and the [SL2610 Build and Flash with CLI](https://synaptics-astra-mcu.github.io/doc/v/latest/srsdk/docs/SL2610/SL2610_Build_and_Flash_with_CLI.html)
Guide.

The MCU SDK supports both: - VS Code-based build flow - Native
(command-line) build flow.

For users following the native build method, the [Astra MCU SDK Developer Guide](https://synaptics-astra-mcu.github.io/doc/v/latest/developer_guide/index.html)
and the [SL2610 Build and Flash with CLI](https://synaptics-astra-mcu.github.io/doc/v/latest/srsdk/docs/SL2610/SL2610_Build_and_Flash_with_CLI.html)
Guide are the primary starting points.

------------------------------------------------------------------------

## Defconfig Selection

### DDR Profile Matrix (M52 BL / M52 SM)

| DDR profile | M52 BL | M52 SM |
| --- | --- | --- |
| DDR4 2x8 (default profile) | configs/SL2610_RDK/sl2610_bootloader_rdk_defconfig | examples/system_manager/configs/sl2610_rdk_system_manager_defconfig |
| DDR4 1x16 | configs/SL2610_RDK/sl2610_bootloader_ddr4_1x16_rdk_defconfig | examples/system_manager/configs/sl2610_rdk_system_manager_ddr4_1x16_defconfig |
| LPDDR4 | configs/SL2610_RDK/sl2610_bootloader_lpddr4_rdk_defconfig | examples/system_manager/configs/sl2610_pek_system_manager_lpddr4_defconfig |
| DDR3 | configs/SL2610_RDK/sl2610_bootloader_ddr3_rdk_defconfig | examples/system_manager/configs/sl2610_rdk_system_manager_ddr3_defconfig |

------------------------------------------------------------------------

## DDR Selection (Kconfig Symbols)

CONFIG_DDR_TYPE_DDR4\
CONFIG_DDR4_CHIP_2X8\
CONFIG_DDR4_CHIP_1X8\
CONFIG_DDR4_CHIP_1X16\
CONFIG_DDR_TYPE_DDR3\
CONFIG_DDR_TYPE_LPDDR4

------------------------------------------------------------------------

## Build custom DDR on M52

This section explains how to modify and build for a new DDR type on MCU SRSDK.

### DDR profile mapping

| DDR profile | M52 BL | M52 SM |
| --- | --- | --- |
| DDR4 2x8 (default profile) | configs/SL2610_RDK/sl2610_bootloader_rdk_defconfig | examples/system_manager/configs/sl2610_rdk_system_manager_defconfig |
| DDR4 1x16 | configs/SL2610_RDK/sl2610_bootloader_ddr4_1x16_rdk_defconfig | examples/system_manager/configs/sl2610_rdk_system_manager_ddr4_1x16_defconfig |
| LPDDR4 | configs/SL2610_RDK/sl2610_bootloader_lpddr4_rdk_defconfig | examples/system_manager/configs/sl2610_pek_system_manager_lpddr4_defconfig |
| DDR3 | configs/SL2610_RDK/sl2610_bootloader_ddr3_rdk_defconfig | examples/system_manager/configs/sl2610_rdk_system_manager_ddr3_defconfig |

### Add new DDR parameter header

1. Copy the new DDR params header file to:

```text
off_chip_components/dhl_ddr/param_tbl/<DDR4/DDR3/LPDDR4>/<new_ddr_chip_type.h>
```

2. Include the same header in:

```text
off_chip_components/dhl_ddr/param_tbl/ddr_params.h
```

### DDR4 selection override

For DDR4, you can override:

- ddr_params[DIAG_DHL_DDR_TYPE_DDR4].param_table
- ddr_params[DIAG_DHL_DDR_TYPE_DDR4].param_table_size

based on selected defconfig options such as CONFIG_DDR4_CHIP_2X8, CONFIG_DDR_RATE, and CONFIG_DDR_TYPE.

```c
if (ddr4_cfg == DDR4_CFG_8X2_2GBx2 || ddr4_cfg == DDR4_CFG_8X2_1GBx2) {
	  if (CONFIG_DDR_RATE == 3200) {
		  ddr_params[DIAG_DHL_DDR_TYPE_DDR4].param_table = init_ddr4_2x8_pek_3200_bin;
		  ddr_params[DIAG_DHL_DDR_TYPE_DDR4].param_table_size = init_ddr4_2x8_pek_3200_bin_len;
	  } else if (CONFIG_DDR_RATE == 1600) {
		  ddr_params[DIAG_DHL_DDR_TYPE_DDR4].param_table = init_ddr4_2x8_pek_1600_bin;
		  ddr_params[DIAG_DHL_DDR_TYPE_DDR4].param_table_size = init_ddr4_2x8_pek_1600_bin_len;
	  } else {
		  LOG_ERROR(LOG_MOD_SYSTEM, "Unsupported DDR rate: %d\n", CONFIG_DDR_RATE);
		  return DDR_INIT_ERROR_PARAM;
	  }
} else if (ddr4_cfg == DDR4_CFG_8X1_2GBx1 || ddr4_cfg == DDR4_CFG_8X1_1GBx1) {
	ddr_params[DIAG_DHL_DDR_TYPE_DDR4].param_table = init_ddr4_1x8_b0_pek_3200_bin;
	ddr_params[DIAG_DHL_DDR_TYPE_DDR4].param_table_size = init_ddr4_1x8_b0_pek_3200_bin_len;
} else if (ddr4_cfg == DDR4_CFG_16X1_CUS) {
	ddr_params[DIAG_DHL_DDR_TYPE_DDR4].param_table = init_ddr4_1x16_c81_3200_bin;
	ddr_params[DIAG_DHL_DDR_TYPE_DDR4].param_table_size = init_ddr4_1x16_c81_3200_bin_len;
}
```

### DDR3 and LPDDR4 updates

For DDR3 and LPDDR4, place new params arrays in:

```text
off_chip_components/dhl_ddr/dhl_lib.c
```

inside the struct definition:

```c
struct ddr_param ddr_params[]
```

Then recompile the code.

### Build requirement

Since DDR init is enabled in M52 BL, build both:

- sl2610_bootloader_rdk_defconfig
- corresponding system manager defconfig (for example, sl2610_rdk_system_manager_defconfig)

For detailed build steps, refer to [SL2610 Build and Flash with CLI](https://synaptics-astra-mcu.github.io/doc/v/latest/srsdk/docs/SL2610/SL2610_Build_and_Flash_with_CLI.html)

Or the same guide included in the source tree:

```text
docs/SL2610/SL2610_Build_and_Flash_with_CLI.md
```

------------------------------------------------------------------------

## Build Steps (Native Flow)

``` bash
# -----------------------------
# Build Bootloader
# -----------------------------
rm -rf
make clean
make sl2610_bootloader_rdk_defconfig BUILD=SRSDK BOARD=SL2610_RDK
make

# -----------------------------
# Build System Manager
# -----------------------------
cd examples/system_manager/ || exit 1
rm -rf install
rm -rf build
rm -rf out
make clean
make sl2610_rdk_system_manager_defconfig BUILD=SRSDK BOARD=SL2610_RDK
```

------------------------------------------------------------------------

## Generate Images

``` bash
make imagegen
```

------------------------------------------------------------------------

## Output Artifacts

examples/out/nexus_bin/

Expected files:

sl2610_bootloader_extras.bin\
sl2610_bootloader_output.bin\
sl2610_cm52_fw_extras.bin\
sl2610_cm52_fw_output.bin

------------------------------------------------------------------------

## Yocto Integration

Prepare build environment
	source meta-synaptics/setup/setup-environment -> (conf/machine/sl2619.conf)
	devtool modify synasdk-preboot

Copy binaries into DDR-specific Yocto paths (example shown for DDR4):
build-sl2619/workspace/sources/synasdk-preboot/boot/mcu/cm52/image/chip/klamath/klamath_rdk/ddr4/

Rename as:

sl2610_bootloader_extras.bin -> apbl_extras.bin\
sl2610_bootloader_output.bin -> apbl_output.bin\
sl2610_cm52_fw_extras.bin -> fw_extras.bin\
sl2610_cm52_fw_output.bin -> fw_output.bin

Then build Yocto to generate the full eMMC image.

------------------------------------------------------------------------

## Prepare USB boot tool

After successful build of M52 BL and system manager application:

1. Copy the following files into the USB boot tool DDR folder:

```text
examples/system_manager/out/image/usb_boot/m52bl.bin
examples/system_manager/out/image/usb_boot/sysmgr.bin
```

