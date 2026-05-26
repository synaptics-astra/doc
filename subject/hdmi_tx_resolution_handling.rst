================================================
HDMI-TX Resolution Handling in Kernel DRM Driver
================================================

Introduction
============

The scope of this document is to provide information and instructions for
HDMI-TX resolution handling in the ``syna_drm`` kernel DRM driver, including
runtime force mode testing and persistent configuration.

HDMI-TX Resolution Control Modes
================================

The ``syna_drm`` driver supports two main options to control output resolution:

1. Fixed mode disabled in DTS
2. Fixed mode enabled in DTS

Fixed mode disabled in DTS
^^^^^^^^^^^^^^^^^^^^^^^^^^

If fixed mode is disabled, full control is delegated to the display
managers/compositors in application or middleware layers.

Fixed mode enabled in DTS
^^^^^^^^^^^^^^^^^^^^^^^^^

If fixed mode is enabled, the kernel driver handles resolution selection,
independent of display managers/compositors.

When fixed mode is enabled, two functional paths are used:

1. Default case

   * Resolution is selected from sink EDID capability.
   * Typical behavior:

     * 2K TV: ``2K60``
     * 4K TV: ``4K30``

2. Force mode

   * Resolution is explicitly forced through the module parameter.
   * Supported force values are listed in the next section.

HDMI Force Mode Testing Guide
=============================

Feature overview
^^^^^^^^^^^^^^^^

The HDMI driver applies resolution selection in this priority order:

1. Force mode: user sets ``hdmi_force_mode`` through module parameter.
2. Auto-detect: driver chooses from sink (TV) EDID capabilities.

Supported Force Mode Values
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following strings are supported for ``hdmi_force_mode``:

* ``4K30``
* ``2K60``
* ``2K50``
* ``720p``
* ``576p``
* ``480p``

Runtime Testing (Valid for Current Boot)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These steps apply mode changes on next hotplug event and do not persist across
reboot.

Step 1: Set the mode
--------------------

Use the module parameter interface:

For 4K at 30 Hz::

   echo "4K30" > /sys/module/syna_drm/parameters/hdmi_force_mode

For 1080p at 60 Hz::

   echo "2K60" > /sys/module/syna_drm/parameters/hdmi_force_mode

For legacy 480p::

   echo "480p" > /sys/module/syna_drm/parameters/hdmi_force_mode

Step 2: Trigger hotplug
-----------------------

The new mode is applied on next HDMI connection event.

* Physically unplug and replug the HDMI cable.

Step 3: Verification
--------------------

Top-level check:

* Verify the TV OSD/pop-up shows expected resolution.

Kernel log check::

   dmesg | grep "syna_drm"

Success log examples:

* ``Processing force mode: '4K30'``
* ``HDMI_HPD detected, setting res to resId:16``

Fallback log examples:

* ``Force 4K30 requested but Sink ... doesn't support it ... Fallback.``
* ``Fallback: setting res to resId:24``

Step 4: Clear force mode
------------------------

Clear the force mode setting::

   echo > /sys/module/syna_drm/parameters/hdmi_force_mode

Persistent Configuration (Reboot Safe)
======================================

To ensure force mode remains active after reboot, configure the module parameter
using ``modprobe.d``.

Update ``syna_drm.conf`` on target device:

1. Open the configuration file::

      vi /usr/lib/modprobe.d/syna_drm.conf

2. Add or update the option. Example to keep ``2K60``::

      options syna_drm hdmi_force_mode=2K60

3. Reboot the board.
4. Verify that the configured resolution is maintained.

Sticky Mode Behavior Check
==========================

The driver remembers the last successfully applied mode from user request or
force mode logic.

Expected behavior when switching TVs (hotplug):

* Keep the same resolution if the new TV supports it.
* If unsupported, fallback to the next best mode supported by the TV.

