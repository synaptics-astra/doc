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

See :ref:`devicetree_overlays` for details on how to enable the devicetree overlays.