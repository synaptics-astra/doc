===================================
Haier Panel Configuration Guide
===================================

Introduction
============

This document provides steps on how to enable the Haier reference panel on SL16XX platforms.

.. note::

    The Haier reference panel was the default output for SL1620 up until v1.3. Follow these instructions
    to switch back to MIPI output with the Haier panel.

Connection
==========

1. Connect the USB cable on the Haier panel's adapter board to the USB ports on the SL16XX I/O board.
    This provides power to the panel.

.. figure:: media/usb-ports.png

    SL16XX I/O board with USB ports highlighted

2. Connect the 22 pin DSI cable to the MIPI DSI connector on the SL16XX I/O board.

.. figure:: media/mipi-dsi-port.png

    SL16XX I/O board with MIPI DSI port highlighted

.. figure:: media/haier-mipi-adapter-board.jpg

    Picture of the Haier MIPI Panel adapter board connected to the MIPI DSI port on the SL16XX I/O board.

Software Configuration
======================

The Haier panel can be enabled by setting the ``dtbo`` variable, in U-Boot, to the correct device tree overlay.

+-----------------+--------------------------------+-----------------------------------+----------------------------------+
|                 | SL1620                         | SL1640                            | SL1680                           |
+-----------------+--------------------------------+-----------------------------------+----------------------------------+
| DTS Overlay     | myna2-haier-panel-overlay.dtbo | platypus-haier-panel-overlay.dtbo | dolphin-haier-panel-overlay.dtbo |
+-----------------+--------------------------------+-----------------------------------+----------------------------------+

Setting the device tree overlay requires booting into U-Boot and setting
the ``dtbo`` variable to the required device tree overlay. See :ref:`uboot_prompt` for instructions on getting to the
U-Boot prompt.

Once at the U-Boot prompt run the following commands to enable the Device Tree Overlay.

Set the ``dtbo`` variables::

    => setenv dtbo myna2-haier-panel-overlay.dtbo

Save the environment to the eMMC so that the new variable will persist across reboots.

::

    => saveenv
    Saving Environment to MMC... Writing to redundant MMC(0)... OK

Optionally, confirm that the variable was correctly set.

::

    => printenv
    altbootcmd=if test ${boot_slot}  = 1; then bootslot set b; bootcount reset;bootcount reset; run bootcmd; else bootslot set a; bootcount reset; bootcount reset; run bootcmd;  fi
    autoload=n
    baudrate=115200
    bootcmd=bootmmc
    bootcount=1
    bootdelay=0
    bootlimit=3
    dtbo=myna2-haier-panel-overlay.dtbo
    fdtcontroladdr=2172e190
    preboot=show_logo;
    upgrade_available=0
    ver=U-Boot 2019.10 (Nov 21 2024 - 14:01:42 +0000)
    Environment size: 407/65531 bytesboo

Finally, boot with the new overlay applied.

::

    => boot