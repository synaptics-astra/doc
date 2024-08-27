================================
SYNA DRM / KMS Driver User Guide
================================

Introduction
============

Overview
--------

   The scope of the document is to provide detailed steps to configure
   and unit test drm/kms driver for SL16xx display interfaces.

   This document emphasizes on MIPI-DSI related configuration like
   timing, initialization command, etc.

Acronyms
--------

   MIPI - Mobile Industry Processor Interface

   LCD – Liquid Crystal Display

   TFT – Thin Film Transistor

   DRM – Direct Rendering Manager

   KMS – Kernel Mode Setting

Astra Machina Display Capabilities
==================================

   syna drm/kms driver is supported for the SL16xx Astra Machina
   platforms.

Display capability of the supported SoC’s.
-------------------------------------------

-  SL1640: Supports Single Display (Either HDMI or MIPI-DSI)

-  SL1680: Supports Dual Display (HDMI and MIPI-DSI)

-  SL1620: Supports Dual Display (TFT and MIPI-DSI)

SYNA DRM/KMS Configuration
==========================

   Device driver configurations are handled through the *defconfig* and
   *dts* files.

Configuration based on defconfig
---------------------------------

Following device driver configuration available in *defconfig*:

1. DRM/KMS driver

2. Backlight

*defconfig* for each platform is given below:

1. SL1620: *myna2_defconfig*

2. SL1640: *platypus_defconfig*

3. SL1680: *dolphin_defconfig*

Configuration based on dts
---------------------------

Following device configuration are handled through *dts* files:

1. Generic Display configuration

2. MIPI-DSI Panel configuration

3. LCDC panel configuration

4. HDMI TX configuration

*dts* files of each platform given below:

-  SL1620: *myna2-rdk.dts*

-  SL1640: *platypus-rdk.dts*

-  SL1680: *dolphin-rdk.dts*

dts configuration template for SL16XX given below:
---------------------------------------------------

*dts* for SL1640 and SL1680
---------------------------

   *&drm {*

      *Generic Display configuration*

      *MIPI-DSI Panel configuration*

      *HDMI TX configuration*

   *}*

*dts* for SL1620
----------------

   *&drm {*

      *MIPI-DSI Panel configuration*

      *LCDC panel specific configuration*

   *}*

Generic Display Configuration
-----------------------------

   For SL1640 or SL1680, the default display type on bootup need be
   specified.

   Below are the parameters which need be configured for the display.

   -  **disp-mode:** Specifies the display mode. Whether it is single
      display/ dual display.

   -  **disp1-res-id:** Resolution Id corresponding to a timing
      information.

..

   More information on the timing and resolution id are available in
   below file.

   *<linux>/drivers/soc/berlin/modules/avio/vpp/ca/include/vpp_defines.h*

   -  **disp1-type:** Type of the Display1 whether it is HDMI or MIPI-DSI.

   -  **disp2-res-id:** Resolution Id corresponding to the timing
      information. In case of dual Display, display2 must be MIPI-DSI and
      resolution id is fixed to 102.

   -  **disp2-type:** Type of the Display2.

SL1640/SL1680 Single Display configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Default configuration for SL1640 and SL1680 given as below.

   -  SL1640 - Single Display mode – HDMI only.

   -  SL1680 - Dual Display mode – HDMI + MIPI-DSI

..

   Display mode can be changed in *dts*. Single Display mode is
   applicable for both SL1640 and SL1680.

   Below is an example for Single display mode.

   **Single Display: HDMI Display Mode**

   *&drm {*

      *disp-mode = <0>;*

      *disp1-res-id = <24>;*

      *disp1-type = <0>;*

   *};*

   **Single Display mode: MIPI-DSI Display Mode**

   *&drm {*

      *disp-mode = <1>;*

      *disp1-res-id = <102>;*

      *disp1-type = <3>;*

   *};*

SL1680 Dual Display configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   **Dual Display Mode (HDMI as primary + DSI as secondary)**

   *&drm {*

      *disp-mode = <2>;*

      *disp1-res-id = <24>;*

      *disp1-type = <0>;*

      *disp2-res-id = <102>;*

      *disp2-type = <3>;*

   *};*

   Note:

   -  For MIPI-DSI Display: RESID is fixed to **102** where it takes the
      custom timing provided in the *dts*.

   -  For HDMI display ID, depending on the capability of the SINK at
      bootup only 4K or 1080P are supported at present.

SL1620 Display configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Default display configuration for SL1620 is Dual – TFT + MIPI-DSI.

   *lcdc_panel* node and *dsi_panel* nodes in *dts* decide the number of
   displays. Display configuration will be carried on based on the
   parameters in section 4.5 and section 4.3 respectively.

HDMI configuration
------------------

   HDMI configuration options in *dts* are as below:

   **hdtx-core-config**: used to configure HDMI output, it includes
   bitfields to control below options.

   Default options: *hdtx-core-config = /bits/ 8 <1 0 1>*

   - *HPD handling*: to enable/disable handling of sink hotplug. If HPD handling is disabled, output format will be configured on bootup depending on sink capability and retained till next reboot.

   - *HDCP control*: to enable/disabled HDCP. Currently not handled.

   - *FixedModeset:* to let SYNA DRM/KMS driver handle the mode setting internally without exposing user interface. If set, it will configure output format without requiring the userspace application to configure output format, any attempt to override the configured format will be ignored.

   **hdtx-supported-formats**:
   used to list the formats exposed to user via kms mode query.

   Default selection: *hdtx-supported-formats = /bits/ 8 <12 9 10 13 22
   21 19 26 25 24 61 62 64>.*

   Refer below file for resolution indices in
   *<linux>/drivers/soc/berlin/modules/avio/vpp/ca/include/vpp_defines.h*

   If needed, this can be overridden using parameter
   “\ *hdmi_preferred_mode* “, by adding/modifying the same in
   */etc/modprobe.d/syna_drm.conf*.

   Example: To override preferred modes as 1080p:
   *hdmi_preferred_mode=1920x1080*

   Below is out of box default configuration,

   - syna drm/kms driver will internally configure HDMI output format.

   On connecting 4K supported sink, 4K30 RGB 8bit format will be
   selected.

   On 1080p TV, output will be configured as 1080p60 RGB 8bit.

   - Preferred mode of EDID is override to 1080p.

MIPI-DSI Display Configuration
------------------------------

MIPI-DSI panel configuration parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   1. *Lanes* - Number of Data lanes

   2. *Data_Lane_Polarity* - Polarity of the Data Lane

   3. *Clk_Lane_Polarity* - Polarity of the clock lane

   4. *virtual_chan* - virtual channel number

   5. *Vid_mode* - Video mode. Supported video mode are:

      -  0 - non-burst mode + sync pulse

      -  1 - non-burst mode + sync event

      -  2 - Burst mode

   6.  *non-Continuous_clk* - 0 for continuous and 1 for non-continuous clock configuration

   7.  *Byte_clk* - Byte clock rate. Calculated as Total Bandwidth / (Lanes \* 8)

   8.  *Recv_ack* - Receive acknowledgement.

   9.  *Color_format* - Color coding output format

      a. RGB888 - 5

   10.  *Loosely_18* - Loosely 18 packed

   11.  *Data_Polarity* – Data enable signal. Assertion indicates valid pixel. 0 – Positive & 1 - negative

   12.  *H_polarity* - Horizontal polarity active low/High

   13.  *V_Polarity* - Vertical polarity

   14.   *Eotp_rx* - EOTP Reception support enable/disable.

   15. *Eotp_tx* - EOTP Transmission enable/disable.

   16. *HTOTAL* – Total number of pixels in a line.

   17. *Chunks* - Number of Chunks in case of multiple chunk transmission otherwise ‘1’ for single.

   18. *Null_Pkt* - Size of the null packet.

   19. *dpi_lp_cmd* - Enable DPI low power command.

   20. *ACTIVE_WIDTH* - Active width of the Panel

   21. *ACTIVE_HEIGHT* - Active height of the panel

   22. *HFP* - Horizontal Front porch

   23. *HSYNCWIDTH* - Horizontal sync width

   24. *HBP* - Horizontal Back porch

   25. *VFP* - vertical Front porch

   26. *VSYNCWIDTH* - Vertical sync width

   27. *VBP* - Vertical Back porch

   28. *TYPE* - '0' for SD, '1' for Full HD '2' for UHD

   29. *SCAN* - '1' for Progressive, '0' for Interlaced

   30. *FRAME_RATE* - Frame rate, ENUMs mentioned as below.

      -  *FRAME_RATE_23P98* = 0

      -  *FRAME_RATE_24* = 1

      -  *FRAME_RATE_25* = 2

      -  *FRAME_RATE_29P97* = 3

      -  *FRAME_RATE_30* = 4

      -  *FRAME_RATE_47P96* = 5

      -  *FRAME_RATE_48* = 6

      -  *FRAME_RATE_50* = 7

      -  *FRAME_RATE_59P94* = 8

      -  *FRAME_RATE_60* = 9

      -  *FRAME_RATE_100* = 10

      -  *FRAME_RATE_119P88* = 11

      -  *FRAME_RATE_120* = 12

      -  *FRAME_RATE_89P91* = 13

      -  *FRAME_RATE_90* = 14

   31. *FLAG_3D* – Disabled always.

   32. 
      | *FREQ* - Pixel clock frequency for primary display in KHz. Pixel frequency is calculated as 
      | FREQ = HTOTAL \* VTOTAL \* FRAME_RATE 
      | For instance, for 1080P60Hz standard resolution, HTOTAL – 2200, VTOTAL – 1125 FREQ = (2200 \* 1125 \* 60)/1000

   33. 
      | *PTS_PER_4* - PTS for every four count Which is nothing but PTS/4. For instance:
      | Crystal frequency is 90kHz and frame rate is 60fps, then
      | PTS_PER_4 = (4*90*1000)/60 = 6000

   34. *PIXEL_CLOCK* - Pixel clock frequency for Secondary display in KHz. Make it same as FREQ.

   35. *mipirst-gpio* - Reset Gpio for the MIPI.

   36. *power-supply* - External power supply control.

   37. *backlight* - External backlight control. 

   38. *COMMAND* = Command for initialization in Hex

      *Format - <CMD> <Payloadlength-n> <BYTE1> <...> <BYTEn>*

      -  Long write Ex: *39 04* *FF 98 81 03*

      *CMD => 0x39*

      *Length => 0x04*

      *PayLoad => FF 98 81 03*

      -  Delay in microseconds Command format: 0xFF <4BYTE delay>

         -  Delay for 100ms (100000us => 0x000186A0)

      ..

                        FF A0 86 01 00

Display Timing Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^

   These parameters are mandatory for SL1640/SL1680 and optional for
   SL1620.

   -  *VB_MIN* - Minimum vertical blanking for the Display TG

   -  *HB_MIN* - Minimum Horizontal blanking for the Display TG

   -  *V_OFF* - Vertical offset for the Display TG.

   -  *H_OFF* - Horizontal offset for the Display TG.

   -  *HB_VOP_OFF* - Horizontal VOP offset for the Display TG.

   -  *VB_VOP_OFF* - Vertical VOP offset for the Display TG

   -  *HB_BE* - Horizontal Blanking Back Edge for the Display TG.

   -  *VB_BE* - Vertical Blanking Back Edge for the Display TG.

   -  *HB_FP* - Horizontal Blanking Front porch for the Display TG.

   -  *VB_FP* - Vertical Blanking Front porch for the Display TG.

Reference entry for the MIPI DSI panel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Below is default entry for the MIPI-DSI in *dts*.

   This serves as a reference for a panel with resolution 800x1280 and
   HTotal = 952, VTOTAL = 1312.

   Refer the parameters above for further information on the panel.

   *&drm {*

      *…*

      *dsi_panel {*

         *status= "okay";*

         */\* Reset PIN configuration for the MIPI-DSI if available in the
         platform \*/*

         *mipirst-gpio = <&expander0 7 GPIO_ACTIVE_LOW>;*

         *NO_OF_RESID = <1>;*

         *DSI_RES = <102>;*

         *ACTIVE_WIDTH = <800>;*

         *HFP = <60>;*

         *HSYNCWIDTH = <32>;*

         *HBP = <60>;*

         *ACTIVE_HEIGHT = <1280>;*

         *VFP = <16>;*

         *VSYNCWIDTH = <2>;*

         *VBP = <14>;*

         *TYPE = <1>;*

         *SCAN = <0>;*

         *FRAME_RATE = <9>;*

         *FLAG_3D = <0>;*

         *FREQ = <75000>;*

         *PTS_PER_4 = <6000>;*

         *bits_per_pixel = <24>;*

         *busformat = <0>;*

         *HTOTAL = <952>;*

         *Lanes = /bits/ 8 <4>;*

         *Vid_mode = /bits/ 8 <2>;*

         *virtual_chan = /bits/ 8 <0>;*

         *Clk_Lane_Polarity = /bits/ 8 <0>;*

         *Data_Lane_Polarity = /bits/ 8 <0>;*

         *Recv_ack = /bits/ 8 <0>;*

         *Loosely_18 = /bits/ 8 <0>;*

         *H_polarity = /bits/ 8 <1>;*

         *V_Polarity = /bits/ 8 <1>;*

         *Data_Polarity = /bits/ 8 <1>;*

         *Eotp_tx = /bits/ 8 <1>;*

         *Eotp_rx = /bits/ 8 <0>;*

         *non-Continuous_clk = /bits/ 8 <1>;*

         *dpi_lp_cmd = /bits/ 8 <1>;*

         *Color_coding = /bits/ 8 <5>;*

         *Chunks = <0>;*

         *Null_Pkt = <0>;*

         *Byte_clk = <56250>;*

         *VB_MIN = /bits/ 8 <6>;*

         *HB_MIN = /bits/ 8 <30>;*

         *V_OFF = /bits/ 8 <6>;*

         *H_OFF = /bits/ 8 <20>;*

         *HB_VOP_OFF = /bits/ 8 <8>;*

         *VB_VOP_OFF = /bits/ 8 <3>;*

         *HB_BE = /bits/ 8 <7>;*

         *VB_BE = /bits/ 8 <2>;*

         *VB_FP = /bits/ 8 <2>;*

         *HB_FP = /bits/ 8 <10>;*

         *PIXEL_CLOCK = <75000>;*

         *command = /bits/ 8 <0x39 0x04 0xFF 0x98 0x81 0x03*

                     *0x15 0x02 0x01 0x00*

                     *…..*

                     *…..*

                     *0xFF 0xC0 0xD4 0x01 0x00*

                     *0x05 0x01 0x29*

                     *0xFF 0x10 0x27 0x00 0x00>;*

      *};*

   };

Sample configuration for waveshare 7-inch DSI panel: :doc:`waveshare_7inch_dsi-configuration`

TFT Display configuration 
--------------------------

   TBA

Panel Backlight Configuration
-----------------------------

.. _section-1:

Panel Backlight enable using Linux *defconfig* and *dts.*

   1. External backlight driver-based Panel (Example: TI LP855x part of
   Panel DC)

      i. Enable backlight driver in Linux kernel defconfig.

         *-CONFIG_BACKLIGHT_CLASS_DEVICE=m*

         *+CONFIG_BACKLIGHT_CLASS_DEVICE=y*

         *-# CONFIG_BACKLIGHT_LP855X is not set*

         *+CONFIG_BACKLIGHT_LP855X=y*

      ii. Create the entry in dts file for backlight driver.

         *backlight@2c {*

            *compatible = "ti, lp8556";*

            *reg = <0x2c>;*

            *bl-name = "lcd-bl";*

            *dev-ctrl = /bits/ 8 <0x05>;*

            *init-brt = /bits/ 8 <0xFF>;*

            *pwm-period = /bits/ 8 <0x00>;*

            */\* CFG2 \*/*

            *rom_A2h {*

               *rom-addr = /bits/ 8 <0xA2>;*

               *rom-val = /bits/ 8 <0x28>;*

         *};*

   2. Panel using SL16xx SOC PWM to control the backlight.

      **Kernel dts:**

      Configure the pinmux to support the PWM Backlight configuration in
      the dts file. Below are the details for sample panel and SL1680
      platform.

      **panel0-backlight** *{*

         *compatible = "pwm-backlight";*

         *pwms = <&\ *\ **pwm0** *1 1000000 0>;*

         *brightness-levels = <0 4 8 16 32 64 128 255>;*

         *default-brightness-level = <6>;*

         **enable-gpio** *=* *<&expander0 4 GPIO_ACTIVE_HIGH>;*

      *};*

      *pwm1_pmux: pwm1-pmux {*

         *groups = "SPI1_SS1n";*

         *function = "pwm";*

      *}*

      *&pwm0 {*

         *pinctrl-names = "default";*

         *pinctrl-0 = <&pwm1_pmux>;*

         *status = "okay";*

      *};*

SYNA DRM/KMS driver testing
===========================

   Upon SL1XXX platform boot-up, display comes up with Weston desktop by
   default.

   To execute sample test application such as modetest, disable Weston
   using below command.

   *systemctl stop Weston*

   *modetest* is a tool provided by *libdrm* library and is available as
   part of the SDK release/image (*/usr/local/bin/modetest*)

   Following are some of the tasks performed with *modetest*

   -  List all display capabilities: CRTCs, encoders & connectors (DP,
      HDMI, DSI ...), planes, modes...

   -  Perform basic tests: display a test pattern, display 2 layers,
      perform a *vsync* test.

   -  Specify the video mode: resolution and *refreshrate*.

..

   Below is the syntax.

   *modetest -M synaptics -s <connector_id> [,
   <connector_id>][@<crtc_id>]:[#<mode index>]<mode>[-<vrefresh>][@<format>]*

   Above application with the syntax provides the frame to Primary
   plane.

To list the connector, CRTC and plane information for the platform,
below command helps.

   *modetest -M synaptics*

SL1680 Display
---------------

SL1680, default configuration provides Encoders – 2, connectors – 2,

planes – 4 (MAIN, PIP, GFX1 and GFX2)

   Sample output of command **modetest -M synaptics** is as below:

   **Encoders**\ *:*

   *id crtc type possible crtcs possible clones*

   *38 0 TMDS 0x00000001 0x00000001*

   *40 0 DPI 0x00000002 0x00000002*

   **Connectors**\ *:*

   *id encoder status name size (mm) modes encoders*

   *37 0 connected HDMI-A-1 0x0 2 38*

      *modes:*

         *index name refresh (Hz) hdisp hss hse htot vdisp vss vse vtot*

      *#0 1920x1080 60.00 1920 2008 2052 2200 1080 1084 1089 1125 148500
      flags: nhsync, nvsync; type: preferred, driver*

      *#1 1280x720 60.00 1280 1390 1430 1650 720 725 730 750 74250 flags:
      phsync, pvsync; type: driver*

      *props:*

         *1 EDID:*

            *flags: immutable blob*

            *blobs:*

            *value:*

         *2 DPMS:*

            *flags: enum*

            *enums: On=0 Standby=1 Suspend=2 Off=3*

            *value: 3*

      *5 link-status:*

         *flags: enum*

         *enums: Good=0 Bad=1*

         *value: 0*

      *6 non-desktop:*

         *flags: immutable range*

         *values: 0 1*

         *value: 0*

      *4 TILE:*

         *flags: immutable blob*

      *blobs:*

      *value:*

   *39 0 connected DSI-1 0x0 1 40*

      *modes:*

         *index name refresh (Hz) hdisp hss hse htot vdisp vss vse vtot*

         *#0 800x1280 60.05 800 860 892 952 1280 1296 1298 1312 75000 flags: ;
         type: preferred, driver*

      *props:*

         *1 EDID:*

            *flags: immutable blob*

            *blobs:*

            *value:*

         *2 DPMS:*

            *flags: enum*

            *enums: On=0 Standby=1 Suspend=2 Off=3*

            *value: 3*

         *5 link-status:*

            *flags: enum*

            *enums: Good=0 Bad=1*

            *value: 0*

         *6 non-desktop:*

            *flags: immutable range*

            *values: 0 1*

            *value: 0*

         *4 TILE:*

            *flags: immutable blob*

            *blobs:*

            *value:*

      **CRTCs**\ *:*

      *id fb pos size*

      *35 0 (0,0) (0x0)*

      *#0 nan 0 0 0 0 0 0 0 0 0 flags: ; type:*

      *props:*

         *24 VRR_ENABLED:*

            *flags: range*

            *values: 0 1*

            *value: 0*

   *36 0 (0,0) (0x0)*

      *#0 nan 0 0 0 0 0 0 0 0 0 flags: ; type:*

      *props:*

         *24 VRR_ENABLED:*

            *flags: range*

            *values: 0 1*

            *value: 0*

      *Planes:*

      *id crtc fb CRTC x,y x,y gamma size possible crtcs*

      *31 0 0 0,0 0,0 0 0x00000003*

         *formats: NV12 NV21 UYVY VYUY YUYV YVYU*

         *props:*

            *8 type:*

               *flags: immutable enum*

               *enums: Overlay=0 Primary=1 Cursor=2*

               *value: 0*

      *32 0 0 0,0 0,0 0 0x00000003*

         *formats: XR24 AR24 XB24 AB24 NV12 NV21*

         *props:*

            *8 type:*

            *flags: immutable enum*

            *enums: Overlay=0 Primary=1 Cursor=2*

            *value: 1*

      *33 0 0 0,0 0,0 0 0x00000003*

         *formats: XR24 AR24 XB24 AB24*

      *props:*

         *8 type:*

            *flags: immutable enum*

            *enums: Overlay=0 Primary=1 Cursor=2*

            *value: 1*

      *34 0 0 0,0 0,0 0 0x00000003*

         *formats: XR24 AR24 XB24 AB24*

         *props:*

            *8 type:*

            *flags: immutable enum*

            *enums: Overlay=0 Primary=1 Cursor=2*

            *value: 0*

      *Frame buffers:*

         *id size pitch*

Single Display Mode (HDMI only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Push frame to GFX1 plane using below modetest command.

..

   *modetest -M synaptics -s 37@35:1920x1080@AR24*

-  Push frame to both GFX1 and PIP plane using below modetest command.

..

   *modetest -M synaptics -s 37@35:1920x1080@AR24 -P
   32@37:1920x1080@AR24*

Dual Display Mode (HDMI + MIPI-DSI)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Push frame to GFX1 plane (Display on HDMI) using below modetest
   command.

..

   *modetest -M synaptics -s 37@35:1920x1080@AR24*

-  Push frame to PIP plane (Display on DSI) using below modetest
   command.

..

   *modetest -M synaptics -s 39@36:800x1280@AR24*

SL1640 Display
--------------

   SL1640 Supports: Encoder – 1; CRTC – 1; Planes – 2 (MAIN and GFX1
   planes)

Single Display (HDMI only)
^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Push frame to GFX1 plane using below modetest command.

..

   *modetest -M synaptics -s 36@35:1920x1080@AR24*

Single Display (MIPI-DSI only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Push frame to GFX1 plane using below modetest command.

..

   *modetest -M synaptics -s 36@35:800x1280@AR24*

SL1620 Display
---------------

   Default list of connector/mode details in SL1620 is as below:

   *Encoders:*

   *id crtc type possible crtcs possible clones*

   *35 0 DPI 0x00000001 0x00000001*

   *37 0 DSI 0x00000002 0x00000002*

   *Connectors:*

   *id encoder status name size (mm) modes encoders*

   *36 0 connected DPI-1 0x0 1 35*

   *modes:*

      *index name refresh (Hz) hdisp hss hse htot vdisp vss vse vtot*

   *#0 800x480 59.72 800 1010 1012 1058 480 502 504 527 33300 flags: ;
   type: preferred, driver*

   *…*

   *…*

   *38 0 connected DPI-2 0x0 1 37*

   *modes:*

      *index name refresh (Hz) hdisp hss hse htot vdisp vss vse vtot*

   *#0 800x1280 60.05 800 860 892 952 1280 1296 1298 1312 75000 flags: ;
   type: preferred, driver*

   *…*

   *…*

TFT Display
^^^^^^^^^^^

-  Push frame to TFT display using below *modetest* command.

..

   *modetest -M synaptics -s 36@33:800x480@AR24*

MIPI-DSI Display
^^^^^^^^^^^^^^^^

-  Push frame to MIPI-DSI display using below *modetest* command.

..

   *modetest -M synaptics -s 38@34:800x1280@AR24*
