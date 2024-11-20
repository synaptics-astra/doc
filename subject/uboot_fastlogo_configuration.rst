=======================================
Uboot Fastlogo Customization User Guide
=======================================

Introduction
============

Overview
========

The scope of the document is to provide detailed steps to customize Uboot Fastlogo for SL16xx display interfaces.

Astra Machina Display Capabilities
==================================

Syna Uboot video driver is supported for the SL16xx Astra Machina platforms.

Display capability of the supported SoC’s
-----------------------------------------

-  SL1680: Supports Dual Fastlogo Display (HDMI and MIPI-DSI)

-  SL1640: Supports Single Fastlogo (Either HDMI or MIPI-DSI)

-  SL1620: Supports Dual Fastlogo (TFT and MIPI-DSI)

SYNA Uboot Fastlogo Configuration
=================================

Uboot video driver and panel configurations are handled through *defconfig*, *dts* and header files.

Configurations based on defconfig
=================================

Uboot *defconfig* for each platform is given below:

1. SL1680: ``dolphin_suboot_defconfig``

2. SL1640: ``platypus_suboot_defconfig``

3. SL1620: ``myna2_suboot_defconfig``

Following configurations are enabled in *defconfig*:

1. Video driver

2. Backlight

3. Panel name

Configuration based on dts
==========================

*dts* files of each platform given below:

-  SL1620: ``myna2-rdk.dts``

-  SL1640: ``platypus-rdk.dts``

-  SL1680: ``dolphin-rdk.dts``

Following device configurations are handled through *dts* files:

1. Generic Display configuration

2. MIPI-DSI Panel configuration

3. LCDC panel configuration

dts configuration template for SL16XX given below
-------------------------------------------------

*dts* for SL1640 and SL1680
---------------------------

::

   &vpp_fb {
     Generic Display configuration
     MIPI-DSI Panel configuration
   };

*dts* for SL1620
----------------

::

   &lcdc_fb {
      MIPI-DSI Panel configuration
      LCDC panel specific configuration
   };

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

``u-boot/arch/arm/mach-synaptics/drivers/video/vpp_ca/thinvpp_ca/include/vpp_api.h``

-  **disp1-type:** Type of the Display1 whether it is HDMI or MIPI-DSI.

-  **disp2-res-id:** Resolution Id corresponding to the timing
   information. In case of dual Display, display2 must be MIPI-DSI and
   resolution id is fixed to 102.

-  **disp2-type:** Type of the Display2.

SL1640/SL1680 Single/Dual Display configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default configuration for SL1640 and SL1680 given as below.

-  SL1640 - Single Display mode – HDMI only.

-  SL1680 - Dual Display mode – HDMI + MIPI-DSI

..

Display mode can be changed in *dts*. Single Display mode is
applicable for both SL1640 and SL1680.

Below is an example for Single display mode.

**Single Display: HDMI Display Mode**

::

   &vpp_fb {
      disp-mode = <0>;
      disp1-res-id = <24>;
   };

**Single Display mode: MIPI-DSI Display Mode**

::

   &vpp_fb {
      disp-mode = <1>;
      disp1-res-id = <102>;
   };

SL1680 Dual Display configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Dual Display Mode (HDMI as primary + MIPI-DSI as secondary)**

::

   &vpp_fb {
      disp-mode = <2>;
      disp1-res-id = <24>;
      disp2-res-id = <102>;
   };

Note:

-  For MIPI-DSI Display: RESID is fixed to **102** where it takes the
   custom timing provided in the *dts*.

SL1620 Display configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default display configuration for SL1620 is Dual – TFT + MIPI-DSI.

*lcdc_panel* node and *dsi_panel* nodes in *dts* decide the number of
displays.

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

::

   &vpp_fb {

      … 

      dsi_panel {
         status= "okay";

         /* Reset PIN configuration for the MIPI-DSI if available in the
         platform */

         mipirst-gpio = <&expander0 7 GPIO_ACTIVE_LOW>;
         NO_OF_RESID = <1>;
         DSI_RES = <102>;
         ACTIVE_WIDTH = <800>;
         HFP = <60>;
         HSYNCWIDTH = <32>;
         HBP = <60>;
         ACTIVE_HEIGHT = <1280>;
         VFP = <16>;
         VSYNCWIDTH = <2>;
         VBP = <14>;
         TYPE = <1>;
         SCAN = <0>;
         FRAME_RATE = <9>;
         FLAG_3D = <0>;
         FREQ = <75000>;
         PTS_PER_4 = <6000>;

         bits_per_pixel = <24>;
         busformat = <0>;

         HTOTAL = <952>;
         Lanes = /bits/ 8 <4>;
         Vid_mode = /bits/ 8 <2>;
         virtual_chan = /bits/ 8 <0>;
         Clk_Lane_Polarity = /bits/ 8 <0>;
         Data_Lane_Polarity = /bits/ 8 <0>;
         Recv_ack = /bits/ 8 <0>;
         Loosely_18 = /bits/ 8 <0>;
         H_polarity = /bits/ 8 <1>;
         V_Polarity = /bits/ 8 <1>;
         Data_Polarity = /bits/ 8 <1>;
         Eotp_tx = /bits/ 8 <1>;
         Eotp_rx = /bits/ 8 <0>;
         non-Continuous_clk = /bits/ 8 <1>;
         dpi_lp_cmd = /bits/ 8 <1>;
         Color_coding = /bits/ 8 <5>;
         Chunks = <0>;
         Null_Pkt = <0>;
         Byte_clk = <56250>;

         VB_MIN = /bits/ 8 <6>;
         HB_MIN = /bits/ 8 <30>;
         V_OFF = /bits/ 8 <6>;
         H_OFF = /bits/ 8 <20>;
         HB_VOP_OFF = /bits/ 8 <8>;
         VB_VOP_OFF = /bits/ 8 <3>;
         HB_BE = /bits/ 8 <7>;
         VB_BE = /bits/ 8 <2>;
         VB_FP = /bits/ 8 <2>;
         HB_FP = /bits/ 8 <10>;
         PIXEL_CLOCK = <75000>;
      };
   };
  
MIPI-DSI panel commands
=======================

Panel Initialization Commands are added in panel_cfg.h. Command format is as given below

::

   Format - <CMD> <Payloadlength-n> <BYTE1> <...> <BYTEn>

Long write Ex: 39 04 FF 98 81 03
CMD => 0x39
Length => 0x04
Data/Payload => FF 98 81 03

Incase a delay need be added, refer below:

Delay in microseconds Command format: 0xFF <4BYTE delay>
   **FF A0 86 01 00** (Command for 100ms Delay (100000us => 0x000186A0))

For ex: Haier MIPI-DSI panel header file is located in ``<UBoot_path>/arch/arm/mach-synaptics/drivers/video/panel/haier_800_1280/panelcfg.h``

Incase of new panel support, it can be under ``panel/<panel_name>/panel_cfg.h``

To select panel, name of the panel (folder in which the panel_cfg.h is available) should be specified in ``configs/<platform>*_defconfig``.

| For ex: If haier panel has to be chosen in SL1620: Below line should be added to ``myna2_suboot_defconfig``.

| **CONFIG_PANEL_CFG="haier_800_1280"**

*Reference panel_cfg.h for Haier 800x1280 Panel :*
--------------------------------------------------

::

   UINT8 panel_commands[] = {
      0x39, 0x04, 0xFF, 0x98, 0x81, 0x03,
      0x15, 0x02, 0x01, 0x00,
      0x15, 0x02, 0x02, 0x00,
      0x15, 0x02, 0x03, 0x73,
      0x15, 0x02, 0x04, 0xD7,
      ...
   };
