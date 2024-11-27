=====================================
Updating the ISP Sensor Configuration
=====================================

SL1680 supports multiple camera sensors. By default, SL1680 is configured to use the IMX258 module. But, the software can be configured to use any of the
supported sensor modules. 

Supported Camera Modules
------------------------

=======  =======================================================================================   ==========  ======================================= ================
Sensor   Module                                                                                    Interface   Adapter Board                           DTS Change
=======  =======================================================================================   ==========  ======================================= ================
IMX258   Synaptics IMX258 Camera Module                                                            MIPI-CSI 0  Synaptics SL1680 MIPI CSI Adaptor Board No
IMX415   Synaptics IMX415 Camera Module                                                            MIPI-CSI 0  Synaptics SL1680 MIPI CSI Adaptor Board No
OV5647   `Arducam 5MP OV5647 Camera Module
         <https://www.arducam.com/product/arducam-ov5647-standard-raspberry-pi-camera-b0033/>`__   MIPI-CSI 0  None                                    Yes
=======  =======================================================================================   ==========  ======================================= ================

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

Enabling the OV5647 Sensor
--------------------------

Astra Machina SL1680 supports using the OV5647 sensor on either the CSI0 (22-pin) or the CSI1 (15-pin) connector. Both configurations
require modifying the kernel's device tree and the ISP initialization script. The configuration
depends on which CSI connector is being used.

.. note::

    Release v1.4 adds support for using an OV5647 sensor on CSI1. Previous versions only support using OV5647 on CSI0.

.. note::

    Using CSI0 and CSI1 simultaneously is currently not support. But, will be supported in a future release.

Using the OV5647 camera module also requires an update to the kernel's device tree. This requires modifying the
``linux-syna`` package using ``devtool``::

    devtool modify linux-syna

Below are instruction on how to :ref:`ov5647_csi0` or :ref:`ov5647_csi1`.

.. _ov5647_csi0:

Configure the OV5647 Sensor for CSI0
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Modify the ``dolphin-rdk.dts`` file located in ``build-sl1680/workspace/sources/linux-syna/arch/arm64/boot/dts/synaptics``.

::

    diff --git a/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts b/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts
    index ee1fbb6..3bcdea7 100644
    --- a/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts
    +++ b/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts
    @@ -158,14 +158,6 @@
                                    #gpio-cells = <2>;
                            };

    -                       expander2: gpio@49 {
    -                               compatible = "ti,pca9536";
    -                               reg = <0x49>;
    -                               gpio-controller;
    -                               #gpio-cells = <2>;
    -                               reset-gpios = <&expander1 4 GPIO_ACTIVE_LOW>;
    -                       };
    -
                            rtc0: rtc@68 {
                                    compatible = "dallas,ds1339";
                                    wakeup-source;
    @@ -540,8 +532,8 @@

    &isp_vsi {
            status = "okay";
    -       enable-gpio = <&expander2 1 GPIO_ACTIVE_HIGH>;
    -       reset-gpio = <&expander2 0 GPIO_ACTIVE_HIGH>;
    +       enable-gpio = <&expander1 0 GPIO_ACTIVE_HIGH>;
    +       reset-gpio = <&expander1 4 GPIO_ACTIVE_HIGH>;
    };

    &isp_vsi_video {

Then update the ``isp_media_server.sh`` script to load the configuration for the OV5647 sensor. Apply the following change
to ``meta-synaptics/recipes-devtools/synasdk/files/isp_media_server.sh``.

::

    diff --git a/recipes-devtools/synasdk/files/isp_media_server.sh b/recipes-devtools/synasdk/files/isp_media_server.sh
    index 20cbc24..0ba2e04 100644
    --- a/recipes-devtools/synasdk/files/isp_media_server.sh
    +++ b/recipes-devtools/synasdk/files/isp_media_server.sh
    @@ -26,7 +26,7 @@ set -e

    case $1 in
        start)
    -        echo "sensor=imx258 xml=/usr/share/IMX258.xml manu_json=/usr/share/ISP_Manual_IMX258.json \
    +        echo "sensor=ov5647 xml=/usr/share/OV5647_480p.xml manu_json=/usr/share/ISP_Manual_IMX258.json \
            auto_json=/usr/share/ISP_Auto.json i2c_bus_id=3 mipi_id=0 mode=0" > /proc/vsi/isp_subdev0
            echo -n "Starting $DESC: "
            start-stop-daemon --start $SSD_OPTIONS  > $LOGFILE &


.. _ov5647_csi1:

Configure the OV5647 Sensor for CSI1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Modify the ``dolphin-rdk.dts`` file located in ``build-sl1680/workspace/sources/linux-syna/arch/arm64/boot/dts/synaptics``.

``dolphin-rdk.dts``::

    diff --git a/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts b/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts
    index c4b7b24..06aa276 100644
    --- a/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts
    +++ b/arch/arm64/boot/dts/synaptics/dolphin-rdk.dts
    @@ -158,14 +158,6 @@
                                    #gpio-cells = <2>;
                            };

    -                       expander2: gpio@49 {
    -                               compatible = "ti,pca9536";
    -                               reg = <0x49>;
    -                               gpio-controller;
    -                               #gpio-cells = <2>;
    -                               reset-gpios = <&expander1 4 GPIO_ACTIVE_LOW>;
    -                       };
    -
                            rtc0: rtc@68 {
                                    compatible = "dallas,ds1339";
                                    wakeup-source;
    @@ -552,8 +544,8 @@

    &isp_vsi {
            status = "okay";
    -       enable-gpio = <&expander2 1 GPIO_ACTIVE_HIGH>;
    -       reset-gpio = <&expander2 0 GPIO_ACTIVE_HIGH>;
    +       enable-gpio = <&expander1 7 GPIO_ACTIVE_HIGH>;
    +       reset-gpio = <&expander1 6 GPIO_ACTIVE_HIGH>;
    };

``dolphin.dtsi``::

    diff --git a/arch/arm64/boot/dts/synaptics/dolphin.dtsi b/arch/arm64/boot/dts/synaptics/dolphin.dtsi
    index 8b8c5b3..2c51a11 100644
    --- a/arch/arm64/boot/dts/synaptics/dolphin.dtsi
    +++ b/arch/arm64/boot/dts/synaptics/dolphin.dtsi
    @@ -1165,32 +1165,32 @@
                            ports {
                                    #address-cells = <1>;
                                    #size-cells = <0>;
    -                               port@1 {
    -                                       reg = <1>;
    +                               port@5 {
    +                                       reg = <5>;
                                            #address-cells = <1>;
                                            #size-cells = <0>;
    -                                       isp_vsi_subdev_ep0: endpoint@1 {
    -                                               reg = <1>;
    +                                       isp_vsi_subdev_ep0: endpoint@5 {
    +                                               reg = <5>;
                                                    remote-endpoint = <&isp_vsi_video_ep0>;
                                            };
                                    };

    -                               port@2 {
    -                                       reg = <2>;
    +                               port@6 {
    +                                       reg = <6>;
                                            #address-cells = <1>;
                                            #size-cells = <0>;
    -                                       isp_vsi_subdev_ep1: endpoint@2 {
    -                                               reg = <2>;
    +                                       isp_vsi_subdev_ep1: endpoint@6 {
    +                                               reg = <6>;
                                                    remote-endpoint = <&isp_vsi_video_ep1>;
                                            };
                                    };

    -                               port@3 {
    -                                       reg = <3>;
    +                               port@7 {
    +                                       reg = <7>;
                                            #address-cells = <1>;
                                            #size-cells = <0>;
    -                                       isp_vsi_subdev_ep2: endpoint@3 {
    -                                               reg = <3>;
    +                                       isp_vsi_subdev_ep2: endpoint@7 {
    +                                               reg = <7>;
                                                    remote-endpoint = <&isp_vsi_video_ep2>;
                                            };
                                    };

Then update the ``isp_media_server.sh`` script to load the configuration for the OV5647 sensor. Apply the following change
to ``meta-synaptics/recipes-devtools/synasdk/files/isp_media_server.sh``.

::

    diff --git a/recipes-devtools/synasdk/files/isp_media_server.sh b/recipes-devtools/synasdk/files/isp_media_server.sh
    index 20cbc24..b521d47 100644
    --- a/recipes-devtools/synasdk/files/isp_media_server.sh
    +++ b/recipes-devtools/synasdk/files/isp_media_server.sh
    @@ -26,8 +26,8 @@ set -e

    case $1 in
        start)
    -        echo "sensor=imx258 xml=/usr/share/IMX258.xml manu_json=/usr/share/ISP_Manual_IMX258.json \
    -        auto_json=/usr/share/ISP_Auto.json i2c_bus_id=3 mipi_id=0 mode=0" > /proc/vsi/isp_subdev0
    +        echo "1 sensor=ov5647 xml=/usr/share/OV5647_480p.xml manu_json=/usr/share/ISP_Manual_IMX258.json \
    +        auto_json=/usr/share/ISP_Auto.json i2c_bus_id=0 mipi_id=1 mode=0" > /proc/vsi/isp_subdev0
            echo -n "Starting $DESC: "
            start-stop-daemon --start $SSD_OPTIONS  > $LOGFILE &
            echo "${DAEMON##*/}."

Building the Updated Image
--------------------------

Build the image with the updated device tree entries::

   devtool build linux-syna
   devtool build-image astra-media