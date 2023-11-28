Astra SDK User Guide
====================

Overview
--------

This guide describes Synaptics specific configurations and procedures
required to build and use Yocto images with the supported Synaptics
SoC and development boards.

This guide assumes that the reader already has some familiarity
with Yocto concepts. For introductory material about Yocto and general
Yocto reference guides, please refer to the official
`Yocto Documentation <https://docs.yoctoproject.org/>`_.

This BSP works with the Yocto Kirkstone release and provides support
for the following machines, distributions and images:

.. table:: Supported machines, distributions and images

    +---------+--------------+-------------------+
    | Machine | Distribution | Images            |
    +=========+==============+===================+
    | vs640   | poky         | syna-media        |
    +         +--------------+-------------------+
    |         | poky-voip    | syna-media-voip   |
    +---------+--------------+-------------------+
    | vs680   | poky         | syna-media        |
    +         +--------------+-------------------+
    |         | poky-voip    | syna-media-voip   |
    +---------+--------------+-------------------+
    | dvf101  | poky         | qt-image-dspg     |
    |         |              | core-image-dspg   |
    +---------+--------------+-------------------+
    | dvf9919 | poky         | qt-image-dspg     |
    |         |              | core-image-dspg   |
    +---------+--------------+-------------------+

The ``poky`` images are intended for general use. The ``poky-voip``
distribution and related images are intended for use with Synaptics
VOIP stack which is available under dedicated license.

Obtaining the sources
---------------------

The sources of the Synaptics Yocto release can be downloaded using the
`repo tool <https://android.googlesource.com/tools/repo>`_. The instructions
on how to install this tool can be found on
`here <https://source.android.com/docs/setup/download#installing-repo>`_.

The repo tool uses a manifest that lists all the git repositories that are required
to build valid images. The URL and branch of repository containing the manifest for
the BSP variants and versions available to you can be obtained from your Synaptics
contact.

In order to access the manifest and the related repositories you must first enroll
a SSH private key and whitelist your IP address with the Synaptics distribution server.
Your Synaptics contact can help you with this process.

Once you have obtained the manifest URL and branch, whitelisted your IP and keys
you can obtain the sources with the following commands::

  $ repo init -u ${URL} -b ${BRANCH}

  $ repo sync -dc

.. warning::

    The repo tool relies on a correctly configured git installation. In case of problems when
    executing the above commands please make sure git can successfully clone the URL of
    the manifest repository. Typical problems include not using the SSH key enrolled with
    Synaptics or connecting via an IP address not whitelisted with Synaptics.

Build host requirements
-----------------------

The recommended hardware is a ``x86_64`` host with at least:

  * 16 cores
  * 32 GB of RAM
  * 150 GB of disk

As an example, building from scratch the ``syna-media`` image for ``vs640`` on a
``c5a.4xlarge`` AWS instance, which matches the requirements above, takes
approximately 2 hours.

Yocto build system can very efficiently exploit more cores if these are available.

.. note::
    Building entirely from NFS mounted directories is not supported
    by the Yocto build system. Please refer to
    `Yocto documentation on the TMPDIR variable <https://docs.yoctoproject.org/ref-manual/variables.html?highlight=nfs#term-TMPDIR>`_
    for more details.

The recommended software configuration is the following:

  * Ubuntu 22.04 LTS
  * Docker 20.10.25 (package ``docker.io``)

Other versions of Linux and Docker may also work.

The build can also be executed directly on the host provided that the Yocto build
dependencies are installed but this configuration is not supported by Synaptics.

Quick start
-----------

Create the build environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to ensure a correctly configured and clean environment, the build
must be performed within a Docker container. The first step is to build a
Docker image that contains the build system dependencies and is correctly configured
to run the build::

  $ docker build --pull meta-synaptics/setup/docker -t crops/poky

The next step is to start a shell in a new temporary container that will host
the build. The container can be terminated when the build is finished
and a new container can be started later to rebuild. To start the
container use the following command line::

  $ docker run --rm -it -v $(pwd):$(pwd) crops/poky --workdir=$(pwd)

.. note::
   On Ubuntu 20 and 18 LTS the seccomp protection feature of docker has to be
   disabled when creating the build container using the parameter
   ``--security-opt "seccomp=unconfined"``.

This will spawn a shell inside the container. The current directory of the host
is mounted inside the container so that the Yocto sources are available within
the container.

Build an image for ``vs640`` and ``vs680``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To build a ``poky`` image execute the following commands::

  pokyuser@xxxx:yyyy$ source meta-synaptics/setup/setup-environment

  pokyuser@xxxx:yyyy$ bitbake syna-media

To build a ``poky-voip`` image execute the following commands::

  pokyuser@xxxx:yyyy$ source meta-synaptics/setup/setup-environment-voip

  pokyuser@xxxx:yyyy$ bitbake syna-media-voip

The resulting image can be found in ``build-${MACHINE}/tmp/deploy/images/${MACHINE}/SYNAIMG/``.

The image can be flashed to an evaluation kit board as described in :ref:`flashing`.

After flashing the board, to log in to the board please refer to :ref:`shell`.

Build an image for ``dvf101`` and ``dvf9919``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To build an image for ``dvf101`` and ``dvf9919``::

  pokyuser@xxxx:yyyy$ source meta-synaptics-dvf/setup/setup-environment

  pokyuser@xxxx:yyyy$ bitbake ${IMAGE_NAME}

where ``${IMAGE_NAME}`` can be either ``core-image-dspg`` or ``qt-image-dspg``.

The resulting image is available in ``build-${MACHINE}/tmp/deploy/images/${MACHINE}/``

Compatible Layers
-----------------

This BSP is compatible with these layers:

  * ``poky`` [branch: ``kirkstone``]

  * ``meta-openembedded`` [branch: ``kirkstone``]

    * ``meta-oe`` (required by ``meta-python`` below)
    * ``meta-python`` (required by ``meta-multimedia`` below)
    * ``meta-multimedia`` (optional - for gstreamer support)

  * ``meta-qt`` [branch ``qt/upstream/kirkstone`` ] (optional)


Images
------

``syna-media`` and ``syna-media-voip``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``syna-media`` image, based on the ``poky`` distribution, provides a basic graphical
system with ``weston`` and it is suitable to test ``vs640`` and ``vs680`` features. It is the
recommended image for the VideoSmart evaluation boards.

The ``syna-media-voip`` image, based on the ``poky-voip`` distribution provides a base image
to develop VOIP products based on ``vs640`` and ``vs680`` using the Synaptics VOIP stack.
It is intended to be used with a VOIP enabled Synaptics release and the VOIP extension
board for the evaluation kit. The image contains ``weston`` and ``qtwayland``.

Both images require some specific configurations in ``conf/local.conf`` to work correctly.
The ``meta-synaptics/setup/setup-environment`` script can be used to correctly setup a
``syna-media`` build automatically. The ``meta-synaptics/setup/setup-environment-voip``
script can be used to correctly setup a ``syna-media-voip`` build automatically.

For more details about these configurations please refer to the comments in the
sample ``local.conf`` found in ``meta-synaptics/setup/conf/local.conf.sample``.

In order to be able to run qt application on wayland the following package must also
be added. This must be enable manually even when using ``setup/setup-environment``::

  DISTRO_EXTRA_RDEPENDS_append = " qtwayland"

``core-image-dspg`` and ``qt-image-dspg``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Both images require some require some specific configurations in ``conf/local.conf``
to work correctly. The ``meta-synaptics-dvf/setup/setup-environment`` script can be used
to correctly setup a build automatically.

For more details about these configurations please refer to the comments in the
sample ``local.conf`` found in ``meta-synaptics-dvf/setup/conf/local.conf.sample``.

Architecture for ``vs640`` and ``vs680``
========================================

Boot
----

Boot is initiated from ROM code that loads early boot compoents for either SPI or eMMC
boot partitions (selected via pins). For details on how to select SPI vs eMMC boot
please refer to the hardware data sheet.

Early boot components in the eMMC boot partition initialize the system including TEE,
the system manager CPU and the DRAM controller. Different versions of the early
boot components are available to support different memory configurations (see
:numref:`system_memory_config`).

Once the early boot is complete an OEM bootloader is loaded from the eMMC and is
started. This bootloader then loads the Linux kernel and an optional initial ram disk
and starts it. Linux then mounts the main rootfs and starts the user space.

Early boot components load some of the required binaries from the UDA of the eMMC by
looking up the GPT partition table that must be present (see :numref:`partitions_config`
for more details).

In case of failure of loading from the first eMMC boot partition, the boot code
automatically switches to the second boot partition using the ``PARTITION_CONFIG``
register of the eMMC. This register can be inspected to detect which boot partition
successfully loaded the system.

Early boot supports A/B boot of the rest of the system. All other system partitions
are available in two copies. The early boot finds the currently active boot flow by
reading a dedicated partition of the eMMC and initiates loading from partitions
belonging to that boot flow. Successive boot stages load the rest of the system
from the same bootflow. In case the early boot flow notices multiple successive
failure of boot it switches to the alternate bootflow.

A/B bootflow and early boot failover are independent. This means that the first boot
partition (respectively the second) can boot with both A and B boot flows.

Configuration for ``vs640`` and ``vs680``
=========================================

Kernel command line
-------------------

The kernel command line is defined by the variable ``CMDLINE`` of the ``linux-syna``
recipe.


.. _system_memory_config:

System Memory configuration
---------------------------

System memory configuration is performed by changing the variables ``CONFIG_PREBOOT_``
in the configuration file pointed by ``SYNA_SDK_CONFIG_FILE`` variable. The available
configurations can be discovered by inspecting the ``syna-release/boot/preboot/prebuilts/``
directory.

.. _partitions_config:

Partition tables
----------------

Partition tables are configured in the file ``emmc.pt`` in the directory
``syna-release/configs/product/${SYNA_SDK_CONFIG_NAME}/emmc.pt``. The
``SYNA_SDK_CONFIG_NAME`` depends on the ``MACHINE`` and ``DISTRO_CONFIG`` variables.

Some partitions are used by the early boot components stored in eMMC boot partition. These
partitions cannot be removed but can be moved. The early boot components locate these partitions
using the GPT found in the UDA. Loading from other hardware partitions is not supported.

The default partition table of ``vs640`` for the ``poky`` distro are
is described in :numref:`vs640_partitions`.

.. tabularcolumns:: |p{0.78125in}|p{2.66493055555556in}|p{0.677083333333333in}|p{1.77083333333333in}|

.. _vs640_partitions:

.. table:: VS640 Poky partition table
    :class: longtable

    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | Partition name    | Contents                                                             | Can be removed   | Accessed by                   |
    +===================+======================================================================+==================+===============================+
    | factory_setting   | MAC address and other factory provisioned files, used by userspace   | No               | Linux Userspace               |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | key_a             | AVB keys, user keys (A copy)                                         | Yes              | Early boot (boot partition)   |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | tzk_a             | TrustZone Kernel (A copy)                                            | Yes              | Early boot (boot partition)   |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | key_b             | AVB keys, user keys (B copy)                                         | Yes              | Early boot (boot partition)   |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | tzk_b             | TrustZone Kernel (B copy)                                            | Yes              | Early boot (boot partition)   |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | bl_a              | OEM Boot loader (A copy)                                             | Yes              | Early boot (boot partition)   |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | bl_b              | OEM Boot loader (B copy)                                             | Yes              | Early boot (boot partition)   |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | boot_a            | Linux Kernel,  loaded by OEM bootloader (A copy)                     | No               | OEM boot loader (bl_a)        |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | boot_b            | Linux Kernel,  loaded by OEM bootloader (B copy)                     | No               | OEM boot loader (bl_b)        |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | firmware_a        | GPU / DSP / SM firmwares, loaded by early boot, required (A copy)    | Yes              | Early boot (boot partition)   |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | firmware_b        | GPU / DSP / SM firmwares, loaded by early boot, required (B copy)    | Yes              | Early boot (boot partition)   |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | rootfs_a          | Root file system, used by Linux, can be changed (A copy)             | No               | Linux (boot_a)                |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | rootfs_b          | Root file system, used by Linux, can be changed (B copy)             | No               | Linux (boot_b)                |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | fastlogo_a        | Fast logo image, loaded by OEM bootloader, can be changed (A copy)   | No               | OEM bootloader (bl_a)         |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | fastlogo_b        | Fast logo image, loaded by OEM bootloader, can be changed (B copy)   | No               | OEM bootloader (bl_b)         |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | devinfo           | Device information (such as serial number, mac address ) required    | Yes              | Early boot (boot partition)   |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | misc              | Boot control settings, required                                      | Yes              | Early boot (boot partition)   |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+
    | home              | Mounted in /home, can be customized                                  | No               | Linux user space              |
    +-------------------+----------------------------------------------------------------------+------------------+-------------------------------+


Operations on ``vs640`` and ``vs680``
=====================================

.. _flashing:

Flashing images
---------------

Prerequisites
^^^^^^^^^^^^^

In order to flash an image to the VS680 and VS640 evaluation kit board you need
the following hardware:

  * VS640 or VS680 evaluation kit board (EVK)
  * Power supply for the EVK
  * Debug board
  * SPI dongle with firmware for the VS chip in use
  * 4-pin UART cable to connect the debug board to the EVK
  * USB cable to connect debug board to the host, the debug board
    connector has a USB Mini format.
  * Host PC running Linux

To flash with an USB drive you also need:

  * USB driver formatted with FAT32 wiht sufficient space to store
    the desired image

To flash via ethernet:

  * TFTP server on the local network
  * DHCP server on the local network
  * Ethernet cable to connect the EVK to the local network

Flashing images with USB drive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Unzip or copy the image files to the USB driver. The resulting
   directory should contain a list of ``subimg.gz`` files and two
   files ``emmc_part_list`` and ``emmc_image_list``.

#. Connect the USB drive to the USB type A port of the EVK.

#. Connect the debug board to the UART connector of the EVK
   using the 4-pin UART cable.

#. Connect the SPI dongle to the connector marked ``SPI`` of EVK,
   the SPI chip should be facing in the same direction as
   SoC.

#. Start a terminal emulator on the host with 115200 baud rate
   (e.g. ``screen /dev/ttyUSB0 115200`` on Linux).

#. Connect the power to the EVK.

#. When on the serial port the prompt ``=>`` is visible, type
   the following command::

     usb2emmc imagedirectoryname

   where ``imagedirectoryname`` is the name of the directory
   created in the first step.

   The SPI firmware will perform the installation of the image to
   the internal eMMC flash of the EVK. When the flashing is
   complete the prompt is again visible.

#. Remove the power from the EVK, remove the USB drive and
   the SPI dongle.


Flashing images with TFTP
^^^^^^^^^^^^^^^^^^^^^^^^^

#. Unzip or copy the image files to a directory published by the
   TFTP server. The resulting directory should contain a list of
   ``subimg.gz`` files and two files ``emmc_part_list`` and
   ``emmc_image_list``.

#. Connect the debug board to the UART connector of the EVK
   using the 4-pin UART cable.

#. Connect the SPI dongle to the connector marked ``SPI`` of EVK,
   the SPI chip should be facing in the same direction as
   SoC.

#. Connect with an ethernet cable the EVK to the local
   network.

#. Start a terminal emulator on the host with 115200 baud rate
   (e.g. ``screen /dev/ttyUSB0 115200`` on Linux)

#. Connect the power to the EVK.

#. When on the serial port the prompt ``=>`` is visible, type
   the following command::

     tftp2emmc IP_OF_TFTP_SERVER:imagedirectoryname

   where ``imagedirectoryname`` is the name of the directory
   created in the first step and ``IP_OF_TFTP_SERVER`` is the IP
   address of the TFTP server.

   The SPI firmware will perform the installation of the image to
   the internal eMMC flash of the EVK. When the flashing is
   complete the prompt is again visible.

#. Remove the power from the EVK, remove the USB drive and
   the SPI dongle.

.. _shell:

Shell access
------------

To log in on the board you can use the root user. The default root password is empty.

The images provide a serial console. To connect to the serial console connect the debug
board to the UART port of the evaluation kit board using the 4-pin cable and to the host PC using an
USB cable. The debug board contains a USB to UART chip that is supported by recent versions
of Linux out of the box.  To connect to the console use a terminal emulator at 115200 baud (e.g.
``screen /dev/ttyUSB0 115200``).

The images also uses DHCP and allow ssh logins when connected using the ethernet port of the
evaluation kit board.

HDMI output configuration
-------------------------

The BSP by default uses 1080p resolution. To change the resolution to 1920x1200 it is possible
modify the ampsvc init script found at ``/etc/init.d/ampsvc`` by adding the following lines::

    /usr/sbin/ampservice -- $OPTARGS &

    +        sleep 2
    +
    +        test_disp setformat 0 109 2 0
    +        test_disp pushframe 2 1920 1200 9 0 0 1 1

.. note::

    If the screen remains black despite setting the correct configuration check that the
    HDCP keys for the board have been correctly installed on the board (see next section).


Factory keys
------------

.. warning::

    Make sure you create a copy of the keys before flashing the board

In order to install from a USB stick the factory keys on the board after flashing use the following
commands::

  $ mount -o remount,rw /factory_setting

  $ cp /media/usb/path_to_the_keys/* /factory_setting

  $ chmod -644 /factory_setting/*

  $ reboot


Demos
-----

Weston and EGL
^^^^^^^^^^^^^^

To install a Qt demo add the following line to your ``conf/local.conf``::

  DISTRO_EXTRA_RDEPENDS_append = " weston-examples"

To run the demo following commands on a root shell on the device::

  $ export XDG_RUNTIME_DIR=/run/user/0/

  $ weston-simple-egl

A demo application that will appear on the HDMI output.

Qt
^^

To install a Qt demo add the following line to your ``conf/local.conf``::

  DISTRO_EXTRA_RDEPENDS_append = " cinematicexperience"

To run the demo following command on a root shell on the device::

  $ export XDG_RUNTIME_DIR=/run/user/0/

  $ /usr/share/cinematicexperience-1.0/Qt5_CinematicExperience -platform wayland

An QT demo application will start on the HDMI output. To control the application
connect a keyboard and/or mouse to the USB3 port of the board.

gstreamer OpenGL intergration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To install a Qt demo add the following line to your ``conf/local.conf``::

  DISTRO_EXTRA_RDEPENDS_append = " gstreamer1.0-plugins-base-opengl"

To run the demo following command on a root shell on the device::

  $ export XDG_RUNTIME_DIR=/run/user/0/

  $ gst-launch-1.0 videotestsrc !  glimagesink

A video player will start on the HDMI output showing a test signal.


Operations on ``dvf101`` and ``dvf9919``
========================================

Please refer to the ``BSP_Manual`` document that you can request to your Synaptics contact.

Frequently Asked Questions
==========================

How do I override the value of to a recipe variable in ``local.conf``?

  To append the text ``some text`` to the variable ``FOO`` of recipe ``bar`` add
  the following line to ``local.conf``::

    FOO:append:pn-bar = " some text"

  Other changes to the variable can be performed with the standard operators
  described in the `Bitbake Guide <https://docs.yoctoproject.org/bitbake/2.4/bitbake-user-manual/bitbake-user-manual-metadata.html#basic-syntax>`_.

Troubleshooting
===============


The build fails at the package ``gdk-pixbuf-native`` with error ``Failed to
close file descriptor for child process`` on Ubuntu 20 or 18.

  This problem is caused by an incompatibility of the package build system with the ``libseccomp``
  library on the host that is running docker. To solve this issue update the libseccomp2 library
  on the host that runs docker or add the parameter ``--security-opt "seccomp=unconfined`` to
  the docker command line when creating the docker build environment.

Build of packages with out-of-trees modules (such as ``synasdk-synap-module``) fail with error
``Kernel configuration is invalid.``.

  Under some circumstatances the state of the recipe ``make-mod-scripts`` may become corrupted. To fix
  the issue clean the recipe with the command::

    bitbake -c cleansstate make-mod-scripts
