===================================================
 OTP Access Utility Guide (Klamath: SL261x)
===================================================

.. contents::
   :depth: 3

Introduction
====================================================================

This document describes the usage of the OTP access utilities for
``klamath``: SL261x in u-boot environment:

  - U-Boot environment      : otpread / otpwrite

OTP (One-Time Programmable) memory allows permanent configuration of
security keys, boot policies, and OEM information.

.. _OTP_Field_Definitions_Table:

OTP Field Definitions Table
====================================================================

Each OTP index has a fixed access permission and a valid data mask.
Only bits set in the mask are allowed to be programmed.

"Atomic Item" indicates whether the field MUST be programmed as part
of the atomic security provisioning group.

+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| Index | Name                          | Read / Write Permission | Mask       | Atomic Item| Comments                                    |
+=======+===============================+=========================+============+============+=============================================+
| 44    | OTP_SYNA_IMAGE_SECURE_BOOT_EN | Read / Write            | 0xFFFFFFFF | NO         | Enable the syna image secure boot feature   |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 72    | OTP_JTAG_ACCESS_CONTROL       | Read / Write            | 0xFFFFFFFF | NO         | JTAG access control                         |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 80    | OTP_K0_OEM_HASH_0             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 0 (512-bit)   |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 81    | OTP_K0_OEM_HASH_1             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 1             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 82    | OTP_K0_OEM_HASH_2             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 2             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 83    | OTP_K0_OEM_HASH_3             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 3             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 84    | OTP_K0_OEM_HASH_4             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 4             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 85    | OTP_K0_OEM_HASH_5             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 5             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 86    | OTP_K0_OEM_HASH_6             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 6             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 87    | OTP_K0_OEM_HASH_7             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 7             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 88    | OTP_K0_OEM_HASH_8             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 8             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 89    | OTP_K0_OEM_HASH_9             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 9             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 90    | OTP_K0_OEM_HASH_10            | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 10            |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 91    | OTP_K0_OEM_HASH_11            | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 11            |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 92    | OTP_K0_OEM_HASH_12            | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 12            |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 93    | OTP_K0_OEM_HASH_13            | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 13            |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 94    | OTP_K0_OEM_HASH_14            | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 14            |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 95    | OTP_K0_OEM_HASH_15            | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 15            |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 112   | OTP_CCGK_0                    | Write Only              | 0xFFFFFFFF | YES        | Customer Chip Global Key Word 0  (256-bit)  |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 113   | OTP_CCGK_1                    | Write Only              | 0xFFFFFFFF | YES        | Customer Chip Global Key Word 1             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 114   | OTP_CCGK_2                    | Write Only              | 0xFFFFFFFF | YES        | Customer Chip Global Key Word 2             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 115   | OTP_CCGK_3                    | Write Only              | 0xFFFFFFFF | YES        | Customer Chip Global Key Word 3             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 116   | OTP_CCGK_4                    | Write Only              | 0xFFFFFFFF | YES        | Customer Chip Global Key Word 4             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 117   | OTP_CCGK_5                    | Write Only              | 0xFFFFFFFF | YES        | Customer Chip Global Key Word 5             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 118   | OTP_CCGK_6                    | Write Only              | 0xFFFFFFFF | YES        | Customer Chip Global Key Word 6             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 119   | OTP_CCGK_7                    | Write Only              | 0xFFFFFFFF | YES        | Customer Chip Global Key Word 7             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 120   | OTP_CCUK_0                    | Write Only              | 0xFFFFFFFF | NO         | Customer Chip Unique Key Word 0  (256-bit)  |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 121   | OTP_CCUK_1                    | Write Only              | 0xFFFFFFFF | NO         | Customer Chip Unique Key Word 1             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 122   | OTP_CCUK_2                    | Write Only              | 0xFFFFFFFF | NO         | Customer Chip Unique Key Word 2             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 123   | OTP_CCUK_3                    | Write Only              | 0xFFFFFFFF | NO         | Customer Chip Unique Key Word 3             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 124   | OTP_CCUK_4                    | Write Only              | 0xFFFFFFFF | NO         | Customer Chip Unique Key Word 4             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 125   | OTP_CCUK_5                    | Write Only              | 0xFFFFFFFF | NO         | Customer Chip Unique Key Word 5             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 126   | OTP_CCUK_6                    | Write Only              | 0xFFFFFFFF | NO         | Customer Chip Unique Key Word 6             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 127   | OTP_CCUK_7                    | Write Only              | 0xFFFFFFFF | NO         | Customer Chip Unique Key Word 7             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 128   | OTP_CCUK_ID_0                 | Read / Write            | 0xFFFFFFFF | NO         | Customer Chip Unique Key ID Word 0 (64-bit) |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 129   | OTP_CCUK_ID_1                 | Read / Write            | 0xFFFFFFFF | NO         | Customer Chip Unique Key ID Word 1          |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 131   | OTP_OEM_IMAGE_SECURE_BOOT_EN  | Read / Write            | 0xFFFFFFFF | NO         | Enable OEM Image Secure Boot                |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 135   | OTP_OEM_SEGID                 | Read / Write            | 0xFFFFFFFF | YES        | OEM segmentation ID                         |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 145   | OTP_OEM_IMAGE_VERSION         | Read / Write            | 0xFFFFFFFF | NO         | OEM image version                           |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 556   | OTP_SOC_UID_0                 | Read Only               | 0xFFFFFFFF | NO         | SoC Unique ID Word 0                        |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 557   | OTP_SOC_UID_1                 | Read Only               | 0xFFFFFFFF | NO         | SoC Unique ID Word 1                        |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 558   | OTP_SOC_UID_2                 | Read Only               | 0xFFFFFFFF | NO         | SoC Unique ID Word 2                        |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 559   | OTP_SOC_UID_3                 | Read Only               | 0xFFFFFFFF | NO         | SoC Unique ID Word 3                        |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 577   | OTP_MAC_ADDRESS_0             | Read / Write            | 0xFFFFFFFF | NO         | MAC address                                 |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 578   | OTP_MAC_ADDRESS_1             | Read / Write            | 0xFFFFFFFF | NO         | MAC address                                 |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+

Notes:

  1. OTP_OEM_IMAGE_SECURE_BOOT_EN:
      This field controls the OEM image secure boot feature. The default value is
      0x00000000, which means that OEM secure boot is disabled.

      The valid configuration values are:

      * ``0x00000000`` -- Secure boot is disabled.
      * ``0x00010001`` -- Secure boot is enabled in development mode.
      * ``0x10011001`` -- Secure boot is enabled in production mode.

      The image production flag policy is defined as follows:

      * When OTP_OEM_IMAGE_SECURE_BOOT_EN is set to ``0x00010001``
        (development mode), the device allows images with
        ``Image_production_flag`` set to either 0 or 1 to boot.

      * When OTP_OEM_IMAGE_SECURE_BOOT_EN is set to ``0x10011001``
        (production mode), the device allows only images with
        ``Image_production_flag`` set to ``1`` to boot.

      During image signing, the user can select the ``Image_production_flag``
      according to the intended image type:

      * Image_production_flag = 0 -- Development image.
      * Image_production_flag = 1 -- Production image.

      During secure boot, the device checks the ``Image_production_flag`` in
      the image header against the configured OTP_OEM_IMAGE_SECURE_BOOT_EN policy to determine
      whether the image is allowed to boot.

  2. OTP_SYNA_IMAGE_SECURE_BOOT_EN:
      This field controls the Syna image secure boot feature. In Astra chips before shipping,
      It is enabled by default. So the official release of Astra preboot images are built with
      security features enabled. In general, customers do not need to change this value.

      The valid configuration values are:

      * ``0x00000000`` -- Syna secure boot is disabled.
      * ``0x10011001`` -- Syna secure boot is enabled.

  3. OTP_JTAG_ACCESS_CONTROL:
      This field controls JTAG access for the M52 and A55 domains.

      For safety and integrity checking, the 32-bit field contains two identical
      16-bit copies:

      * Bits ``[15:0]``  -- Primary JTAG access control value
      * Bits ``[31:16]`` -- Duplicate of bits ``[15:0]``

      Bits ``[31:16]`` must have the same value as bits ``[15:0]``. A mismatch
      between the primary and duplicate fields indicates an invalid or corrupted
      configuration.

      The default value is ``0x00000000``, which means that JTAG access is
      open (enabled) for all domains.

      The bit definitions are as follows:

      +----------+---------------+------------------------------------------+
      | Bits     | Field         | Description                              |
      +==========+===============+==========================================+
      | [1:0]    | M52_SEC       | M52 Secure JTAG access control           |
      +----------+---------------+------------------------------------------+
      | [3:2]    | A55_SEC       | A55 Secure JTAG access control           |
      +----------+---------------+------------------------------------------+
      | [5:4]    | M52_NS        | M52 Non-Secure JTAG access control       |
      +----------+---------------+------------------------------------------+
      | [7:6]    | A55_NS        | A55 Non-Secure JTAG access control       |
      +----------+---------------+------------------------------------------+
      | [15:8]   | Reserved      | Reserved                                 |
      +----------+---------------+------------------------------------------+
      | [17:16]  | M52_SEC_dup   | Duplicate of M52_SEC                     |
      +----------+---------------+------------------------------------------+
      | [19:18]  | A55_SEC_dup   | Duplicate of A55_SEC                     |
      +----------+---------------+------------------------------------------+
      | [21:20]  | M52_NS_dup    | Duplicate of M52_NS                      |
      +----------+---------------+------------------------------------------+
      | [23:22]  | A55_NS_dup    | Duplicate of A55_NS                      |
      +----------+---------------+------------------------------------------+
      | [31:24]  | Reserved      | Reserved                                 |
      +----------+---------------+------------------------------------------+

      Each 2-bit JTAG access control field uses the following policy:

      +----------+--------------------------+
      | Value    | JTAG Access Policy       |
      +==========+==========================+
      | 2'b00    | Open                     |
      +----------+--------------------------+
      | 2'b01    | Certificate-controlled   |
      +----------+--------------------------+
      | 2'b1x    | Closed                   |
      +----------+--------------------------+

      The access policy is applied independently to each JTAG domain.

      For example:

      * ``M52_SEC = 2'b00`` means M52 Secure JTAG access is open.
      * ``M52_SEC = 2'b01`` means M52 Secure JTAG access is controlled by
        certificate authentication.
      * ``M52_SEC = 2'b10`` or ``2'b11`` means M52 Secure JTAG access is closed.

      The same policy applies to ``A55_SEC``, ``M52_NS``, and ``A55_NS``.

      When programming ``OTP_JTAG_ACCESS_CONTROL``, the lower 16-bit value must
      also be duplicated into the upper 16 bits.

      The 32-bit value shall therefore follow the format::

          OTP_JTAG_ACCESS_CONTROL[31:16] =
              OTP_JTAG_ACCESS_CONTROL[15:0]

      For example, if the primary configuration is::

          OTP_JTAG_ACCESS_CONTROL[15:0] = 0x0055

      then the complete 32-bit value must be::

          OTP_JTAG_ACCESS_CONTROL = 0x00550055

      Similarly, the default configuration is::

          OTP_JTAG_ACCESS_CONTROL[15:0]  = 0x0000
          OTP_JTAG_ACCESS_CONTROL[31:16] = 0x0000
          OTP_JTAG_ACCESS_CONTROL        = 0x00000000

      A valid programmed value must satisfy the following condition::

          OTP_JTAG_ACCESS_CONTROL[31:16] ==
              OTP_JTAG_ACCESS_CONTROL[15:0]

   4. OTP_CCUK_ID_0 and OTP_CCUK_ID_1:
       These two fields are used to store a 64-bit Customer Chip Unique Key ID. The CCUK ID is an optional field that
       can be used to associate the CCUK. It does not affect the functionality of the CCUK itself.
       Please program the OTP_CCUK_ID_0 and OTP_CCUK_ID_1 in the same session as it's a 64-bit value
       spanning across two 32-bit fields.

   5. OTP_OEM_IMAGE_VERSION:
       This field is used to store a version number for the CCGK derived images (i.e., tzk, bl, firmware, boot, fastlogo)
       to implement anti-rollback mechanisms. Supported OEM image version range is 0~31. Default value is 0. User can choose to
       increase the version number when there's a need to prevent older OEM image from booting.

   6. OTP_SOC_UID_0-3:
       The OTP_SOC_UID_0-3 fields collectively store the 128-bit unique ID.
       Each field contains a 32-bit word of the 128-bit unique ID. These
       fields are programmed by Synaptics before the chips are shipped to customers.

   7. OTP_MAC_ADDRESS_0 and OTP_MAC_ADDRESS_1:
       These fields are used to store the 48-bit Ethernet MAC address in OTP.
       The MAC address is divided into two 32-bit OTP fields:

       +---------------------+-----------+----------------------------------+
       | OTP Field           | OTP Index | MAC Address Data                 |
       +=====================+===========+==================================+
       | OTP_MAC_ADDRESS_0   | 577       | Lower 32 bits of the MAC address |
       +---------------------+-----------+----------------------------------+
       | OTP_MAC_ADDRESS_1   | 578       | Upper 16 bits of the MAC address |
       +---------------------+-----------+----------------------------------+

       For example, given the following Ethernet MAC address::

       ether = 56:E5:F7:CB:FE:E3

       The six MAC address bytes are::

           56 E5 F7 CB FE E3
           |     |          |
           |     +----------+-- OTP_MAC_ADDRESS_0
           +------------------- OTP_MAC_ADDRESS_1

       The MAC address is programmed into the OTP fields as follows:

       * ``OTP_MAC_ADDRESS_0`` contains the lower four bytes
         ``F7:CB:FE:E3``, resulting in the 32-bit value ``0xF7CBFEE3``.

       * ``OTP_MAC_ADDRESS_1`` contains the upper two bytes
         ``56:E5`` in bits ``[15:0]``, resulting in the 32-bit value
         ``0x000056E5``. Bits ``[31:16]`` are unused and should be set to zero.

       The corresponding OTP programming commands are::

           otpwrite 577 0xf7cbfee3 0xffffffff
           otpwrite 578 0x000056e5 0xffffffff

       Therefore, the MAC address mapping is::

           MAC Address:  56:E5:F7:CB:FE:E3

                  +---------+-------------+
                  |  56 E5  | F7 CB FE E3 |
                  +---------+-------------+
                       |            |
                       v            v
                  OTP 578       OTP 577
                  0x000056E5    0xF7CBFEE3

       After programming, the two OTP fields together represent the original
       48-bit Ethernet MAC address ``56:E5:F7:CB:FE:E3``.



U-BOOT OTP Commands
====================================================================

otpread
------------------------------------------------------------

Usage:
   ::

    otpread <otp_index>
    otpread   577
    otpread   578

Return Codes:
   ::

    0x00000000 : Success
    0xFF000001 : STATUS_FAILURE
    0xFF000050 : STATUS_OTP_INVALID_IDX
    0xFF000052 : STATUS_OTP_ERROR_WRITEONLY_FIELD

Examples:
   ::

      => otpread 577
      otp operation succeed
      read otp[577] data=0xf7cbfee3

      => otpread 578
      otp operation succeed
      read otp[578] data=0x000056e5

If a write-only field is read:

Return Code:
    0xFF000052 : STATUS_OTP_ERROR_WRITEONLY_FIELD

Returned Data:
    0xDEADBEAF   (INVALID DUMMY DATA)

Examples:
   ::

    => otpread 112
    otp operation failed
    read otp[112] data=0xdeadbeaf

otpwrite
------------------------------------------------------------

Usage:
   ::

    otpwrite <otp_index> <data> <mask>

    otpwrite   577 0xf7cbfee3 0xFFFFFFFF
    otpwrite   578 0x000056e5 0xFFFFFFFF

Return Codes:
   ::

     0x00000000 : Success
     0xFF000001 : STATUS_FAILURE
     0xFF000050 : STATUS_OTP_INVALID_IDX
     0xFF000051 : STATUS_OTP_ERROR_READONLY_FIELD

Examples:
   ::

      => otpwrite 577 0xf7cbfee3 0xFFFFFFFF
      otp operation succeed

      => otpwrite 578 0x000056e5 0xFFFFFFFF
      otp operation succeed


Tools to generate OTP commands
====================================================================

It is strongly recommended to use the helper script gen_otp_command.py to generate OTP programming
commands instead of writing them by hand.

The tool can be found under `Factory repository <https://github.com/synaptics-astra/factory/tree/#release#>`__ at
``factory/scripts/[klamath]``. Where ``klamath``: SL26xx

Examples: (Klamath: SL26xx)
   ::

        $sdk/factory/scripts/klamath$ ./gen_otp_command.py


When the command completes, following file will be generated in the current directory:

    - otp_commands_uboot.txt:  U-Boot otpwrite commands

The script performs the following:

    - Reads OTP configuration from
        - configs/oem_config.conf
        - keys/AES_CCGK.bin
        - keys/generic/oem/K0_OEM.EC551.pub.pem

A sample configs/oem_config.conf configuration file is shown below

::

        ### OEM Configuration File
        ### This file contains default settings for OTP programming during manufacturing.
        ### Modify the parameters as needed for your specific OEM requirements.
        ### Items commented out are optional and can be enabled if required.

        [Chip Info]
        chip_name = klamath
        chip_rev = A0

        [Segmentation ID]
        oem_segid = 0x4F4C4548

        [Version]
        oem_version = 0

        [Image Production Flag]
        Image_production_flag = 1

        [OTP_OEM_IMAGE_SECURE_BOOT_EN]
        oem_security_enable = 0x10011001

        [OTP_OEM_IMAGE_VERSION]
        oem_image_version = 0

        [OTP_JTAG_ACCESS_CONTROL]
        jtag_access_control = 0x00000000

Below is a sample execution log:

   ::

    $sdk/factory/scripts/klamath/factory$ ./gen_otp_command.py
    [SKIP] OTP_REE_VERSION is zero; command not generated.
    [SKIP] OTP_JTAG_ACCESS_CONTROL is zero; command not generated.
    otpwrite 80 0x92dc58d7 0xffffffff [Atomic]
    otpwrite 81 0x81a0c5cc 0xffffffff [Atomic]
    otpwrite 82 0x7b4b0fae 0xffffffff [Atomic]
    otpwrite 83 0x9dac32a9 0xffffffff [Atomic]
    otpwrite 84 0xd4a4ea7e 0xffffffff [Atomic]
    otpwrite 85 0x83596267 0xffffffff [Atomic]
    otpwrite 86 0xadb93b00 0xffffffff [Atomic]
    otpwrite 87 0x753ac64c 0xffffffff [Atomic]
    otpwrite 88 0x2c2f2c42 0xffffffff [Atomic]
    otpwrite 89 0xf1bee7aa 0xffffffff [Atomic]
    otpwrite 90 0xbb063fe1 0xffffffff [Atomic]
    otpwrite 91 0x56cbb296 0xffffffff [Atomic]
    otpwrite 92 0x4c6c5b6d 0xffffffff [Atomic]
    otpwrite 93 0xcbca7c34 0xffffffff [Atomic]
    otpwrite 94 0x8977cb87 0xffffffff [Atomic]
    otpwrite 95 0xa661193e 0xffffffff [Atomic]
    otpwrite 112 0x1869752d 0xffffffff [Atomic]
    otpwrite 113 0x6f143de3 0xffffffff [Atomic]
    otpwrite 114 0x54884e23 0xffffffff [Atomic]
    otpwrite 115 0x316736ee 0xffffffff [Atomic]
    otpwrite 116 0x91cbcdad 0xffffffff [Atomic]
    otpwrite 117 0xaff45729 0xffffffff [Atomic]
    otpwrite 118 0x798ebbe7 0xffffffff [Atomic]
    otpwrite 119 0x18438e6f 0xffffffff [Atomic]
    otpwrite 131 0x10011001 0xffffffff
    otpwrite 135 0x4f4c4548 0xffffffff
    [OK] Wrote 26 commands to otp_commands_uboot.txt

Notes:

    - otp_commands_uboot.txt contains commands in the form to perform in u-boot:
          otpwrite <idx> <value> <mask>
