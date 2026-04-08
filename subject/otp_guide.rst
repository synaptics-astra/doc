=========================================================================
 OTP Access Utility Guide
=========================================================================

.. contents::
   :depth: 3

Introduction
====================================================================

This document describes the usage of the OTP access utilities in:

  - U-Boot environment      : otpread / otpwrite
  - Linux TA/CA environment: factory_util 6 otpread / otpwrite

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
| 0-31  | OTP_USER_DATA_0 ~ 31          | Read / Write            | 0xFFFFFFFF | NO         | User Data                                   |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 100   | OTP_K0_OEM_HASH_0             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 0 (256-bit)   |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 101   | OTP_K0_OEM_HASH_1             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 1             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 102   | OTP_K0_OEM_HASH_2             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 2             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 103   | OTP_K0_OEM_HASH_3             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 3             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 104   | OTP_K0_OEM_HASH_4             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 4             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 105   | OTP_K0_OEM_HASH_5             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 5             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 106   | OTP_K0_OEM_HASH_6             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 6             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 107   | OTP_K0_OEM_HASH_7             | Read / Write            | 0xFFFFFFFF | YES        | OEM Root Public Key Hash word 7             |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 108   | OTP_AESK0_0                   | Write Only              | 0xFFFFFFFF | YES        | AES Root Key K0 word 0 (0-3 total 128-bit)  |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 109   | OTP_AESK0_1                   | Write Only              | 0xFFFFFFFF | YES        | AES Root Key K0 word 1                      |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 110   | OTP_AESK0_2                   | Write Only              | 0xFFFFFFFF | YES        | AES Root Key K0 word 2                      |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 111   | OTP_AESK0_3                   | Write Only              | 0xFFFFFFFF | YES        | AES Root Key K0 word 3                      |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 112   | OTP_REE_SEGID                 | Read / Write            | 0xFFFFFFFF | YES        | 32-bit REE segmentation ID                  |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 113   | OTP_REE_SECURITY_ENABLE       | Read / Write            | 0x00000001 | YES        | 1 = Enable REE security                     |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 114   | OTP_BOOT_SECURITY_ENABLE      | Read / Write            | 0x00000001 | NO         | 1 = Enable Secure Boot                      |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 115   | OTP_MP_PROVISION_DONE         | Read / Write            | 0x00000001 | NO         | 1 = Factory provisioning complete           |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 116   | OTP_SCS_AREA_SIZE_SEL         | Read / Write            | 0x00000003 | NO         | 2-bit Secure Code Storage size select       |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 117   | OTP_REE_JTAG_PROTECTION_POLICY| Read / Write            | 0x00000003 | NO         | 2-bit JTAG access policy                    |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 118   | OTP_REE_VERSION               | Read / Write            | 0x0000003F | NO         | 6-bit REE version                           |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 119   | OTP_RKEK_ID_0                 | Read / Write            | 0xFFFFFFFF | NO         | Word 0 (32-bit) of 64-bit RKEK_ID           |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 120   | OTP_RKEK_ID_1                 | Read / Write            | 0xFFFFFFFF | NO         | Word 1 (32-bit) of 64-bit RKEK_ID           |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 200   | OTP_EMMC_BOOT_DISABLE         | Read / Write            | 0x00000001 | NO         | 1 = Disable eMMC boot                       |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 201   | OTP_SPI_BOOT_DISABLE          | Read / Write            | 0x00000001 | NO         | 1 = Disable SPI boot                        |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 202   | OTP_DOLBY_AUDIO_DISABLE       | Read Only               | 0x00000001 | NO         | 1 = Disable Dolby Audio                     |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 203   | OTP_OEM_AUDIO_CUSTOMER_ID     | Write Only              | 0xFFFFFFFF | NO         | 32-bit OEM Audio Customer ID                |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 204   | OTP_PRODUCTION_CHIP_FLAG      | Read / Write            | 0x00000007 | NO         | 3-bit 0:Development chip 7: Production Chip |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 205   | OTP_USB_BOOT_DISABLE          | Read / Write            | 0x00000001 | NO         | 1 = Disable USB boot                        |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 206   | OTP_BOOT_VERSION              | Read / Write            | 0x0000003F | NO         | 6-bit BOOT version                          |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 207   | OTP_SOC_UID_0                 | Read Only               | 0xFFFFFFFF | NO         | Word 0 (32-bit) of 64-bit SOC_UID           |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 208   | OTP_SOC_UID_1                 | Read Only               | 0xFFFFFFFF | NO         | Word 1 (32-bit) of 64-bit SOC_UID           |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+
| 209   | OTP_FIELD_MAX                 | N/A                     | N/A        | N/A        | Enum boundary only                          |
+-------+-------------------------------+-------------------------+------------+------------+---------------------------------------------+

Notes:

  1. OTP_USER_DATA_0 ~ 31:
      This field is provided for user data storage. It supports per-bit masking programming.

  2. OTP_MP_PROVISION_DONE:
      Set this field to 1 means all the MP provision are completed. There's no restriction for otpread/otpwrite
      to distinguish this field to do anything different. But it would be a good indicator for
      provision are all complete if set OTP_MP_PROVISION_DONE = 1.  It's up to user to use this field
      if using otpread/otpwrite to do fusing stuff.

  3. OTP_SCS_AREA_SIZE_SEL:
      - 0x0 : 385K (default)

  4. OTP_REE_JTAG_PROTECTION_POLICY:
      - 0x0 : JTAG always enabled
      - 0x1 : JTAG password protected
      - 0x2 : JTAG always disabled
      - 0x3 : JTAG always disabled

  5. OTP_PRODUCTION_CHIP_FLAG:
      - 0x0 : Development chip. Both development and production image can run on this chip.
      - 0x7 : Production chip. Only production image can run on this chip.

      Notes:
      Basically, only production chips are shipped to customers. This field can be used to
      prevent development images from running on production chips.

  6. OTP_OEM_AUDIO_CUSTOMER_ID:
      This field is used to store a 32-bit customer ID for Dolby Audio feature customization.

  7. OTP_BOOT_SECURITY_ENABLE:
      This field by default is enabled in Astra chips before shipping to customers.

  8. OTP_RKEK_ID_0 and OTP_RKEK_ID_1:
      These two fields are used to store a 64-bit RKEK ID. The RKEK ID is an optional field that
      can be used to associate the RKEK. It does not affect the functionality of the RKEK itself.
      Please program the OTP_RKEK_ID_0 and OTP_RKEK_ID_1 in the same session as it's a 64-bit value
      spanning across two 32-bit fields.

  9. OTP_REE_VERSION:
      This field is used to store a version number for the K0_REE derived images (i.e., tzk, bl, firmware, boot, fastlogo)
      to implement anti-rollback mechanisms. Supported REE version range is 0~31. Default value is 0. User can choose to
      increase the version number when there's a need to prevent older REE image from booting.

  10. OTP_BOOT_VERSION:
       This field is used to store a version number for K0_SYNA_ROOT_KEY derived images to implement anti-rollback mechanisms.
       Supported boot version range is 0~31. The affected images are signed and owned by Synaptics. Any update of these
       image would require a new preboot image release from Synaptics. Please keep the boot version unchanged (default 0)
       except for getting confirmation from Synaptics.

  11. OTP_SOC_UID_0 and OTP_SOC_UID_1:
       These two fields are used to store a 64-bit SOC_UID. The field is programmed by Synaptics during manufacturing
       and cannot be modified by users. This SOC_UID is a read-only field that is unique for each chip and can be used
       for chip identification purposes.


U-BOOT OTP Commands
====================================================================

otpread
------------------------------------------------------------

Usage:
   ::

    otpread <otp_index>
    otpread   0
    otpread   1

Return Codes:
   ::

    0x00000000 : Success
    0xFF000001 : STATUS_FAILURE
    0xFF000050 : STATUS_OTP_INVALID_IDX
    0xFF000052 : STATUS_OTP_ERROR_WRITEONLY_FIELD


otpwrite
------------------------------------------------------------

Usage:
   ::

    otpwrite <otp_index> <data> <mask>

    otpwrite   1 0x500 0xFFF
    otpwrite   2 0x1A2B3C4D 0xFFFFFFFF
    otpwrite   3 0x1A2B0000 0xFFFF0000
    otpwrite   4 0x00010000 0x00010000

Return Codes:
   ::

     0x00000000 : Success
     0xFF000001 : STATUS_FAILURE
     0xFF000050 : STATUS_OTP_INVALID_IDX
     0xFF000051 : STATUS_OTP_ERROR_READONLY_FIELD

Examples:
   ::

      => otpread 0
      otp operation succeed
      read otp[0] data=0x0000beaf, mask=0xffffffff
      => otpread 1
      otp operation succeed
      read otp[1] data=0xbeafbeaf, mask=0xbeafffff
      => otpread 2
      otp operation succeed
      read otp[2] data=0x0000beaf, mask=0x0000ffff

      => otpread 100
      otp operation failed
      do_otp_read: ret = 0xff000052
      read otp[100] data=0xdeadbeaf, mask=0xffffffff


Linux TA/CA OTP Commands
====================================================================

factory_util 6 otpread
------------------------------------------------------------

Usage:
   ::

    factory_util 6 otpread  <otp_index>
    factory_util 6 otpread    0
    factory_util 6 otpread    1



Return Codes:
   ::

        0x00000000 : Success
        0xFF000001 : STATUS_FAILURE
        0xFF000050 : STATUS_OTP_INVALID_IDX
        0xFF000052 : STATUS_OTP_ERROR_WRITEONLY_FIELD



factory_util 6 otpwrite
------------------------------------------------------------

Usage:
   ::

    factory_util 6 otpwrite <otp_index> <data> <mask>
    factory_util 6 otpwrite 1 0x500      0xFFF
    factory_util 6 otpwrite 2 0x1A2B3C4D 0xFFFFFFFF
    factory_util 6 otpwrite 3 0x1A2B0000 0xFFFF0000
    factory_util 6 otpwrite 4 0x00010000 0x00010000

Return Codes:
   ::

        0x00000000 : Success
        0xFF000001 : STATUS_FAILURE
        0xFF000050 : STATUS_OTP_INVALID_IDX
        0xFF000051 : STATUS_OTP_ERROR_READONLY_FIELD


Examples:
   ::

      root@sl1640:~# factory_util 6 otpread 0
      D/TA:   __GP11_TA_InvokeCommandEntryPoint:82 CommandID = 0xe00c
      _otp_read: idx=0, val=0x0000BEAF, mask=0xFFFFFFFF
      OTP[0] = 0x0000BEAF, mask=0xFFFFFFFF

      root@sl1640:~# factory_util 6 otpread 1
      D/TA:   __GP11_TA_InvokeCommandEntryPoint:82 CommandID = 0xe00c
      _otp_read: idx=1, val=0xBEAFBEAF, mask=0xBEAFFFFF
      OTP[1] = 0xBEAFBEAF, mask=0xBEAFFFFF

      root@sl1640:~# factory_util 6 otpread 100
      D/TA:   __GP11_TA_InvokeCommandEntryPoint:82 CommandID = 0xe00c
      _otp_read:744: Invoke failed, res=0xff000052 origin=4
      _otp_read: idx=100, val=0xDEADBEAF, mask=0xFFFFFFFF
      otpread failed for index 100 (status=1)

.. note::

  By default, the factory utilities are installed in astra-media images. If
  not present, can add the package by adding below line to conf/local.conf
  and build image.

    IMAGE_INSTALL:append = " synasdk-factory-ta synasdk-drm-factory-ca-program"

  Once package is installed, should find below ta and factory utilities in the target device:
    - /usr/lib/optee_armtz/1316a183-894d-43fe-9893-bb946ae10420.ta
    - /usr/bin/factory_util

Common OTP Index List
====================================================================

  =====  ============================
  Idx    Name
  =====  ============================
   0        OTP_USER_DATA_0
   1        OTP_USER_DATA_1
   :         :
   31       OTP_USER_DATA_31
   100      OTP_K0_OEM_HASH_0
   101      OTP_K0_OEM_HASH_1
   102      OTP_K0_OEM_HASH_2
   103      OTP_K0_OEM_HASH_3
   104      OTP_K0_OEM_HASH_4
   105      OTP_K0_OEM_HASH_5
   106      OTP_K0_OEM_HASH_6
   107      OTP_K0_OEM_HASH_7
   108      OTP_AESK0_0
   109      OTP_AESK0_1
   110      OTP_AESK0_2
   111      OTP_AESK0_3
   112      OTP_REE_SEGID
   113      OTP_REE_SECURITY_ENABLE
   114      OTP_BOOT_SECURITY_ENABLE
   115      OTP_MP_PROVISION_DONE
   116      OTP_SCS_AREA_SIZE_SEL
   117      OTP_REE_JTAG_PROTECTION_POLICY
   118      OTP_REE_VERSION
   119      OTP_RKEK_ID_0
   120      OTP_RKEK_ID_1
   200      OTP_EMMC_BOOT_DISABLE
   201      OTP_SPI_BOOT_DISABLE
   202      OTP_DOLBY_AUDIO_DISABLE
   203      OTP_OEM_AUDIO_CUSTOMER_ID
   204      OTP_PRODUCTION_CHIP_FLAG
   205      OTP_USB_BOOT_DISABLE
   206      OTP_BOOT_VERSION
   207      OTP_FIELD_MAX

  =====  ============================


Important Programming Rules
====================================================================

Except for OTP_USER_DATA_0-31 which supports per-bits fusing access, for other fields, please follow
below mask guideline:

1. 1-bit fields must use mask = 0x00000001
2. 2-bit fields must use mask = 0x00000003
3. 3-bit fields must use mask = 0x00000007
4. 32-bit fields must use mask = 0xFFFFFFFF


WRITE-ONLY OTP Field Readback Behavior
====================================================================

If a write-only field is read:

Return Code:
    0xFF000052 : STATUS_OTP_ERROR_WRITEONLY_FIELD

Returned Data:
    0xDEADBEAF   (INVALID DUMMY DATA)

Returned Mask:
    VALID. Mask would reflect whether the OTP field is programmed.
    0x0 = not programmed; 0xFFFFFFFF = fully programmed.

Examples:
   ::

      root@sl1640:~# factory_util 6 otpread 100
      _otp_read:744: Invoke failed, res=0xff000052 origin=4
      _otp_read: idx=100, val=0xDEADBEAF, mask=0xFFFFFFFF
      otpread failed for index 100 (status=1)

If the mask=0xFFFFFFFF, which means all the 32-bits of the field are all programmed.

OTP_USER_DATA_0~31 Mask Usage
====================================================================

    - Write of OTP_USER_DATA_0~31 would only program bits set in the mask. Bits not set
      in the mask would remain unchanged.
    - If the mask specifies bits already programmed, those bits would be ignored
      and not cause error.
    - Supports:
       - Per-bit masking
       - Per-n-bit masking
       - Full 32-bit masking

Examples:
   ::

      # Per-bit masking examples
      => otpwrite 0 0x00000001 0x00000001
      => otpwrite 0 0x000000F0 0x000000F0
      => otpwrite 0 0xA5A5A5A5 0xFFFFFFFF

      # Bit masking examples
      # Preexisting otp[5] = 0x0000000a,     mask=0x0000000f
      # Write       otp[5]   0x000000a7      mask=0x000000ff
      # Final       otp[5] = 0x000000aa,     mask=0x000000ff
      => otpwrite 5 0xA 0xF
      otp operation succeed
      => otpread 5
      otp operation succeed
      read otp[5] data=0x0000000a, mask=0x0000000f
      => otpwrite 5 0xa7 0xff
      otp operation succeed
      => otpread 5
      otp operation succeed
      read otp[5] data=0x000000aa, mask=0x000000ff


.. _Atomic_Programming_Rules:

Atomic Programming Rules
====================================================================

Atomic group includes:

    - OTP_K0_OEM_HASH_0 ~ OTP_K0_OEM_HASH_7
    - OTP_AESK0_0 ~ OTP_AESK0_3
    - OTP_REE_SEGID
    - OTP_REE_SECURITY_ENABLE

Rules:

  1. ALL atomic items must be programmed in ONE SESSION. Once reboot or power loss, it would mean
     enter a new SESSION.
  2. NO reboot or power loss is allowed before completion.
  3. It is FORBIDDEN to program HASH/AESK0 and set OTP_REE_SECURITY_ENABLE = 0.
  4. Any violation may result in PERMANENT BRICK.

Notes:

  1. There's no constrain for the command sequence of atomic items inside the same SESSION.
  2. For none-atomic fields, there's no constrain to program in any SESSION.


Tools to generate OTP commands
====================================================================

It is strongly recommended to use the helper script gen_otp_command.py to generate OTP programming
commands instead of writing them by hand.

The tool can be found under `Factory repository <https://github.com/synaptics-astra/factory/tree/#release#>`__ at
``factory/scripts/[platypus/dolphin/myna2/]/factory``. ``platypus``: SL1640, ``dolphin``: SL1680, ``myna2``: SL1620.

Examples: (Platypus: SL1640)
   ::

        $sdk/factory/scripts/platypus/factory$ ./gen_otp_command.py

When the command completes, two files will be generated in the current directory:

    - otp_commands_uboot.txt:  U-Boot otpwrite commands
    - otp_commands_linux.txt:  Linux factory_util 6 otpwrite commands

The script performs the following:

    - Reads OTP configuration from
        - configs/oem_config.conf
        - keys/K0_REE_hash.bin
        - keys/AESK0.bin

    - Applies the mask rules described in this document

    - Enforces atomic programming rules for:
         - OTP_K0_OEM_HASH_0 ~ 7
         - OTP_AESK0_0 ~ 3
         - OTP_REE_SEGID
         - OTP_REE_SECURITY_ENABLE

    - Treats OTP_MP_PROVISION_DONE as a special case:
          - If its value is 0, the command is skipped and a
            [SKIP] message is printed
          - User can perform the OTP_MP_PROVISION_DONE = 1 command when
            ALL the OTP fields are done in the LAST production SESSION.

    - Tags atomic items in the debug output with [Atomic]

A sample configs/oem_config.conf configuration file is shown below

::

        ### This file contains default settings for OTP programming during manufacturing.
        ### Modify the parameters as needed for your specific OEM requirements.
        ### Items commented out are optional and can be enabled if required.

        [Segmentation ID]
        ree_segid = 0x2E32000A

        [Version]
        ree_version = 0

        [OTP_REE_SECURITY_ENABLE]
        ree_security_enable = 1

        [OTP_BOOT_SECURITY_ENABLE]
        #boot_security_enable = 1

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

        [OTP_USB_BOOT_DISABLE]
        usb_boot_disable = 0

        [OTP_OEM_AUDIO_CUSTOMER_ID]
        #oem_audio_customer_id = 0x00000000

        [OTP_PRODUCTION_CHIP_FLAG]
        #production_chip_flag = 7

        [OTP_BOOT_VERSION]
        #boot_version = 0

        [OTP_RKEK_ID_0]
        #rkek_id_0 = 0x1640abcd

        [OTP_RKEK_ID_1]
        #rkek_id_1 = 0x10001234


Below is a sample execution log:

   ::

    $sdk/factory/scripts/platypus/factory$ ./gen_otp_command.py
    [SKIP] OTP_MP_PROVISION_DONE value is 0, command not generated
    otpwrite 100 0xc4ddf49e 0xffffffff [Atomic]
    otpwrite 101 0xe0593948 0xffffffff [Atomic]
    otpwrite 102 0xde9b8638 0xffffffff [Atomic]
    otpwrite 103 0x81ace868 0xffffffff [Atomic]
    otpwrite 104 0x2a629998 0xffffffff [Atomic]
    otpwrite 105 0xd105297d 0xffffffff [Atomic]
    otpwrite 106 0x8559f683 0xffffffff [Atomic]
    otpwrite 107 0xd92484ee 0xffffffff [Atomic]
    otpwrite 108 0x60c500da 0xffffffff [Atomic]
    otpwrite 109 0x08625e40 0xffffffff [Atomic]
    otpwrite 110 0xf5c13936 0xffffffff [Atomic]
    otpwrite 111 0x908e3b76 0xffffffff [Atomic]
    otpwrite 112 0x00000000 0xffffffff [Atomic]
    otpwrite 113 0x00000001 0x00000001 [Atomic]
    otpwrite 116 0x00000000 0x00000003
    otpwrite 117 0x00000001 0x00000003
    otpwrite 200 0x00000000 0x00000001
    otpwrite 201 0x00000000 0x00000001
    otpwrite 205 0x00000000 0x00000001
    [OK] Wrote 19 lines to otp_commands_uboot.txt
    [OK] Wrote 19 lines to otp_commands_linux.txt

Notes:

    - Lines tagged with [Atomic] belong to the atomic security group and MUST be programmed as part
      of one provisioning session without reboot or power loss.

    - otp_commands_uboot.txt contains commands in the form to perform in u-boot:
          otpwrite <idx> <value> <mask>

    - otp_commands_linux.txt contains commands in the form to perform in Linux:
          factory_util 6 otpwrite <idx> <value> <mask>
