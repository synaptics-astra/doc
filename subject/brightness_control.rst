==========================================================
Controlling Display Brightness on the Synaptics DRM Driver
==========================================================

``modetest`` application to control display brightness on DRM CRTCs
using the Synaptics display driver.

Features
========

* Controls overall CRTC brightness from userspace
* Controls per-channel brightness (``R brightness``, ``G brightness``,
  ``B brightness``)
* Works directly with DRM CRTC properties
* Supports mode setup and brightness update in a single command
* Supports dynamic brightness update after display initialization

Brightness Properties
=====================

The Synaptics DRM driver exposes the following brightness-related
properties on the CRTC:

* ``brightness``
* ``R brightness``
* ``G brightness``
* ``B brightness``

Brightness Range
================

Each brightness property accepts a signed value in the range
**-128 to 127**:

+--------+---------------------------------+
| Value  | Meaning                         |
+========+=================================+
| 127    | Maximum brightness              |
+--------+---------------------------------+
| 0      | Default / neutral level         |
+--------+---------------------------------+
| -128   | Minimum brightness / full dark  |
+--------+---------------------------------+

.. note::

   Brightness change is applicable only for **SL1620** and **SL26XX**
   series platforms.

Display Configuration Used
==========================

The examples on this page assume the following display setup. Replace
the connector and CRTC IDs with the values reported by ``modetest`` on
your board.

+-----------+----------------+
| Parameter | Value          |
+===========+================+
| Driver    | synaptics      |
+-----------+----------------+
| Connector | 33             |
+-----------+----------------+
| CRTC      | 36             |
+-----------+----------------+
| Mode      | 800x480@59.72  |
+-----------+----------------+

Example Commands
================

Default brightness values can be viewed using the ``modetest`` command::

    modetest -M synaptics -p

Sample output (CRTC section)::

    CRTCs:
    id      fb      pos     size
    36      54      (0,0)   (800x480)
      #0 800x480 59.72 800 1010 1012 1058 480 502 504 527 33300 flags: ; type: preferred, driver
      props:
            24 VRR_ENABLED:
                    flags: range
                    values: 0 1
                    value: 0
            28 GAMMA_LUT:
                    flags: blob
                    blobs:

                    value:
            29 GAMMA_LUT_SIZE:
                    flags: immutable range
                    values: 0 4294967295
                    value: 256
            37 R brightness:
                    flags: signed range
                    values: -128 127
                    value: -128
            38 G brightness:
                    flags: signed range
                    values: -128 127
                    value: -128
            39 B brightness:
                    flags: signed range
                    values: -128 127
                    value: 127
            40 brightness:
                    flags: signed range
                    values: -128 127
                    value: -128

Set full brightness::

    modetest -M synaptics -s 33@36:#0 -w 36:"brightness":127

Set full dark::

    modetest -M synaptics -s 33@36:#0 -w 36:"brightness":-128

Set the blue channel to maximum::

    modetest -M synaptics -s 33@36:#0 -w 36:"B brightness":127

Alternate Method
================

Brightness can also be changed **after mode initialization**.

Open two terminals on the board.

Terminal 1 -- Set Display Mode::

    modetest -M synaptics -s 33@36:#0 -d

Terminal 2 -- Update Brightness Dynamically::

    modetest -M synaptics -w 36:"B brightness":0
    modetest -M synaptics -w 36:"B brightness":127

Negative Cases
==============

Values outside the allowed range are rejected by the kernel::

    modetest -M synaptics -w 36:"B brightness":128
    failed to set CRTC 36 property

    modetest -M synaptics -w 36:"B brightness":-129
    failed to set CRTC 36 property

Full ``modetest`` Output (Reference)
====================================

The following is the complete output of ``modetest -M synaptics`` on a
dual-display SL1620 setup, showing both CRTCs (DPI-1 and DPI-2) and
their associated brightness properties::

    root@sl1620:~# modetest -M synaptics
    Encoders:
    id      crtc    type    possible crtcs  possible clones
    32      36      DPI     0x00000001      0x00000001
    41      45      DSI     0x00000002      0x00000002

    Connectors:
    id      encoder status          name            size (mm)       modes   encoders
    33      32      connected       DPI-1           0x0             1       32
      modes:
            index name refresh (Hz) hdisp hss hse htot vdisp vss vse vtot
      #0 800x480 59.72 800 1010 1012 1058 480 502 504 527 33300 flags: ; type: preferred, driver
      props:
            1 EDID:
                    flags: immutable blob
                    blobs:

                    value:
            2 DPMS:
                    flags: enum
                    enums: On=0 Standby=1 Suspend=2 Off=3
                    value: 0
            5 link-status:
                    flags: enum
                    enums: Good=0 Bad=1
                    value: 0
            6 non-desktop:
                    flags: immutable range
                    values: 0 1
                    value: 0
            4 TILE:
                    flags: immutable blob
                    blobs:

                    value:
    42      41      connected       DPI-2           0x0             1       41
      modes:
            index name refresh (Hz) hdisp hss hse htot vdisp vss vse vtot
      #0 1920x1080 60.00 1920 2008 2052 2200 1080 1084 1089 1125 148500 flags: ; type: preferred, driver
      props:
            1 EDID:
                    flags: immutable blob
                    blobs:

                    value:
            2 DPMS:
                    flags: enum
                    enums: On=0 Standby=1 Suspend=2 Off=3
                    value: 0
            5 link-status:
                    flags: enum
                    enums: Good=0 Bad=1
                    value: 0
            6 non-desktop:
                    flags: immutable range
                    values: 0 1
                    value: 0
            4 TILE:
                    flags: immutable blob
                    blobs:

                    value:

    CRTCs:
    id      fb      pos     size
    36      54      (0,0)   (800x480)
      #0 800x480 59.72 800 1010 1012 1058 480 502 504 527 33300 flags: ; type: preferred, driver
      props:
            24 VRR_ENABLED:
                    flags: range
                    values: 0 1
                    value: 0
            28 GAMMA_LUT:
                    flags: blob
                    blobs:

                    value:
            29 GAMMA_LUT_SIZE:
                    flags: immutable range
                    values: 0 4294967295
                    value: 256
            37 R brightness:
                    flags: signed range
                    values: -128 127
                    value: -128
            38 G brightness:
                    flags: signed range
                    values: -128 127
                    value: -128
            39 B brightness:
                    flags: signed range
                    values: -128 127
                    value: 127
            40 brightness:
                    flags: signed range
                    values: -128 127
                    value: -128
    45      54      (0,0)   (1920x1080)
      #0 1920x1080 60.00 1920 2008 2052 2200 1080 1084 1089 1125 148500 flags: ; type: preferred, driver
      props:
            24 VRR_ENABLED:
                    flags: range
                    values: 0 1
                    value: 0
            28 GAMMA_LUT:
                    flags: blob
                    blobs:

                    value:
            29 GAMMA_LUT_SIZE:
                    flags: immutable range
                    values: 0 4294967295
                    value: 256
            46 R brightness:
                    flags: signed range
                    values: -128 127
                    value: 0
            47 G brightness:
                    flags: signed range
                    values: -128 127
                    value: 0
            48 B brightness:
                    flags: signed range
                    values: -128 127
                    value: 0
            49 brightness:
                    flags: signed range
                    values: -128 127
                    value: 0

    Planes:
    id      crtc    fb      CRTC x,y        x,y     gamma size      possible crtcs
    34      36      54      0,0             0,0     0               0x00000001
      formats: XR24 AR24 XB24 AB24 RG16 BG16 BG24 RG24
      props:
            8 type:
                    flags: immutable enum
                    enums: Overlay=0 Primary=1 Cursor=2
                    value: 1
            30 IN_FORMATS:
                    flags: immutable blob
                    blobs:

                    value:
                            01000000000000000800000018000000
                            01000000380000005852323441523234
                            58423234414232345247313642473136
                            4247323452473234ff00000000000000
                            00000000000000000000000000000000
                    in_formats blob decoded:
                             XR24:  LINEAR(0x0)
                             AR24:  LINEAR(0x0)
                             XB24:  LINEAR(0x0)
                             AB24:  LINEAR(0x0)
                             RG16:  LINEAR(0x0)
                             BG16:  LINEAR(0x0)
                             BG24:  LINEAR(0x0)
                             RG24:  LINEAR(0x0)
    43      45      54      0,0             0,0     0               0x00000002
      formats: XR24 AR24 XB24 AB24 RG16 BG16 BG24 RG24
      props:
            8 type:
                    flags: immutable enum
                    enums: Overlay=0 Primary=1 Cursor=2
                    value: 1
            30 IN_FORMATS:
                    flags: immutable blob
                    blobs:

                    value:
                            01000000000000000800000018000000
                            01000000380000005852323441523234
                            58423234414232345247313642473136
                            4247323452473234ff00000000000000
                            00000000000000000000000000000000
                    in_formats blob decoded:
                             XR24:  LINEAR(0x0)
                             AR24:  LINEAR(0x0)
                             XB24:  LINEAR(0x0)
                             AB24:  LINEAR(0x0)
                             RG16:  LINEAR(0x0)
                             BG16:  LINEAR(0x0)
                             BG24:  LINEAR(0x0)
                             RG24:  LINEAR(0x0)

    Frame buffers:
    id      size    pitch

Observed Behavior
=================

+-----------------------------------+----------------------------------------------------------+
| Command                           | Result                                                   |
+===================================+==========================================================+
| ``brightness:127``                | Full bright                                              |
+-----------------------------------+----------------------------------------------------------+
| ``brightness:-128``               | Full dark                                                |
+-----------------------------------+----------------------------------------------------------+
| ``B brightness:127``              | Fully bright blue                                        |
+-----------------------------------+----------------------------------------------------------+
| Property write (Terminal 2)       | Brightness updates dynamically while display is enabled  |
+-----------------------------------+----------------------------------------------------------+

Example Output
==============

The following property writes were exercised on the reference setup
above:

.. figure:: media/b_b127.jfif

         ``-w 36:"B brightness":127``

.. figure:: media/b0.jfif

        ``-w 36:"brightness":0``

.. figure:: media/b127.jfif

        ``-w 36:"brightness":127``

.. figure:: media/b-128.jfif

        ``-w 36:"brightness":-128``
