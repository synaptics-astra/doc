======================================
Enabling SDIO WiFi for SL640 and SL680
======================================

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

    diff --git a/arch/arm64/boot/dts/synaptics/platypus-rdk.dts b/arch/arm64/boot/dts/synaptics/platypus-rdk.dts
    index c7c388d..26ff787 100644
    --- a/arch/arm64/boot/dts/synaptics/platypus-rdk.dts
    +++ b/arch/arm64/boot/dts/synaptics/platypus-rdk.dts
    @@ -69,6 +69,12 @@
            pool-attributes = <0x00000105 0x00000F3A 0x00000102 0x00000F3D>;
        };
    
    +	sdhci1_pwrseq: sdhci1-pwrseq {
    +		compatible = "mmc-pwrseq-simple";
    +		reset-gpios = <&expander1 2 GPIO_ACTIVE_LOW>;
    +		post-power-on-delay-ms = <50>;
    +	};
    +
        regulators {
            compatible = "simple-bus";
            #address-cells = <1>;
    @@ -114,6 +120,12 @@
        bluesleep: bluesleep {
            compatible = "syna,bluesleep";
            bt-dev-wake-gpio = <&expander1 3 GPIO_ACTIVE_HIGH>;
    +	};
    +
    +	bcmdhd {
    +		compatible = "synaptics,bcmdhd_wlan";
    +		wl_reg_on = <&expander1 2 GPIO_ACTIVE_HIGH>;         /* wifi reg_on pin */
    +		wl_host_wake = <&expander1 3 GPIO_ACTIVE_HIGH>;      /* wifi host wake (OOB) pin */
        };
    
        gpio_keys {
    @@ -261,9 +273,11 @@
        pinctrl-0 = <&sdhci1_pmux>, <&sdhci1_gpio_pmux>, <&sdhci1_cd_pmux>;
        pinctrl-names = "default";
        bus-width = <4>;
    -	no-sdio;
    +	no-sd;
        no-mmc;
    -	disable-wp;
    +	non-removable;
    +	mmc-pwrseq = <&sdhci1_pwrseq>;
    +	mode1-tune;
        sdclkdl-dc = /bits/ 8 <75>;
        pad-sp = /bits/ 8 <4>;
        pad-sn = /bits/ 8 <4>;

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

    diff --git a/recipes-kernel/linux/files/platypus_defconfig b/recipes-kernel/linux/files/platypus_defconfig
    index b57eac8..fc22a7e 100644
    --- a/recipes-kernel/linux/files/platypus_defconfig
    +++ b/recipes-kernel/linux/files/platypus_defconfig
    @@ -292,13 +292,14 @@
    # CONFIG_WLAN_VENDOR_ZYDAS is not set
    # CONFIG_WLAN_VENDOR_QUANTENNA is not set
    CONFIG_BCMDHD=m
    -CONFIG_BCMDHD_PCIE=y
    -CONFIG_BCMDHD_PCIE_RUNTIMEPM=y
    +CONFIG_BCMDHD_SDIO=y
    +#CONFIG_BCMDHD_PCIE is not set
    +#CONFIG_BCMDHD_PCIE_RUNTIMEPM is not set
    CONFIG_BCM4362=y
    CONFIG_DHD_OF_SUPPORT=y
    -CONFIG_BCMDHD_FW_PATH="/data/etc/wifi/fw_bcmdhd.bin"
    -CONFIG_BCMDHD_NVRAM_PATH="/data/etc/wifi/bcmdhd.cal"
    -CONFIG_BCMDHD_CLM_PATH="/data/etc/wifi/bcmdhd_clm.blob"
    +#CONFIG_BCMDHD_FW_PATH is not set
    +#CONFIG_BCMDHD_NVRAM_PATH is not set
    +#CONFIG_BCMDHD_CLM_PATH is not set
    CONFIG_DHD_USE_SCHED_SCAN=y
    # CONFIG_WLAIBSS is not set
    # CONFIG_WL_RELMCAST is not set

Build the Updated Image
-----------------------

Build the image with the updated device tree entries::

   devtool build linux-syna
   devtool build-image astra-media