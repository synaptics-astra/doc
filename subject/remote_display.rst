=================================
Remote Display for Astra Series
=================================

Astra supports remote display access via RDP. This allows users to connect
to the device's graphical session over the network.

Supported Platforms
===================

Remote display has been validated on:

- SL16X0
- SL261X

Enable Remote Display
=====================

Edit ``/etc/default/weston`` and set the RDP backend:

.. code-block:: bash

    BACKEND=rdp-backend.so

.. note::

    The ``BACKEND=rdp-backend.so`` setting replaces any existing ``BACKEND``
    line in ``/etc/default/weston``.

Then restart Weston:

.. code-block:: bash

    systemctl restart weston.service

Connect to the Device
=====================

After Weston restarts, connect to the remote session using the device IP address.

Windows
-------

Use **Remote Desktop Connection** (``mstsc``) and enter the device IP.

Linux
-----

Install **Remmina** and connect using the device IP.

macOS
-----

Install **Windows App** from the Apple App Store and use it to connect to the remote display.
