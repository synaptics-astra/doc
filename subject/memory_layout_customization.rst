============================================
Memory Layout Customization on Astra Machina
============================================

Astra Machina uses DRAM for several components in the SoC. The DRAM is divided up into several sections
depending on what it is used for. These sections include System memory, NonSecure (CMA), NonSecure (non-cached),
and Secure memory. System memory is the memory available to the Linux kernel. Included in System memory
is the NonSecure section which is used by the kernel for CMA. Secure memory is reserved for when the SoC
is operating secure environments such as TrustZone, and is not accessible to Linux. The NonSecure
(non-cached) section is reserved for SoC components which require non-cached memory.

Memory Layouts
--------------

Astra Machina supports predefined memory layouts for various DDR configurations. The default configuration
can be changed based on the amount of DDR in the system.

.. note::

    Modifying the size of the memory sections requires Synaptics to resign the preboot firmware and are not
    user modifiable.

======== ============== ================
Chip     Default Memory Supported Memory
======== ============== ================
SL1620   2GB            1GB / 2GB / 4GB
SL1640   2GB            2GB / 4GB
SL1680   4GB            2GB / 4GB
======== ============== ================

Below are the memory layouts for all available DDR sizes.

SL1620 Memory Layout
^^^^^^^^^^^^^^^^^^^^

+-------------------+------------------------+----------------------------+
| Memory Size       | Memory Section         | Size                       |
+-------------------+------------------------+----------------------------+
| 1 GB DDR          | NonSecure (CMA)        | 64MB                       |
|                   +------------------------+----------------------------+
|                   | System                 | 930MB                      |
|                   +------------------------+----------------------------+
|                   | NonSecure (Non-cached) | 4MB                        |
|                   +------------------------+----------------------------+
|                   | Secure                 | 16MB                       |
+-------------------+------------------------+----------------------------+
| 2 GB DDR          | NonSecure (CMA)        | 512MB                      |
|                   +------------------------+----------------------------+
|                   | System                 | 1.950GB                    |
|                   +------------------------+----------------------------+
|                   | NonSecure (Non-cached) | 8MB                        |
|                   +------------------------+----------------------------+
|                   | Secure                 | 16MB                       |
+-------------------+------------------------+----------------------------+
| 4 GB DDR          | NonSecure (CMA)        | 64MB                       |
|                   +------------------------+----------------------------+
|                   | System                 | 3.482GB                    |
|                   +------------------------+----------------------------+
|                   | NonSecure (Non-cached) | 8MB                        |
|                   +------------------------+----------------------------+
|                   | Secure                 | 16MB                       |
+-------------------+------------------------+----------------------------+

SL1640 Memory Layout
^^^^^^^^^^^^^^^^^^^^

+-------------------+------------------------+----------------------------+
| Memory Size       | Memory Section         | Size                       |
+-------------------+------------------------+----------------------------+
| 2 GB DDR          | NonSecure (CMA)        | 260MB                      |
|                   +------------------------+----------------------------+
|                   | System                 | 1.948GB                    |
|                   +------------------------+----------------------------+
|                   | NonSecure (Non-cached) | 8MB                        |
|                   +------------------------+----------------------------+
|                   | Secure                 | 16MB                       |
+-------------------+------------------------+----------------------------+
| 4 GB DDR          | NonSecure (CMA)        | 500MB                      |
|                   +------------------------+----------------------------+
|                   | System                 | 3.482GB                    |
|                   +------------------------+----------------------------+
|                   | NonSecure (Non-cached) | 8MB                        |
|                   +------------------------+----------------------------+
|                   | Secure                 | 16MB                       |
+-------------------+------------------------+----------------------------+

SL1680 Memory Layout
^^^^^^^^^^^^^^^^^^^^

+-------------------+------------------------+----------------------------+
| Memory Size       | Memory Section         | Size                       |
+-------------------+------------------------+----------------------------+
| 2 GB DDR          | NonSecure (CMA)        | 260MB                      |
|                   +------------------------+----------------------------+
|                   | System                 | 1.948GB                    |
|                   +------------------------+----------------------------+
|                   | NonSecure (Non-cached) | 8MB                        |
|                   +------------------------+----------------------------+
|                   | Secure                 | 16MB                       |
+-------------------+------------------------+----------------------------+
| 4 GB DDR          | NonSecure (CMA)        | 500MB                      |
|                   +------------------------+----------------------------+
|                   | System                 | 3.482GB                    |
|                   +------------------------+----------------------------+
|                   | NonSecure (Non-cached) | 8MB                        |
|                   +------------------------+----------------------------+
|                   | Secure                 | 16MB                       |
+-------------------+------------------------+----------------------------+

Changing the Memory Layout
--------------------------

The memory layout is set in the configuration file included in the ``synasdk-config-native`` package. Use the ``devtool`` utility to
modify the config file::

    devtool modify synasdk-config-native

The ``devtool`` utility will create the ``build-sl1680/workspace/sources/synasdk-config-native/configs/product`` directory which will contain the source for
the config package. This directory will contain a subdirectory containing a config file for each of the  platforms. Edit the config file for the platform which
you are building for. Set the ``CONFIG_TZK_MEM_LAYOUT`` parameter to the layout which matches the about of DDR on your board. The supported memory layouts are listed
below in the ``CONFIG_TZK_SUPPORTED_MEM_LAYOUT`` parameter.

For example, to change the memory layout for SL1620, edit ``sl1620_poky_aarch64_rdk/sl1620_poky_aarch64_rdk_defconfig``.

.. figure:: media/sl1620-config-mem-layout.png

For SL1640 ``sl1640_poky_aarch64_rdk/sl1640_poky_aarch64_rdk_defconfig`` and SL1680 ``sl1680_poky_aarch64_rdk/sl1680_poky_aarch64_rdk_defconfig``

.. figure:: media/sl1680-config-mem-layout.png

Finally, build an image with the modified memory layout::

    devtool build synasdk-config-native
    devtool build-image astra-media