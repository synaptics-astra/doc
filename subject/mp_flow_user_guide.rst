========================
Astra MP Flow User Guide
========================


Introduction
============

This guide provides detailed instructions for configuring, generating, and flashing keys into the One-Time Programmable Memory (OTP) for Astra Machina in production environments.

System Requirements
===================

- Ubuntu 16.04 x86_64 desktop edition
- Python 2.7.1+
- libssl1.0.0

Definitions
===========

- syna-release SDK: A software development kit from Synaptics used to build normal eMMC images and USB Boot Linux Image Packs.
- normal_eMMCimg: It's an eMMC image built from the syna-release SDK.
- production_eMMCimg: It's an eMMCimg, REE images have been to set the production_image_flag = 1. This image only can be run on the production boards (secure boot actived).
- usb_tool: It's a toolset designed for use on a PC, enabling booting of the Astra board via USB.
- factory_tool: It's post-processing tool in syna-release SDK that using to generate secure keys, OTP layouts, production eMMCimg and resign "USB Boot Linux Image Pack" REE images. 

Tools can be found in the `Factory repository <https://github.com/synaptics-astra/factory/tree/#release#>`__ at
``factory/scripts/[platypus/dolphin/myna2/]/factory``. ``platypus``: SL1640, ``dolphin``: SL1680, ``myna2``: SL1620.

Pre-MP Preparation
==================

1. Assign REE SegID in Configuration File
   The REE segmentation ID must align with the root key of REE (OEM) images, ensuring that all images share the same segmentation ID.
   Therefore, REE segmentation ID must be assigned by OEM, and two values are stored in ``[factory tool]/config/oem_config.conf``, 
   and must be set to the expected values before running key generation tool.
   For example,

::
   
       [Segmentation ID]
       ree_segid = 0x2E32000A
       [Version]
       ree_version = 0x00000000

2. Generate REE RSA Keys and AESK0 Keys

   a) Utilize the tool located in ``[factory_tool]`` for this process.
   b) Execute the following script to generate REE RSA keys and AESK0 keys necessary for signing and encrypting REE images.

::

    $ ./gen_all_keys_stores.py

After running the script, the following keys are generated:
   - ``K0_REE.rsa.priv.pem``: 2048-bit RSA private key for signing ``K1_REE_A.rsa.pub.pem``, ``K1_REE_B.rsa.pub.pem``, and ``K1_REE_C.rsa.pub.pem``.
   - ``K0_REE_store.bin``: image holding the public key of ``K0_REE.rsa.priv.pem``.
   - ``K1_REE_A.rsa.priv.pem``: 2048-bit RSA private key for signing OEM bootloader(Uboot) and TZK images.
   - ``K1_REE_A_store.bin``: image holding the public key of ``K1_REE_A.rsa.priv.pem``.
   - ``K1_REE_B.rsa.priv.pem``: 2048-bit RSA private key for signing SM firmware images.
   - ``K1_REE_B_store.bin``: image holding the public key of ``K1_REE_B.rsa.priv.pem``.
   - ``K1_REE_C.rsa.priv.pem``: 2048-bit RSA private key for signing Linux image.
   - ``K1_REE_C_store.bin``: image holding the public key of ``K1_REE_C.rsa.priv.pem``.
   - ``AESK0.bin``: 128-bit root AES key.
   - ``AESK0_K0_REE.bin``: derived from ``AESK0.bin``, 128-bit AES key to encrypt ``K0_REE_store.bin``
   - ``AESK0_ATF.bin``: derived from ``AESK0.bin``, 128-bit AES key to encrypt ATF.
   - ``AESK0_TZ_KERNEL.bin``: derived from ``AESK0.bin``, 128-bit AES key to encrypt OPTEE.
   - ``AESK0_TZK_BOOT_PARAMETER.bin``: derived from ``AESK0.bin``, 128-bit AES key to encrypt TZK boot parameter.
   - ``AESK0_BOOT_LOADER.bin``: derived from ``AESK0.bin``, 128-bit AES key to encrypt OEM bootloader(Uboot).
   - ``AESK0_SM_FW.bin``: derived from ``AESK0.bin``, 128-bit AES key to encrypt SM firmware.
   - ``AESK0_LINUX.bin``: derived from ``AESK0.bin``, 128-bit AES key to encrypt Linux kernel image.

3. Generate Production eMMCimg

   a) Refer to the build guide for generating a normal eMMCimg.
   b) Utilize the tool located in ``[factory_tool]`` for this process.
   c) Execute the following script to resign REE images from Normal eMMCimg directory.

::
   
      $ ./gen_production_image.py [normal_eMMCimg] -o [production_eMMCimg]

eMMC flash content changes
--------------------------

+---------------------------------+--------------------------------------------+----------------------------------------------------------------------------------------------------+
| Image                           | Before Factory Flow  (Normal eMMCimg)      | After Factory Flow (Production eMMCimg)                                                            |
+=================================+============================================+====================================================================================================+
| K0_REE  (in preboot.subimg)     | non-production value                       | k0_ree.bin generated from gen_all_keys_stores.py, included in preboot.subimg                       |
+---------------------------------+--------------------------------------------+----------------------------------------------------------------------------------------------------+
| K1_REE_A/B/C (in preboot.subimg)| non-production value                       | k1_ree_a.bin, k1_ree_b.bin and k1_ree_c.bin from gen_all_keys_stores.py, included in preboot.subimg|
+---------------------------------+--------------------------------------------+----------------------------------------------------------------------------------------------------+
| tzk.subimg                      | Clear, authentication is bypassed          | Encrypted by aesk0_atf.bin/aesk0_tz_kernel.bin/aesk0_tzk_boot_parameter.bin, signed by K1_REE_A    |
+---------------------------------+--------------------------------------------+----------------------------------------------------------------------------------------------------+
| bl.subimg                       | Clear, authentication is bypassed          | Encrypted by aesk0_boot_loader.bin, signed by K1_REE_A                                             |
+---------------------------------+--------------------------------------------+----------------------------------------------------------------------------------------------------+
| firmware.subimg  (SM FW)        | Clear, authentication is bypassed          | Encrypted by aesk0_sm_fw.bin, signed by K1_REE_B                                                   |
+---------------------------------+--------------------------------------------+----------------------------------------------------------------------------------------------------+
| boot.subimg                     | Clear, authentication is bypassed          | Encrypted by aesk0_linux.bin, signed by K1_REE_C                                                   |
+---------------------------------+--------------------------------------------+----------------------------------------------------------------------------------------------------+
| fastlogo.subimg                 | Clear, authentication is bypassed          | Signed by K1_REE_A                                                                                 |
+---------------------------------+--------------------------------------------+----------------------------------------------------------------------------------------------------+
      
4. Resign "USB Boot Linux Image Pack" images

   a) Utilize the tool located in ``[factory_tool]`` to resign "USB Boot Linux Image Pack" images used after the MP flow.
   b) Execute the following script to resign REE images from image directory that in USB boot tool directory.

::

      $ ./resign_usb_boot_image.py [usb_tool/image_dir] -o [output_image_dir]
     
USB Boot tool content changes
-----------------------------

+-----------------------------------+--------------------------------------------+---------------------------------------------------------------------------------------------------+
| Image                             | Before Factory Flow  (Normal eMMCimg)      | After Factory Flow (Production eMMCimg)                                                           |
+===================================+============================================+===================================================================================================+
| K0_REE  (in gen3_bkl.bin.usb)     | non-production value                       | k0_ree.bin generated from gen_all_keys_stores.py, included gen3_bkl.bin.usb                       |
+-----------------------------------+--------------------------------------------+---------------------------------------------------------------------------------------------------+
| K1_REE_A/B/C (in gen3_bkl.bin.usb)| non-production value                       | k1_ree_a.bin, k1_ree_b.bin and k1_ree_c.bin from gen_all_keys_stores.py, included gen3_bkl.bin.usb|
+-----------------------------------+--------------------------------------------+---------------------------------------------------------------------------------------------------+
| gen3_tzk.bin.usb                  | Clear, authentication is bypassed          | Encrypted by aesk0_atf.bin/aesk0_tz_kernel.bin/aesk0_tzk_boot_parameter.bin, signed by K1_REE_A   |
+-----------------------------------+--------------------------------------------+---------------------------------------------------------------------------------------------------+
| gen3_uboot.bin.usb                | Clear, authentication is bypassed          | Encrypted by aesk0_boot_loader.bin, signed by K1_REE_A                                            |
+-----------------------------------+--------------------------------------------+---------------------------------------------------------------------------------------------------+

5. Generate OTP layout for MAC_ADDRESS OTP Programming (Optional)

   a) Utilize the tool located in ``[factory_tool]`` for this process.
   b) Execute the following script to generate MAC_ADDRESS OTP layouts

   ::

      $ ./tools/gen_genx_otp_layout_v1 -M <mac_addr_hex_value> -s tools/device_prov_pub.pem -o <otp_mac_addr_out>.bin

   example:
  
   ::

       $ ./tools/gen_genx_otp_layout_v1 -M 0x123456781234 -s tools/device_prov_pub.pem -o mac_addr_layout_123456781234.bin

   c) ``<otp_mac_addr_out>.bin``, the mac_addr OTP layout file will appear in the current directory.

6. Generate OTP layout for production OTP Programming

   a) Utilize the tool located in ``[factory_tool]`` for this process.
   b) Execute the following script to generate OTP layouts::

      $ ./gen_otp.py --out <otp_output_name>.bin

   example:

   ::

       $ ./gen_otp.py --out otp_layout.bin

   c) ``<otp_output_name>.bin``, the otp layout files will appear in the current directory.
   
OTP fuse changes during factory flow
------------------------------------

+-------------------------+-----------------------+------------------------+
| OTP                     | Before Factory Flow   | After Factory Flow     |
+=========================+=======================+========================+
| REE_Security_Enable     | Unprogrammed          | 1                      |
+-------------------------+-----------------------+------------------------+
| K0_REE                  | Unprogrammed          | SHA-256 of K0_REE      |
+-------------------------+-----------------------+------------------------+
| REE_SEGID               | Unprogrammed          | OEM value              |
+-------------------------+-----------------------+------------------------+
| AESK0                   | Unprogrammed          | OEM value              |
+-------------------------+-----------------------+------------------------+
| SCS_Total_Area_Size_Sel | Unprogrammed          | 385K                   |
+-------------------------+-----------------------+------------------------+
| OTP                     | Before Factory Flow   | After Factory Flow     |
+-------------------------+-----------------------+------------------------+
| jtag_protection_level   | Unprogrammed          | 1                      |
+-------------------------+-----------------------+------------------------+
| MP_provision_done       | Unprogrammed          | 1                      |
+-------------------------+-----------------------+------------------------+


Go Through MP flow (OTP programming and eMMCimg updating)

1. Flash Production eMMCimg

   a) Copy the Production eMMCimg to an external USB drive or usb_boot tool directory.
   b) Boot into USB U-Boot.
   c) Execute the following U-Boot command to flash eMMCimg ``production_eMMCimg`` from external USB drive.
   
   ::

         => usb2emmc <production_eMMCimg>
      

   Execute the following U-Boot command to flash eMMCimg ``production_eMMCimg`` from usb_boot tool directory.
   
   ::

        => l2emmc <production_eMMCimg>

2. Fuse MAC_ADDRESS into OTP (optional)

   a) Execute the following U-Boot commands to load the OTP layout from usb_boot tool directory and program OTP.
   
   ::

      => usbload <mac_addr_otp_layout_path> <fileaddr>
      => otp write <fileaddr> <filesize>

   example:
   
   ::

     usbload mac_addr_layout_123456781234.bin 0x7000000
     otp write 0x7000000 0x500

   b) Execute the following U-Boot commands to load OTP layout from external USB Drive to and program OTP.
   
   ::

     => usb start
     => fatload <interface> [<dev[:part]> <fileaddr> <mac_addr_otp_layout_path> 
     => otp write <fileaddr> <filesize>

   example:
   
   ::
   
     usb start
     fatload usb 0:1 0x7000000 mac_addr_layout_123456781234.bin
     otp write 0x7000000 0x500

   c) Check MAC address with below uboot commands
   
   ::

      => net_init
      => printenv
     
   example:

   ::

     => net_init

      Warning: ethernet@b60000 using MAC address from ROM
      eth0: ethernet@b60000
     
      => printenv
      autoload=n
      baudrate=115200
      bootcmd=bootmmc
      bootdelay=0
      ethaddr=12:34:56:78:12:34
      fdtcontroladdr=21730290
      preboot=show_logo;
      ver=U-Boot 2019.10-g45105f1b01-dirty (Sep 18 2024 - 18:31:01 +0000)

      Environment size: 193/65532 bytes

3. Fuse OTP

   a) Execute the following U-Boot commands to load OTP layout from usb_boot tool directory and program OTP
   
   ::

      => usbload <otp_layout_path> <fileaddr>
      => otp write <fileaddr> <filesize>

   example:
   
   ::
   
      => usbload otp_layout.bin 0x7000000
      => otp write 0x7000000 0x500
     
   b) Execute the following U-Boot commands to load OTP layout from external USB Drive and program OTP
   
   ::

      => usb start
      => fatload <interface> [<dev[:part]> <fileaddr> <otp_layout_path> 
      => otp write <fileaddr> <filesize>
    
   example:
   
   ::

      usb start
      fatload usb 0:1 0x7000000 otp_layout.bin
      otp write 0x7000000 0x500
