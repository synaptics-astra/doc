===================
SPI Boot User Guide
===================

Astra Machina supports booting from SPI NOR Flash. The SPI flash can contain a backup version of U-Boot or a Linux boot
image. Linux boot images require a minimum of 32MB.

.. note::

    Astra Machina Core Modules contain 16MB SPI NOR Flash. Booting Linux from SPI requires a minimum
    of 32MB and is not supported on the Astra Machina Core Module.

Flashing SPI Images
===================

The SPI boot image contains two files. The ``spi_suboot.bin`` file contains boot info, preboot code, the TEE, and SU-Boot.
The ``boot.subimg`` contains the Linux Kernel, DTB, and RAMFS for booting Linux. Prebuilt SPI images are included in the
`Astra SDK Releases <https://github.com/synaptics-astra/sdk/releases>`_. Look for the ``slxxxx_spi_boot_scarthgap`` image.

The SPI image if flashed using U-Boot. It can be flashed using ``astra-update`` or directly from the U-Boot prompt (See :ref:`flash_internal_spi`).

Comments on ``spi_suboot.bin``
------------------------------

- The SPI boot image is named SPI SU-Boot to distinguish it from SPI U-Boot.

- SPI SU-Boot layout is defined in the ``xspi.pt`` file under product configuration folder.

- SPI SU-Boot relies on the misc partition to choose A/B images, system will initialize this misc partition on the first boot.

- If there is a boot issue when you only burn image A, please try to recovery your board by erasing misc partition.
  The system will re-initialization misc during the next boot.

Flashing SPI Images with Astra Update
-------------------------------------

Astra Update can boot U-Boot over the USB interface and then flash the SPI images. Astra Update will need a ``manifest.yaml``
file to know which files to flash and what addresses to program the images. Create this file inside of the spiBOOTimg directory.

Example ``manifest.yaml`` file for flashing on SL2610:

::

    image_type: spi
    chip: sl2610
    board: rdk
    reset: enable

    images:
        spi_suboot.bin:
            read_address: 0x10000000
            write_first_copy_address: 0
            write_second_copy_address: 0x200000
            write_length: $filesize
            erase_first_start_address: 0
            erase_first_length: 0x200000
            erase_second_start_address: 0x200000
            erase_second_length: 0x200000

        boot.subimg:
            read_address: 0x10000000
            write_first_copy_address: 0x3f0000
            write_second_copy_address: 0x11f0000
            write_length: $filesize
            erase_first_start_address: 0x3f0000
            erase_first_length: 0xE00000
            erase_second_start_address: 0x11f0000
            erase_second_length: 0xE00000

Example ``manifest.yaml`` file for flashing on SL1680:

::

    image_type: spi
    chip: sl1680
    board: rdk
    reset: enable

    images:
        spi_suboot.bin:
            read_address: 0x10000000
            write_first_copy_address: 0xf0000000
            write_second_copy_address: 0xf0200000
            write_length: 0x1f0000
            erase_first_start_address: 0xf0000000
            erase_first_length: 0xf01fffff
            erase_second_start_address: 0xf0200000
            erase_second_length: 0xf03fffff

        boot.subimg:
            read_address: 0x10000000
            write_first_copy_address: 0xf0400000
            write_second_copy_address: 0xf1200000
            write_length: 0xd0c990
            erase_first_start_address: 0xf0400000
            erase_first_length: 0xf11fffff
            erase_second_start_address: 0xf1200000
            erase_second_length: 0xf1ffffff

.. note::

    Delete the ``boot.subimg`` entry if only flashing ``spi_suboot.bin``.

Flashing SPI Images with U-Boot
-------------------------------

Flashing Image from an External USB Drive on SL16x0
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Flash the ``spi_suboot.bin`` to slots A and B.

::

    usb start; fatload usb 0 0x10000000 spi_suboot.bin
    spinit;
    erase f0000000 f01fffff; cp.b 0x10000000 0xf0000000 $filesize;
    erase f0200000 f03fffff; cp.b 0x10000000 0xf0200000 $filesize;

Flash the ``boot.subimg`` to slots A and B.

::

    usb start; fatload usb 0  0x10000000 boot.subimg
    spinit;
    erase f0400000 f11fffff; cp.b 0x10000000 f0400000 $filesize;
    erase f1200000 f1ffffff; cp.b 0x10000000 f1200000 $filesize; //For 32MB SPI NOR onlyy

Flashing Image from an External USB Drive on SL2610
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Flash the ``spi_suboot.bin`` to slots A and B.

::

    usb start; fatload usb 0 0x10000000 spi_suboot.bin
    sf probe;
    sf erase 0 0x200000;sf write 0x10000000 0 $filesize;
    sf erase 0x200000 0x200000;sf write 0x10010000 0x200000 $filesize;

Flash the ``boot.subimg`` to slots A and B.

::

    usb start; fatload usb 0  0x10000000 boot.subimg
    sf probe;
    sf erase 0x3f0000 0xE00000;sf write 0x10000000 0x3f0000 $filesize;
    sf erase 0x11f0000 0xE00000;sf write 0x10000000 0x11f0000 $filesize; //For 32MB SPI NOR only

Flashing Image from TFTP Server on SL16x0
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Flash the ``spi_suboot.bin`` to slots A and B.

::

    net_init; dhcp; setenv serverip 10.10.10.10
    tftpboot 0x10000000 spi_suboot.bin
    spinit;
    erase f0000000 f01fffff; cp.b 0x10000000 0xf0000000 $filesize;
    erase f0200000 f03fffff; cp.b 0x10000000 0xf0200000 $filesize;

Flash the ``boot.subimg`` to slots A and B.

::

    net_init; dhcp; setenv serverip 10.70.XX.XX
    tftpboot 0x10000000 boot.subimg
    spinit;
    erase f0400000 f11fffff; cp.b 0x10000000 f0400000 $filesize;
    erase f1200000 f1ffffff; cp.b 0x10000000 f1200000 $filesize; //For 32MB SPI NOR only

Flashing Image from TFTP Server on SL2610
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Flash the ``spi_suboot.bin`` to slots A and B.

::

    net_init; dhcp; setenv serverip 10.10.10.10
    tftpboot 0x10000000 spi_suboot.bin
    sf probe;
    sf erase 0 0x200000;sf write 0x10000000 0 $filesize;
    sf erase 0x200000 0x200000;sf write 0x10010000 0x200000 $filesize;

Flash the ``boot.subimg`` to slots A and B.

::

    net_init; dhcp; setenv serverip 10.70.XX.XX
    tftpboot 0x10000000 boot.subimg
    sf probe;
    sf erase 0x3f0000 0xE00000;sf write 0x10000000 0x3f0000 $filesize;
    sf erase 0x11f0000 0xE00000;sf write 0x10000000 0x11f0000 $filesize; //For 32MB SPI NOR only

Building Custom SPI Images
==========================

Astra supports building custom SPI boot images. Common examples are for devices which user different memory
layouts or DDR types.

General instructions on building images and setting up the environment can be found in the :doc:`../yocto`.

To build USB U-Boot images use the ``*spi`` machine type and the ``astra-tiny`` image.

::

    pokyuser@xyz:/path/to/workspace/sdk $ MACHINE=sl2619spi . meta-synaptics/setup/setup-environment

Next modify the packages in order to apply changes.

::

    pokyuser@xyz:/path/to/workspace/sdk $ devtool modify synasdk-config-native

Build the updated USB boot images.

::

    pokyuser@xyz:/path/to/workspace/sdk $ devtool build-image astra-tiny

Building for Different DDR Types
--------------------------------

Instructions for changing the DDR type are the same as those listed in :doc:`memory_layout_customization`. Just use the
``*spi`` machine type when setting up the environment.