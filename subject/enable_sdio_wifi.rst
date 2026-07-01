========================================
Enabling SDIO WiFi for SL1640 and SL1680
========================================

By default, SL1640 and SL1680 are configured to use PCIe based WiFi modules. But, SDIO support with the 43711S WiFi module
can be enabled by updating the Linux Kernel's DTS and config.

Modifying the Kernel
====================

This requires modifying the ``linux-syna`` package using ``devtool``::

    devtool modify linux-syna

Updating the DTS File
---------------------

Modify the platform dts file located in ``build-sl1680/workspace/sources/linux-syna/arch/arm64/boot/dts/synaptics``.

+-----------------+------------------+-----------------+
|                 | SL1640           | SL1680          |
+-----------------+------------------+-----------------+
| DTS             | platypus-rdk.dts | dolphin-rdk.dts |
+-----------------+------------------+-----------------+

The following sections need to be added / modified. The sections in ``dolphin-rdk.dts`` and ``platypus-rdk.dts`` are identical so the
below patch applies to both platforms.

::

    diff --git a/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts b/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts
    index f3bf406ee518..31dc31d08e30 100644
    --- a/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts
    +++ b/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts
    @@ -85,6 +85,12 @@ dmabuf_heap {
            pool-attributes = <0x00000105 0x00000F3A 0x00000102 0x00000F3D>;
        };
    
    +	sdhci1_pwrseq: sdhci1-pwrseq {
    +           	compatible = "mmc-pwrseq-simple";
    +           	reset-gpios = <&expander1 2 GPIO_ACTIVE_LOW>;
    +           	post-power-on-delay-ms = <50>;
    +   	};
    +
        regulators {
            compatible = "simple-bus";
            #address-cells = <1>;
    @@ -417,15 +423,15 @@ &sdhci0 {
    
    &sdhci1 {
        status = "okay";
    -	pinctrl-0 = <&sdhci1_pmux>, <&sdhci1_gpio_pmux>;
    -	pinctrl-names = "default";
    -	no-sdio;
    +	bus-width = <4>;
    +	no-sd;
        no-mmc;
    -	disable-wp;
    -	sdclkdl-dc = /bits/ 8 <75>;
    -	pad-sp = /bits/ 8 <4>;
    -	pad-sn = /bits/ 8 <4>;
    -	vmmc-supply = <&vmmc_sdhci1>;
    +	non-removable;
    +	mmc-pwrseq = <&sdhci1_pwrseq>;
    +	mode1-tune;
    +	sdclkdl-dc = /bits/ 8 <35>;
    +	pad-sp = /bits/ 8 <12>;
    +	pad-sn = /bits/ 8 <12>;
    };

    &pcie_phy0 {

Updating the defconfig
----------------------

Modify the ``defconfig`` file located in ``build-sl1680/workspace/sources/linux-syna/arch/arm64/configs``.

+-----------------+--------------------+-------------------+
|                 | SL1640             | SL1680            |
+-----------------+--------------------+-------------------+
| defconfig       | platypus_defconfig | dolphin_defconfig |
+-----------------+--------------------+-------------------+

The following sections need to be added / modified. The sections in ``dolphin_defconfig`` and ``platypus_defconfig`` are identical so the
below patch applies to both platforms.

::

    diff --git a/arch/arm64/configs/dolphin_defconfig b/arch/arm64/configs/dolphin_defconfig
    index 2c442ca0b26b..cd163c3e6efd 100644
    --- a/arch/arm64/configs/dolphin_defconfig
    +++ b/arch/arm64/configs/dolphin_defconfig
    @@ -177,10 +177,10 @@ CONFIG_SYNA_CLK_BASE=y
    CONFIG_SYNA_DOLPHIN_CLK=y
    CONFIG_PINCTRL_DOLPHIN=y
    CONFIG_MMC_SDHCI_OF_DWCMSHC=y
    -CONFIG_PCIE_BERLIN=y
    +#CONFIG_PCIE_BERLIN=y
    CONFIG_REGULATOR_HL7593=m
    CONFIG_REGULATOR_RPI_PANEL_ATTINY=m
    -CONFIG_PHY_BERLIN_PCIE=y
    +#CONFIG_PHY_BERLIN_PCIE=y
    CONFIG_PHY_SYNA_USB=y
    CONFIG_SENSORS_DOLPHIN=y
    CONFIG_I2C_DYNDMX_PINCTRL=y
    @@ -211,13 +211,11 @@ CONFIG_BCMDHD103=y
    CONFIG_BCMDHD591=y
    CONFIG_BCMDHD361=y
    CONFIG_BCMDHD=m
    -CONFIG_BCMDHD_PCIE=y
    +CONFIG_BCMDHD_SDIO=y
    CONFIG_BCM4362=y
    CONFIG_DHD_OF_SUPPORT=y
    -CONFIG_DHD_USE_SCHED_SCAN=y
    # CONFIG_WLAIBSS is not set
    # CONFIG_WL_RELMCAST is not set
    -CONFIG_BCMDHD_PCIE_RUNTIMEPM=y
    # CONFIG_SYNAPTICS_VIDEO is not set
    CONFIG_SND_SOC_SYNA=m
    CONFIG_SND_SOC_BERLIN_ASOC=m

Build the Updated Image
-----------------------

Build the image with the updated device tree entries::

   devtool build linux-syna
   devtool build-image astra-media