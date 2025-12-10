========================
Astra MP Flow User Guide
========================

.. contents::
   :depth: 3


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
``factory/scripts/[platypus/dolphin/myna2/]/factory``. Where ``platypus``: SL1640, ``dolphin``: SL1680, ``myna2``: SL1620.

Pre-MP Preparation
==================

1. Assign REE SegID in Configuration File
------------------------------------------------------------

   The REE segmentation ID must align with the root key of REE (OEM) images, ensuring that all images share the same segmentation ID.

   REE segmentation ID are stored in ``factory/scripts/[platypus/dolphin/myna2/]/factory/config/oem_config.conf``, and must be set to the expected values before running key generation tool.
   For example, adjust the ree_segid = 0x2E32000A in the configuration file as below:

::
   
       [Segmentation ID]
       ree_segid = 0x2E32000A

       [Version]
       ree_version = 0x00000000

       [OTP_REE_SECURITY_ENABLE]
       ree_security_enable = 1

       [OTP_BOOT_SECURITY_ENABLE]
       boot_security_enable = 1

       [OTP_MP_PROVISION_DONE]
       mp_provision_done = 0

       [OTP_SCS_AREA_SIZE_SEL]
       scs_area_size_sel = 0

       [OTP_REE_JTAG_PROTECTION_POLICY]
       ree_jtag_protection_policy = 1

       [OTP_EMMC_BOOT_DISABLE]
       emmc_boot_disable = 0

       [OTP_SPI_BOOT_DISABLE]
       spi_boot_disable = 0

       [OTP_OEM_AUDIO_CUSTOMER_ID]
       oem_audio_customer_id = 0x00000000

       [OTP_PRODUCTION_CHIP_FLAG]
       production_chip_flag = 0x00000007


2. Generate REE RSA Keys and AESK0 Keys
------------------------------------------------------------


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
------------------------------------------------------------

   a) Refer to the build guide for generating a normal eMMCimg.
   b) Utilize the tool located in ``[factory_tool]`` for this process.
   c) Execute the following script to resign REE images from Normal eMMCimg directory.

::
   
      $ ./gen_production_image.py [normal_eMMCimg] -o [production_eMMCimg]

eMMC flash content changes:


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
------------------------------------------------------------


   a) Utilize the tool located in ``[factory_tool]`` to resign "USB Boot Linux Image Pack" images used after the MP flow.
   b) Execute the following script to resign REE images from image directory that in USB boot tool directory.

::

      $ ./resign_usb_boot_image.py [usb_tool/image_dir] -o [output_image_dir]
     
USB Boot tool content changes:


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


5. Generate OTP commands for production OTP Programming
------------------------------------------------------------

Use the helper script gen_otp_command.py to generate OTP programming commands instead of writing them by hand.

The tool can be found under `Factory repository <https://github.com/synaptics-astra/factory/tree/#release#>`__ at
``factory/scripts/[platypus/dolphin/myna2/]/factory``. Where
``platypus``: SL1640, ``dolphin``: SL1680, ``myna2``: SL1620.

Update the ``factory/scripts/[platypus/dolphin/myna2/]/factory/config/oem_config.conf`` settings as needed. Remember don't
change ree_segid = 0x2E32000A as it should be updated in step 1.

Adjust the configuration file as below if necessary. For OTP fields, please refer to 
:ref:`OTP_Field_Definitions_Table` for details.

::
   
       [Segmentation ID]
       ree_segid = 0x2E32000A

       [Version]
       ree_version = 0x00000000

       [OTP_REE_SECURITY_ENABLE]
       ree_security_enable = 1

       [OTP_BOOT_SECURITY_ENABLE]
       boot_security_enable = 1

       [OTP_MP_PROVISION_DONE]
       mp_provision_done = 0

       [OTP_SCS_AREA_SIZE_SEL]
       scs_area_size_sel = 0

       [OTP_REE_JTAG_PROTECTION_POLICY]
       ree_jtag_protection_policy = 1

       [OTP_EMMC_BOOT_DISABLE]
       emmc_boot_disable = 0

       [OTP_SPI_BOOT_DISABLE]
       spi_boot_disable = 0

       [OTP_OEM_AUDIO_CUSTOMER_ID]
       oem_audio_customer_id = 0x00000000

       [OTP_PRODUCTION_CHIP_FLAG]
       production_chip_flag = 0x00000007


Examples: (Platypus: SL1640)
   ::

   $sdk/factory/scripts/platypus/factory$ ./gen_otp_command.py

When the command completes, two files will be generated in the current directory:

    - otp_commands_uboot.txt:  U-Boot otpwrite commands
    - otp_commands_linux.txt:  Linux factory_util 6 otpwrite commands

The script performs the following:

    - Reads OTP configuration and keys from 
        - configs/oem_config.conf
        - keys/K0_REE_hash.bin
        - keys/AESK0.bin

    - Applies the mask rules described in this document

    - Enforces atomic programming rules for:
         - OTP_K0_OEM_HASH_0 ~ 7
         - OTP_AESK0_0 ~ 3
         - OTP_REE_SEGID
         - OTP_REE_SECURITY_ENABLE
         - OTP_BOOT_SECURITY_ENABLE
         - OTP_PRODUCTION_CHIP_FLAG

    - Treats OTP_MP_PROVISION_DONE as a special case:
          - If its value is 0, the command is skipped and a
            [SKIP] message is printed
          - User can perform the OTP_MP_PROVISION_DONE = 1 command when
            ALL the OTP fields are done in the LAST production SESSION.

    - Tags atomic items in the debug output with [Atomic]

Below is a sample execution log:

   ::


    $sdk/factory/scripts/platypus/factory$ ./gen_otp_command.py
    [SKIP] OTP_MP_PROVISION_DONE value is 0, command not generated
    otpwrite 100 0x98bead63 0xffffffff [Atomic]
    otpwrite 101 0x0732d206 0xffffffff [Atomic]
    otpwrite 102 0x6162bc31 0xffffffff [Atomic]
    otpwrite 103 0x3433e405 0xffffffff [Atomic]
    otpwrite 104 0xe15933d7 0xffffffff [Atomic]
    otpwrite 105 0x3e6e6562 0xffffffff [Atomic]
    otpwrite 106 0x2c56fbaf 0xffffffff [Atomic]
    otpwrite 107 0x49486fa9 0xffffffff [Atomic]
    otpwrite 108 0x5a319519 0xffffffff [Atomic]
    otpwrite 109 0xd2b79aab 0xffffffff [Atomic]
    otpwrite 110 0x88edae3e 0xffffffff [Atomic]
    otpwrite 111 0x0f6f2a3b 0xffffffff [Atomic]
    otpwrite 112 0x2E32000A 0xffffffff [Atomic]
    otpwrite 113 0x00000001 0x00000001 [Atomic]
    otpwrite 114 0x00000001 0x00000001 [Atomic]
    otpwrite 116 0x00000000 0x00000003
    otpwrite 117 0x00000001 0x00000003
    otpwrite 200 0x00000000 0x00000001
    otpwrite 201 0x00000000 0x00000001
    otpwrite 203 0x00000000 0xffffffff
    otpwrite 204 0x00000007 0x00000007 [Atomic]
    [OK] Wrote 21 lines to otp_commands_uboot.txt
    [OK] Wrote 21 lines to otp_commands_linux.txt

Notes:

    - Refer to :ref:`Atomic_Programming_Rules` for details on atomic programming rules.

    - Lines tagged with [Atomic] belong to the atomic security group and MUST be programmed as part of one provisioning session without reboot or power loss.

    - otp_commands_uboot.txt contains commands in the form to perform in u-boot:
          otpwrite <idx> <value> <mask>

    - otp_commands_linux.txt contains commands in the form to perform in Linux:
          factory_util 6 otpwrite <idx> <value> <mask>
   

Go Through MP flow
===================================================================

1. Flash Production eMMCimg
------------------------------

   a) Copy the Production eMMCimg to an external USB drive or usb_boot tool directory.
   b) Boot into USB U-Boot.
   c) Execute the following U-Boot command to flash eMMCimg ``production_eMMCimg`` from external USB drive.
   
   ::

         => usb2emmc <production_eMMCimg>
      

   Execute the following U-Boot command to flash eMMCimg ``production_eMMCimg`` from usb_boot tool directory.
   
   ::

        => l2emmc <production_eMMCimg>


2. Fuse OTP
------------------------------

Assume fuse the OTP in u-boot environment. The otp_commands_uboot.txt contains commands in the form to perform in u-boot.
Either copy and paste the commands (i.e., otp_commands_uboot.txt) one by one or create a script image (.scr) to execute all 
commands automatically in u-boot. Below is the instruction to create a script image (.scr) from otp_commands_uboot.txt.

  
   ::

      $ mkimage -A arm -O linux -T script -C none -n "OTP script" -d otp_commands_uboot.txt otp_commands_uboot.scr

      Image Name:   OTP script
      Created:      Tue Dec  9 13:33:26 2025
      Image Type:   ARM Linux Script (uncompressed)
      Data Size:    708 Bytes = 0.69 KiB = 0.00 MiB
      Load Address: 00000000
      Entry Point:  00000000
      Contents:
          Image 0: 700 Bytes = 0.68 KiB = 0.00 MiB

      $ which mkimage
      /usr/bin/mkimage

      $ mkimage --version
      mkimage version 2025.01

      $ file /usr/bin/mkimage
      /usr/bin/mkimage: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=5971adb62d81976b9c7c36b1f5b6d974495e8de6, for GNU/Linux 3.2.0, stripped


   
   Copy the otp_commands_uboot.scr to an external USB drive or usb_boot tool directory.
   
   a) Execute the following U-Boot commands to load otp_commands_uboot.scr from usb_boot tool directory and program OTP
   
   ::

      => usbload otp_commands_uboot.scr <addr>
      => source <addr>

   example:
   
   ::
   
      => usbload otp_commands_uboot.scr 0x7000000
      => source 0x7000000
     
   b) Execute the following U-Boot commands to load otp_commands_uboot.scr from external USB Drive and program OTP
   
   ::

      => usb start
      => fatload <interface> [<dev[:part]> <fileaddr> <otp_layout_path> 
      => otp write <fileaddr> <filesize>
    
   example:
   
   ::

      => usb start
      => fatload usb 0:1 0x7000000 otp_commands_uboot.scr
      => source 0x7000000


.. note::

    CONFIG_CMD_SOURCE=y must be enabled in U-Boot configuration to use the source command.

    ::

      boot\u-boot\configs\platypus_usb_suboot_defconfig

      CONFIG_CMD_SOURCE=y
