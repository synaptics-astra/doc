==================================
How to enable 12.5mv PMIC on Astra
==================================

Information
===========

-  For SL1680 RDK board only

**Take SY8827N and eMMC boot for example, please apply changes below
then build your image again.**

**Please change defconfig files according to your boot media if not
booting from eMMC.**

1. Configuration for preboot
============================

The configuration file is included in the ``synasdk-config-native`` package. Use the ``devtool`` utility to
modify the config file::

    devtool modify synasdk-config-native

The ``devtool`` utility will create the ``build-sl1680/workspace/sources/synasdk-config-native/configs/product`` directory which will contain the source for
the config package. In the product directory is a subdirectory containing a config file for each of the  platforms. Edit the config file ``sl1680_poky_aarch64_rdk_defconfig``.

::

    diff --git
    a/product/sl1680_poky_aarch64_rdk/sl1680_poky_aarch64_rdk_defconfig
    b/product/sl1680_poky_aarch64_rdk/sl1680_poky_aarch64_rdk_defconfig
    index f3f51295..7b50d704 100755
    --- a/product/sl1680_poky_aarch64_rdk/sl1680_poky_aarch64_rdk_defconfig
    +++ b/product/sl1680_poky_aarch64_rdk/sl1680_poky_aarch64_rdk_defconfig
    @@ -172,29 +172,29 @@ CONFIG_PMIC_IF_I2C=y
    # CONFIG_VCORE_PMIC_MODEL_SY8824B is not set
    # CONFIG_VCORE_PMIC_MODEL_NCP6335D is not set
    # CONFIG_VCORE_PMIC_MODEL_MP886X is not set
    -# CONFIG_VCORE_PMIC_MODEL_SY8827N is not set
    +CONFIG_VCORE_PMIC_MODEL_SY8827N=y
    # CONFIG_VCORE_PMIC_MODEL_HL7593WL06 is not set
    # CONFIG_VCORE_PMIC_MODEL_TPS62868 is not set
    # CONFIG_VCORE_PMIC_MODEL_RT5739 is not set
    # CONFIG_VCORE_PMIC_MODEL_PWM_PMIC is not set
    -CONFIG_VCORE_PMIC_MODEL_TPS6287X=y
    +# CONFIG_VCORE_PMIC_MODEL_TPS6287X is not set
    # CONFIG_VCORE_PMIC_MODEL_RT5733 is not set
    # CONFIG_VCORE_PMIC_MODEL_SMTIMER is not set
    -CONFIG_VCORE_PMIC_MODEL="tps6287x"
    +CONFIG_VCORE_PMIC_MODEL="sy8827n"
    # CONFIG_VCPU_PMIC_MODEL_NONE is not set
    # CONFIG_VCPU_PMIC_MODEL_M88PG86X is not set
    # CONFIG_VCPU_PMIC_MODEL_SY8824B is not set
    # CONFIG_VCPU_PMIC_MODEL_NCP6335D is not set
    # CONFIG_VCPU_PMIC_MODEL_MP886X is not set
    -# CONFIG_VCPU_PMIC_MODEL_SY8827N is not set
    +CONFIG_VCPU_PMIC_MODEL_SY8827N=y
    # CONFIG_VCPU_PMIC_MODEL_HL7593WL06 is not set
    # CONFIG_VCPU_PMIC_MODEL_TPS62868 is not set
    # CONFIG_VCPU_PMIC_MODEL_RT5739 is not set
    # CONFIG_VCPU_PMIC_MODEL_PWM_PMIC is not set
    -CONFIG_VCPU_PMIC_MODEL_TPS6287X=y
    +# CONFIG_VCPU_PMIC_MODEL_TPS6287X is not set
    # CONFIG_VCPU_PMIC_MODEL_RT5733 is not set
    # CONFIG_VCPU_PMIC_MODEL_SMTIMER is not set
    -CONFIG_VCPU_PMIC_MODEL="tps6287x"
    +CONFIG_VCPU_PMIC_MODEL="sy8827n"
    # CONFIG_VCORE_PMIC_I2C_NONE_VAL is not set
    # CONFIG_VCORE_PMIC_I2C_TW0_VAL is not set
    # CONFIG_VCORE_PMIC_I2C_TW1_VAL is not set

2. Configuration for U-Boot
===========================

Add the ``CONFIG_SYNA_PMIC_STEP_12500UV`` option by checking out U-Boot source code using the
 ``devtool`` utility to checkout the U-Boot source code. Use the ``devtool`` utility to modify the source code.::

    devtool modify syna-u-boot

The U-Boot source code has now been checkout out under ``build-sl1680/workspace/sources/syna-u-boot``.

Add below option to ``dolphin_suboot_defconfig``.

::

    diff --git a/configs/dolphin_suboot_defconfig
    b/configs/dolphin_suboot_defconfig
    index 59b0cc946f3..1d57f9723a8 100644
    --- a/configs/dolphin_suboot_defconfig
    +++ b/configs/dolphin_suboot_defconfig
    @@ -20,6 +20,7 @@ CONFIG_MMC_DWCMSHC=y
    CONFIG_ETH_ROM_MAC=y
    CONFIG_SYNA_USB_PHY=y
    CONFIG_SYNA_USB_DWC3=y
    +CONFIG_SYNA_PMIC_STEP_12500UV=y
    CONFIG_SYNA_RESET=y
    CONFIG_SYNA_DWSPI=y
    CONFIG_VIDEO_SYNA=y

3. Configuration for Linux
==========================

Configuring Linux requires modifying the ``linux-syna`` package using ``devtool``::

    devtool modify linux-syna

Modify config file ``build-sl1680/workspace/sources/linux-syna/arch/arm64/configs/dolphin_defconfig``
the platform dts file located in ``build-sl1680/workspace/sources/linux-syna/arch/arm64/boot/dts/synaptics``.


3.1 Configuration for Linux defconfig
-------------------------------------

::

    diff --git a/arch/arm64/configs/dolphin_defconfig
    b/arch/arm64/configs/dolphin_defconfig
    index 5a2325851744..d8495e544b71 100644
    --- a/arch/arm64/configs/dolphin_defconfig
    +++ b/arch/arm64/configs/dolphin_defconfig
    @@ -404,6 +404,7 @@ CONFIG_REGULATOR=y
    CONFIG_REGULATOR_FIXED_VOLTAGE=y
    CONFIG_REGULATOR_GPIO=y
    CONFIG_REGULATOR_RT5739=m
    +CONFIG_REGULATOR_SY8827N=y
    CONFIG_REGULATOR_TPS6287X=y
    # CONFIG_MEDIA_CEC_SUPPORT is not set
    CONFIG_MEDIA_SUPPORT=m

3.2 Configuration for Linux dts
-------------------------------

::

    diff --git a/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts
    b/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts
    index f3bf406ee518..d1de1bfcb42c 100644
    --- a/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts
    +++ b/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts
    @@ -164,9 +164,9 @@ i2c@1 {
                #address-cells = <1>;
                #size-cells = <0>;
        
     -          vcpu: regulator@40 {
     -              compatible = "ti,tps62870";
     -              reg = <0x40>;
     +          vcpu: regulator@60 {
     +              compatible = "silergy,sy8827n";
     +              reg = <0x60>;
                    status = "okay";
                    regulator-boot-on;
                    regulator-always-on;
    @@ -174,6 +174,7 @@ vcpu: regulator@40 {
                    regulator-name = "vcpu";
                    regulator-min-microvolt = <700000>;
                    regulator-max-microvolt = <987500>;
        +           silergy,vsel-step = <1>;
                };
            };
        };
    @@ -190,9 +191,9 @@ i2c@1 {
                #address-cells = <1>;
                #size-cells = <0>;
    
    -           vcore: regulator@40 {
    -               compatible = "ti,tps62870";
    -               reg = <0x40>;
    +           vcore: regulator@60 {
    +               compatible = "silergy,sy8827n";
    +               reg = <0x60>;
                    status = "okay";
                    regulator-boot-on;
                    regulator-always-on;
    @@ -200,6 +201,7 @@ vcore: regulator@40 {
                    regulator-name = "vcore";
                    regulator-min-microvolt = <700000>;
                    regulator-max-microvolt = <987500>;
    +               silergy,vsel-step = <1>;
                };
            };
        };
