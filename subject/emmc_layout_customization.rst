=============================================
eMMC Partition Customization on Astra Machina
=============================================

The main internal storage used for Astra Machina is the eMMC chip located on the Core Module. The eMMC has partitions for firmware, the root fs, and a home partition.
These partitions can be resized to allow more data to be stored in a specific partition. The most common use case would be to enlarge the root fs to accommodate more packages
being installed on the board.

==============  ======================  ==============  ============    ================
Partition Size  Partition Name          Erase / Format  First Action    Write Protection
==============  ======================  ==============  ============    ================
16M@16M         factory_setting         format          default         none
1M              key_a                   default         default         none
7M              tzk_a                   default         default         none
1M              key_b                   default         default         none
7M              tzk_b                   default         default         none
16M             bl_a                    default         default         none
16M             bl_b                    default         default         none
32M             boot_a                  default         default         none
32M             boot_b                  default         default         none
32M             firmware_a              default         default         none
32M             firmware_b              default         default         none
1408M           rootfs_a                default         default         none
1408M           rootfs_b                default         default         none
16M             fastlogo_a              default         default         none
16M             fastlogo_b              default         default         none
2M              devinfo                 erase           default         none
2M              misc                    erase           default         none
-               home                    default         default         none
==============  ======================  ==============  ============    ================

The default image layout for SL1620, SL1640, and SL1680. As of v1.2.0, the home partition is resized to the use the
remaining space left at the end of the eMMC.

Some partitions have a and b versions. These redundant partitions are used to support system update.

.. note::

    Enlarging an ab partition will require 2x additional space on the eMMC.

Changing Partition Sizes
------------------------

The eMMC partition layout is set in the ``emmc.pt`` file included in the ``synasdk-config-native`` package. Use the ``devtool`` utility to
modify the config file::

    devtool modify synasdk-config-native

The ``devtool`` utility will create the ``build-sl1680/workspace/sources/synasdk-config-native/configs/product`` directory which will contain the source for
the config package. In the product directory is a subdirectory containing a config file for each of the  platforms. Edit the ``emmc.pt`` file for the platform which
you are building for.

For example, to change the root fs partition size for  SL1680, edit ``sl1680_poky_aarch64_rdk/emmc.pt``.

.. figure:: media/sl1680-resize-rootfs-partition.png

    Change made to double the root fs partition on SL1680

Enlarging the Total eMMC Size
-----------------------------

The default eMMC image size is 16GB. This is the minimum eMMC size for Astra Machina Core Modules. If you have a device with a larger eMMC and would
like to allocate more space to system partitions, then you can enlarge the total eMMC size to accommodate the larger partitions.

The total eMMC size is set in the in the configuration file included in the ``synasdk-config-native`` package.  Set the ``CONFIG_EMMC_TOTAL_SIZE`` parameter
to the to the total size of the eMMC on your board.

.. figure:: media/sl1680-enlarge-emmc.png

    Setting the total eMMC size to 32GB on SL1680

Building the Updated Image
--------------------------

Finally, build an image with the modified eMMC partition layout::

    devtool build synasdk-config-native
    devtool build-image astra-media