==================
NAND Customization
==================

Astra supports using NAND for the main internal storage with SL2610. The machine types ``sl2611nand``, ``sl2615nand``, and ``sl2619nand`` are configured to use a default 256MB SPI NAND (2K page size).
However, other NAND configurations can be used. This guide details how to modify the SDK to use different NAND configurations.

Changing the NAND Configuration
===============================

The NAND configuration is included in the `synasdk-config-native`` package. Use the ``devtool`` utility to
modify the config file::

    devtool modify synasdk-config-native

The ``devtool`` utility will create the ``build-sl2619nand/workspace/sources/synasdk-config-native/configs/product`` directory which will contain the source for
the config package. In the product directory is a subdirectory containing a config file for each of the  platforms. Modify the files
based on the sections below.

Changing the NAND Size
----------------------

The NAND configuration is defined in the ``Image Generation Configuration`` of the profile ``defconfig`` file.

.. figure:: media/nand-image-generation-section.png

    Image Generation Configuration section of the defconfig

Update the sizes for your specific NAND. For example, switching to a 512MB (4K) NAND wou

.. figure:: media/update-nand-sizes.png

    Patch updating sizes in ``sl2619_nand_poky_aarch64_rdk_defconfig``.


Changing Partition Sizes
------------------------

The NAND partition layout is set in the ``nand.pt`` file.

.. figure:: media/update-nand-flash-type.png

    Updating the NAND Flash Type Configuration

Changing the Flash Type Configuration
-------------------------------------

The Flash Type configuration is stored in ``flash_type.cfg`` file.

.. figure:: media/update-nand-flash-type.png

    Updating the NAND Flash Type Configuration

Changing the NAND Width
-----------------------

Updating the NAND Width in U-Boot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The NAND width is configured in the Linux and U-Boot devicetree . The default width is ``2``
for a Dual SPI Configuration. Update the dts file widths to ``4`` for Quad SPI Configuration.

The NAND U-Boot devicetree is included in the ``syna-u-boot`` package. Use the ``devtool`` utility to
modify the config file::

    devtool modify syna-u-boot

The ``devtool`` utility will create the ``build-sl2619nand/workspace/sources/syna-u-boot/boot/u-boot`` directory which will contain the source for

Modify the ``spi-tx-bus-width`` and ``spi-rx-bus-width`` in ``arch/arm/dts/klamath-rdk-nand.dts``.

.. figure:: media/devicetree-nand-width-u-boot.png

    Updating the NAND Width in Device Tree

Updating the NAND Width in Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The NAND Linux devicetree is included in the ``linux-syna`` package. Use the ``devtool`` utility to
modify the config file::

    devtool modify linux-syna

The ``devtool`` utility will create the ``build-sl2619nand/workspace/sources/linux-syna`` directory which will contain the source for

Modify the ``spi-tx-bus-width`` and ``spi-rx-bus-width`` in ``arch/arm64/boot/dts/synaptics/sl2619-nand-rescue-rdk.dts``.

.. figure:: media/devicetree-nand-width-linux.png

    Updating the NAND Width in Device Tree

Building the Updated Image
==========================

Finally, build an image with the modified NAND configuration::

    bitbake -f synasdk-config-native
    bitbake -f syna-u-boot -c compile
    bitbake -f linux-syna -c compile
    bitbake -f astra-media -c compile
    bitbake -f astra-media
