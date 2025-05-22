=====================================
Updating the ISP Sensor Configuration
=====================================

SL1680 supports multiple camera sensors. By default, SL1680 is configured to use the OV5647 module with port CSI0. But, the software can be configured to use any of the
supported sensor modules. Some configurations require setting a device tree overlay to function correctly.

.. note::

    Starting with release v1.5, the default sensor is now the OV5647 module.

Supported Camera Modules
------------------------

=======  =======================================================================================   ============  ======================================= ======================================
Sensor   Module                                                                                    Interface     Adapter Board                           Device Tree Overlay
=======  =======================================================================================   ============  ======================================= ======================================
IMX258   Synaptics IMX258 Camera Module                                                            MIPI-CSI 0    Synaptics SL1680 MIPI CSI Adaptor Board dolphin-csi0-with-expander.dtbo
IMX415   Synaptics IMX415 Camera Module                                                            MIPI-CSI 0    Synaptics SL1680 MIPI CSI Adaptor Board dolphin-csi0-with-expander.dtbo
OV5647   `Arducam 5MP OV5647 Camera Module
         <https://www.arducam.com/product/arducam-ov5647-standard-raspberry-pi-camera-b0033/>`__   MIPI-CSI 0    None                                    N/A

                                                                                                   MIPI-CSI 1    None                                    dolphin-csi1-without-expander.dtbo

                                                                                                   Dual CSI0/1   None                                    dolphin-bothcsi-without-expander.dtbo

=======  =======================================================================================   ============  ======================================= ======================================


 .. _changing_sensor_module:

Changing the Camera Sensor Module
---------------------------------

The file ``/proc/vsi/isp_subdev0`` is used to display the sensor configuration properties and to update the sensor configuration.

Current Sensor Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The current sensor configuration can be viewed by read from the ``/proc/vsi/isp_subdev0`` file.

.. figure:: media/sl1680-isp-sensor-configuration.png

    Reading the current sensor configuration

Configuring a New Module
^^^^^^^^^^^^^^^^^^^^^^^^

To change the sensor configuration, update the ``/usr/sbin/isp_media_server.sh`` script. Change the line which writes
the sensor config to ``/proc/vsi/isp_subdev0``. Update the sensor name, xml, and json files for the new sensor.

.. figure:: media/isp_media_server_script.png

Each camera sensor module contains one or more XML configuration files located in ``/usr/share``.

.. figure:: media/sl1680-isp-sensor-config-files.png

    List of sensor config files

Then restart the isp_media_server service to apply the update.

::

    systemctl restart isp_media_server

.. note::

    To apply these changes to an image, modify the ``meta-synaptics/recipes-devtools/synasdk/files/isp_media_server.sh``
    script as described below.

Updating Device Tree Overlay
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See :ref:`devicetree_overlays` for details on how to enable the devicetree overlays.

Using the OV5647 Sensor
-----------------------

Astra Machina SL1680 supports using the OV5647 sensor on either the CSI0 (22-pin), or the CSI1 (15-pin) connector, or both simultaneously.
Connecting a single OV5647 sensor to CSI0 is the default configuration. Connecting a single OV5647 sensor to CSI1 requires enabling the
``dolphin-csi1-without-expander.dtbo`` overlay. Using two OV5647 sensors simultaneously requires enabling the ``dolphin-bothcsi-without-expander.dtbo``
overlay.

.. note::

    Release v1.4 adds support for using an OV5647 sensor on CSI1. Previous versions only support using OV5647 on CSI0.

.. note::

    Release v1.5 adds support for using CSI0 and CSI1 simultaneously with two OV5647 sensors.

Enabling the IMX258 and IMX415 Sensors
--------------------------------------

Astra Machina SL1680 supports the IMX258 and IMX415 sensors connected to CSI0. These sensors use a GPIO expander which requires the ``dolphin-csi0-with-expander.dtbo``
overlay.

.. note::

    Using the IMX258 and IMX415 on CSI1 is not supported on Synaptics Astra Machina boards since CSI1
    is not compatible with the GPIO expander.

In addition to enabling the ``dolphin-csi0-with-expander.dtbo``, the sensor configuration needs to be updated to use the new sensor. Apply the following changes
to ``isp_media_server.sh`` as describe in the previous section: :ref:`changing_sensor_module`.

Configuration for IMX258::

    diff --git a/recipes-devtools/synasdk/files/isp_media_server.sh b/recipes-devtools/synasdk/files/isp_media_server.sh
    index 4f603fb..c5cd9b1 100644
    --- a/recipes-devtools/synasdk/files/isp_media_server.sh
    +++ b/recipes-devtools/synasdk/files/isp_media_server.sh
    @@ -26,7 +26,7 @@ set -e

    case $1 in
        start)
    -        echo "sensor=ov5647 xml=/usr/share/OV5647_480p.xml manu_json=/usr/share/ISP_Manual_IMX258.json \
    +        echo "sensor=imx258 xml=/usr/share/IMX258.xml manu_json=/usr/share/ISP_Manual_IMX258.json \
            auto_json=/usr/share/ISP_Auto.json i2c_bus_id=3 mipi_id=0 mode=0" > /proc/vsi/isp_subdev0
            echo "1 sensor=ov5647 1 xml=/usr/share/OV5647_480p.xml 1 manu_json=/usr/share/ISP_Manual_IMX258.json \
            1 auto_json=/usr/share/ISP_Auto.json 1 i2c_bus_id=0 1 mipi_id=1 1 mode=0" > /proc/vsi/isp_subdev0

Configuration for IMX415::

    diff --git a/recipes-devtools/synasdk/files/isp_media_server.sh b/recipes-devtools/synasdk/files/isp_media_server.sh
    index 4f603fb..c5cd9b1 100644
    --- a/recipes-devtools/synasdk/files/isp_media_server.sh
    +++ b/recipes-devtools/synasdk/files/isp_media_server.sh
    @@ -26,7 +26,7 @@ set -e

    case $1 in
        start)
    -        echo "sensor=ov5647 xml=/usr/share/OV5647_480p.xml manu_json=/usr/share/ISP_Manual_IMX258.json \
    +        echo "sensor=imx415 xml=/usr/share/IMX415.xml manu_json=/usr/share/ISP_Manual_IMX415.json \
            auto_json=/usr/share/ISP_Auto.json i2c_bus_id=3 mipi_id=0 mode=0" > /proc/vsi/isp_subdev0
            echo "1 sensor=ov5647 1 xml=/usr/share/OV5647_480p.xml 1 manu_json=/usr/share/ISP_Manual_IMX258.json \
            1 auto_json=/usr/share/ISP_Auto.json 1 i2c_bus_id=0 1 mipi_id=1 1 mode=0" > /proc/vsi/isp_subdev0

