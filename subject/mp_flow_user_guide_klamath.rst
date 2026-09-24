===================================================
Astra MP Flow User Guide (Klamath: SL261x)
===================================================

.. contents::
   :depth: 3


Introduction
============

This guide describes the current Klamath manufacturing policy for generating
OEM key material, signing and optionally encrypting eMMC or USB production
images, retaining production records, and programming One-Time Programmable
Memory (OTP).

The key and image implementation is self-contained in this factory-tool
directory. It uses ECDSA P-521 signing keys and AES-256 CCGK-derived image
keys. The local tool ``genx_img_v3`` is the tool used by the flow to sign and
encrypt images. Unless stated otherwise, commands in this guide are run from
the directory containing this file.

System Requirements
===================

- Ubuntu 22.04 x86_64 desktop edition
- Python 3.10+
- A filesystem that preserves Linux owner/group/other permissions and
  symbolic links. The flow relies on modes ``600`` and ``700`` and on the
  ``keys`` symlink. Linux filesystems such as ext4 and XFS are suitable;
  FAT/exFAT or file shares that discard these attributes are not.

Definitions
===========

- ``syna-release SDK``: A software development kit from Synaptics used to build normal eMMC images and USB Boot
  Linux Image Packs.
- ``normal_eMMCimg``: Normal images are the ones without signature, no encryption and Production_Image_Flag = 0
- ``production_eMMCimg``: Factory output whose selected OEM images have
  production flags, signatures, and encryption applied.
- ``factory-tool directory``: The directory containing this guide, key
  lifecycle scripts, image tools, configuration, and keysets.
- ``CCGK``: The 256-bit root AES key used by the NIST SP800-108 AES-CMAC KDF.
- ``K0_OEM``: OEM root ECDSA P-521 key.
- ``K1_C``: ECDSA P-521 image-signing key signed by ``K0_OEM`` private key.
- ``OEM SegID``: OEM segmentation ID shared by key stores, images, and OTP settings.
- ``keyset``: One complete, versioned set of root, derived, signing, and store
  files under ``keysets``.
- ``production record``: External JSON metadata that links a production output
  to its keyset, configuration, tools, and file digests without storing secret
  key material.
- Mode ``600``: Only the file owner can read or modify the file.
- Mode ``700``: Only the directory owner can list, access, or modify its
  contents.

Pre-MP Preparation
==================

1. Configure Chip Information, OEM SegID, and Version
------------------------------------------------------

Update ``configs/oem_config.conf`` before generating any key store or
production image:

::

       [Chip Info]
       chip_name = klamath
       chip_rev = A0

       [Segmentation ID]
       oem_segid = 0x3015ffff

       [Version]
       oem_version = 0

       [Image Production Flag]
       Image_production_flag = 1

``oem_segid`` must be a 32-bit hexadecimal or decimal value.
``oem_version`` must be an integer from 0 through 32. Within this factory-tool
directory, these fields are the single source of truth for key stores and
signed images.
``Image_production_flag`` is the explicit image and key-derivation mode: ``0`` for
development material and images, or ``1`` for production material and images.
The configured value must match the device lifecycle and image policy. Do not
change any of these values after generating keys or images for a production
lot unless all affected derived keys, key stores, and images are regenerated
as described below.

The KDF context, output size, and per-image type values are data-only settings
in ``configs/key_derivation.conf``. They are not shell code. Changes require
review against the Klamath/ROM key-derivation specification and require
dependent encryption image keys to be rebuilt.

2. Configure the Image Encryption Policy
-----------------------------------------

``configs/encrypto_image.conf`` explicitly lists the image classes that must
be encrypted:

::

       encrypto_image_list = [
           "m52bl",
           "SM",
           "UBOOT",
           "OPTEE",
           "ATF",
           "Fastlogo",
           "Linux",
       ]

Supported names are case-sensitive:

- ``m52bl``: M52 bootloader contained in ``preboot.subimg``
- ``SM``: System Manager firmware
- ``UBOOT``: OEM bootloader
- ``ATF``: ATF component inside ``tzk.subimg``
- ``OPTEE``: OP-TEE and TEE boot parameter components inside ``tzk.subimg``
- ``Linux``: Linux kernel
- ``Fastlogo``: Fast logo image

An image listed in this policy must have its CCGK-derived AES key; otherwise
the flow stops. There is no silent fallback to unencrypted output. An image
deliberately omitted from the policy is signed without encryption and retains
a zero IV. A missing, empty, duplicate, or unknown policy entry is treated as
a configuration error.

3. Generate OEM Keys and Key Stores
-----------------------------------

For a new production keyset, run:

::

       $ ./gen_all_keys_stores.py

After the script completes, the active keyset contains the following keys and
stores.

Generated key directory layout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

       keys
       |-- AES_CCGK.bin
       |-- generic
       |   `-- oem
       |       |-- CCGK_ATF.bin
       |       |-- CCGK_BL.bin
       |       |-- CCGK_FAST_LOGO.bin
       |       |-- CCGK_LINUX.bin
       |       |-- CCGK_MODEL.bin
       |       |-- CCGK_NPU.bin
       |       |-- CCGK_OPTEE.bin
       |       |-- CCGK_OPTEE_CONTAINER_HEADER.bin
       |       |-- CCGK_SM.bin
       |       |-- CCGK_TEEBP.bin
       |       |-- CCGK_UBOOT.bin
       |       |-- K0_OEM.EC521.priv.pem
       |       |-- K0_OEM.EC521.pub.pem
       |       |-- K1_C.EC521.priv.pem
       |       `-- K1_C.EC521.pub.pem
       |-- keyset_manifest.json
       `-- store
           |-- K0_OEM_store_4k.bin
           `-- K1_C_store_4k.bin

The generated ``keyset_manifest.json`` records the chip name/revision, OEM
SegID, OEM version, and production flag used to generate that keyset. Before a
production-image run modifies any image, the tool compares those values with
the current ``configs/oem_config.conf`` and stops if any differ. After changing
one of these settings, rebuild the affected artifacts while preserving any
keys already bound to programmed OTP values.

Signing trust hierarchy
~~~~~~~~~~~~~~~~~~~~~~~

- ``keys/generic/oem/K0_OEM.EC521.priv.pem``: OEM root ECDSA P-521 private
  key. It signs/certifies the K1_C public-key store; it does not directly sign
  production images.
- ``keys/generic/oem/K0_OEM.EC521.pub.pem``: Public half of K0_OEM. It is
  packaged into the K0 OEM store and represents the OEM root of trust.
- ``keys/store/K0_OEM_store_4k.bin``: 4096-byte root key-store image holding
  the K0_OEM public-key information. It replaces the non-production K0 OEM in
  the K0 store inside ``preboot.subimg``.
- ``keys/generic/oem/K1_C.EC521.priv.pem``: ECDSA P-521 image-signing private
  key. It signs M52BL, System Manager, U-Boot, ATF, OP-TEE, TEE boot parameter,
  Linux, and Fastlogo images handled by the current factory flow.
- ``keys/generic/oem/K1_C.EC521.pub.pem``: Public half of K1_C. It is packaged
  into the K1_C store so the device can authenticate images signed by K1_C.
- ``keys/store/K1_C_store_4k.bin``: 4096-byte K1_C key-store image containing
  the K1_C public-key information, production flag, OEM SegID, and OEM version
  policy. The store is signed/certified using K0_OEM and replaces the
  non-production K1_C store in ``preboot.subimg`` and ``key.bin``.

Image-encryption hierarchy
~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``keys/AES_CCGK.bin``: 256-bit root AES key. It is KDF input material and is
  not used directly to encrypt a production image.
- ``keys/generic/oem/CCGK_BL.bin``: 256-bit derived AES key for encrypting
  M52BL, including M52BL inside ``preboot.subimg``.
- ``keys/generic/oem/CCGK_SM.bin``: 256-bit derived AES key for encrypting the
  System Manager firmware.
- ``keys/generic/oem/CCGK_ATF.bin``: 256-bit derived AES key for encrypting the
  ATF component inside ``tzk.subimg``.
- ``keys/generic/oem/CCGK_OPTEE.bin``: 256-bit derived AES key for encrypting
  the OP-TEE/TZ kernel component inside ``tzk.subimg``.
- ``keys/generic/oem/CCGK_TEEBP.bin``: 256-bit derived AES key for encrypting
  the TEE boot parameter component inside ``tzk.subimg``.
- ``keys/generic/oem/CCGK_UBOOT.bin``: 256-bit derived AES key for encrypting
  the OEM bootloader/U-Boot image.
- ``keys/generic/oem/CCGK_LINUX.bin``: 256-bit derived AES key for encrypting
  the Linux kernel image.
- ``keys/generic/oem/CCGK_FAST_LOGO.bin``: 256-bit derived AES key for
  encrypting the Fastlogo image.


All ``CCGK_<IMAGE>.bin`` files are independently derived from
``AES_CCGK.bin`` using NIST SP800-108 AES-CMAC. The derivation also binds the
configured context, image type, production flag, OEM SegID, and OEM version;
therefore changing any of these inputs changes the derived key.

Keyset metadata
~~~~~~~~~~~~~~~

- ``keys/keyset_manifest.json``: Non-secret metadata for the active keyset. It
  records the keyset ID, lifecycle action, KDF image types, configuration/tool
  digests, and public-key fingerprints. It never contains private-key or AES
  key values.

Each successful operation publishes a complete versioned directory under
``keysets`` and atomically switches the relative ``keys``
symlink to it.

The target of the ``keys`` symlink is the active keyset. Historical keysets
remain as versioned directories under ``keysets`` until they are archived or
removed according to the approved retention policy.

Private keys, AES keys, and CCGK-derived keys use mode ``600``. The keyset
directories contain secrets even though they are historical records. Protect
them like the active keys, define a retention and backup policy, and never
commit them to source control.

.. warning::

   Running the command without an action regenerates the complete keyset,
   including CCGK, K0 OEM, and K1_C. It is a rotation operation when a
   production keyset already exists. Back up and approve the current keyset
   before running it.

Available lifecycle commands are:

::

       # Regenerate the complete keyset.
       $ ./gen_all_keys_stores.py

       # Keep CCGK and rebuild all encryption image keys.
       $ ./gen_all_keys_stores.py rebuild-encryption-Image-keys

       # Keep K0 OEM and K1_C, and rebuild both key stores.
       $ ./gen_all_keys_stores.py rebuild-key-stores

       # Rotate CCGK and rebuild all encryption image keys. This can be done only before programming OTP CCGK
       $ ./gen_all_keys_stores.py rotate-CCGK

       # Rotate K0 OEM and rebuild the K0/K1 stores. This can be done only before programming OTP K0_OEM_Hash
       $ ./gen_all_keys_stores.py rotate-k0-oem

       # Rotate K1_C and rebuild the K1_C store.
       $ ./gen_all_keys_stores.py rotate-k1_c_ECC_pair

All candidates are validated before publication. AES keys must be 32 bytes,
stores must be 4096 bytes, ECC private/public pairs must match, and secret
permissions must not grant group or other access. A lifecycle lock prevents
concurrent key changes.

The KDF prints every derived AES image key to the console as required. Protect
terminal capture and manufacturing logs containing this output.

Do not manually edit files through the ``keys`` symlink. Doing so
changes a versioned keyset in place and makes ``keyset_manifest.json`` stale.
Use the lifecycle command matching the intended operation.

.. important:: Key immutability after OTP provisioning

   After the corresponding OTP values have been programmed into a Device
   Under Test (DUT), the following root and signing keys are fixed for that
   device and must not be rotated or replaced:

   - ``keys/AES_CCGK.bin``
   - ``keys/generic/oem/K0_OEM.EC521.priv.pem``
   - ``keys/generic/oem/K0_OEM.EC521.pub.pem``
   - ``keys/generic/oem/K1_C.EC521.priv.pem``
   - ``keys/generic/oem/K1_C.EC521.pub.pem``

   The private and public files of each ECDSA key pair are listed separately,
   but they form one key identity and must always remain matched. Replacing any
   fixed key produces artifacts that are incompatible with devices provisioned
   with the original OTP values. Back up and protect the complete production
   keyset before OTP provisioning.

.. note:: Effect of changing the production flag or OEM version

   ``Image_production_flag`` and ``oem_version`` are inputs to derived image
   keys and key-store generation. If either value changes, keep the following
   root and signing keys unchanged:

   - ``keys/AES_CCGK.bin``
   - ``keys/generic/oem/K0_OEM.EC521.priv.pem``
   - ``keys/generic/oem/K0_OEM.EC521.pub.pem``
   - ``keys/generic/oem/K1_C.EC521.priv.pem``
   - ``keys/generic/oem/K1_C.EC521.pub.pem``

   Regenerate all affected artifacts using the updated configuration:

   - Every ``keys/generic/oem/CCGK_<IMAGE>.bin`` derived image key
   - ``keys/store/K0_OEM_store_4k.bin``
   - ``keys/store/K1_C_store_4k.bin``

   Run both commands below to rebuild the affected artifacts while preserving
   ``AES_CCGK.bin``, K0 OEM, and K1_C:

   ::

          # Keep CCGK and rebuild all encryption image keys.
          $ ./gen_all_keys_stores.py rebuild-encryption-Image-keys

          # Keep K0 OEM and K1_C, and rebuild both key stores.
          $ ./gen_all_keys_stores.py rebuild-key-stores

   Complete both rebuild operations before generating a production image.
   Verify that the resulting ``keyset_manifest.json`` matches the updated
   ``configs/oem_config.conf``.

   Do not mix derived keys or key stores generated with different production
   flags or OEM versions in the same keyset or production image.


4. Generate a Production eMMC Image
-----------------------------------

a) Refer to the applicable SDK build guide and generate a clear normal eMMC
   image directory.
b) Verify ``configs/oem_config.conf``, ``configs/encrypto_image.conf``, and
   the active ``keys`` keyset before starting the factory flow. The flow
   rejects the run before signing if the active keyset manifest's chip name,
   chip revision, OEM SegID, OEM version, or production flag differs from
   ``oem_config.conf``.
c) Run the following command to generate the production eMMC image directory:

::

   $ ./gen_production_image.py emmc \
       <normal_eMMCimg> -o <production_eMMCimg>

The destination directory must not already exist. The flow reads only the
configuration, tools, and active keyset in this factory-tool directory. It
uses a private temporary key workspace and removes it automatically.

The active ``keys`` target must contain a valid ``keyset_manifest.json``.
A shared keyset lock keeps the active keyset stable for the complete image
run. If a key lifecycle operation is already running, image generation stops
and must be retried after the rotation completes.

eMMC image content changes:

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Image
     - Before factory flow
     - After factory flow
   * - K0 OEM store inside ``preboot.subimg.gz``
     - Non-production key-store value
     - Replaced with ``keys/store/K0_OEM_store_4k.bin``.
   * - K1_C store inside ``preboot.subimg.gz``
     - Non-production key-store value
     - Replaced with ``keys/store/K1_C_store_4k.bin``.
   * - M52BL inside ``preboot.subimg.gz``
     - Clear image with a zero IV
     - Signed by K1_C. When ``m52bl`` is selected, it is encrypted with
       ``CCGK_BL.bin``; otherwise it remains signed-only with a zero IV.
   * - ``bl.subimg.gz``
     - Clear U-Boot image with a zero IV
     - Signed by K1_C. When ``UBOOT`` is selected, it is encrypted with
       ``CCGK_UBOOT.bin``.
   * - ``sysmgr.subimg.gz``
     - Clear System Manager image with a zero IV
     - Signed by K1_C. When ``SM`` is selected, it is encrypted with
       ``CCGK_SM.bin``.
   * - ``tzk.subimg.gz``
     - Clear ATF, OP-TEE, and TEE boot parameter components with zero IVs
     - All components are signed by K1_C. When ``ATF`` is selected, it uses
       ``CCGK_ATF.bin``. When ``OPTEE`` is selected, it uses
       ``CCGK_OPTEE.bin`` and ``CCGK_TEEBP.bin``.
   * - ``boot.subimg.gz``
     - Clear Linux image with a zero IV
     - Signed by K1_C. When ``Linux`` is selected, it is encrypted with
       ``CCGK_LINUX.bin``.
   * - ``fastlogo.subimg.gz``
     - Clear Fastlogo image with a zero IV
     - Signed by K1_C. When ``Fastlogo`` is selected, it is encrypted with
       ``CCGK_FAST_LOGO.bin``.

Images omitted from the encryption policy are still signed when present. They
are not encrypted and retain a zero IV. Files in the source directory that
are not listed above are copied to the destination without image processing.

Input images must be clear. In the supported image-format header, an all-zero
16-byte IV means clear or signed-only, while a non-zero IV means encrypted.
The flow preflights every present image before the first signing operation.
If any input IV is non-zero, the tool reports ``already encrypted`` and stops
the entire run. TZK checks all three sub-image IVs.

When encryption is requested, the generated output must have a non-zero IV;
otherwise the run fails. A missing required key, image, signature, encryption,
size, or IV validation also fails closed. No partial output directory is
published.

5. Resign USB Boot Images
-------------------------

a) Obtain the clear USB Boot Linux Image Pack from the approved USB boot-tool
   release.
b) Verify ``configs/oem_config.conf``, ``configs/encrypto_image.conf``, and
   the active ``keys`` keyset.
c) Run the USB profile of the same production-image command:

::

   $ ./gen_production_image.py usb \
       <usb_tool/image_dir> -o <output_image_dir>

USB Boot Linux Image Pack content changes:

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Image
     - Before factory flow
     - After factory flow
   * - ``key.bin``
     - Non-production K0 OEM and K1_C key-store values
     - Updated with ``K0_OEM_store_4k.bin`` and ``K1_C_store_4k.bin``.
   * - ``m52bl.bin``
     - Clear image with a zero IV
     - Signed by K1_C. When ``m52bl`` is selected, it is encrypted with
       ``CCGK_BL.bin``; otherwise it remains signed-only with a zero IV.
   * - ``bl.subimg``
     - Clear U-Boot image with a zero IV
     - Signed by K1_C. When ``UBOOT`` is selected, it is encrypted with
       ``CCGK_UBOOT.bin``.
   * - ``sysmgr.subimg``
     - Clear System Manager image with a zero IV
     - Signed by K1_C. When ``SM`` is selected, it is encrypted with
       ``CCGK_SM.bin``.
   * - ``tzk.subimg``
     - Clear ATF, OP-TEE, and TEE boot parameter components with zero IVs
     - All components are signed by K1_C. When ``ATF`` is selected, it uses
       ``CCGK_ATF.bin``. When ``OPTEE`` is selected, it uses
       ``CCGK_OPTEE.bin`` and ``CCGK_TEEBP.bin``.

Other USB pack files are copied without image processing. The USB flow uses
the same configuration, active keyset, production record, temporary key
workspace, fail-closed behavior, and IV re-encryption guard as the eMMC flow.

6. Retain and Verify Production Records
---------------------------------------

Each successful eMMC or USB run creates an external record:

::

       production_records/
       `-- <UTC>-<profile>-<output-directory-name>/
           `-- production_manifest.json

For example:

::

       20260729T145027Z-emmc-production_eMMCimg

The output directory name is normalized to letters, digits, ``.``, ``_``, and
``-`` in the record ID. If an ID collides in the same second, an
eight-character suffix is appended. The record directory uses mode ``700``
and ``production_manifest.json`` uses mode ``600``.

The JSON records:

- production record ID, UTC creation time, profile, and successful status
- current keyset ID, keyset-manifest digest, and public-key fingerprints
- OEM values, encryption policy, and configuration/tool SHA-256 digests
- per-image input and output SHA-256 values
- signing handler, encryption request, and input-IV preflight result
- all output file SHA-256 values and a deterministic output-tree digest

It does not record AES/private-key contents, AES/private-key hashes, or
temporary key-workspace paths.

The published output also contains ``signed_image_info.txt``:

::

       schema_version=1
       production_record_id=20260729T145027Z-emmc-production_eMMCimg
       profile=emmc
       created_at_utc=2026-07-29T14:50:27+00:00

``schema_version`` identifies the production-record data format. It is not the
signed-image format, OEM version, or key version. ``signed_image_info.txt`` is a
minimal lookup pointer included in the output-tree digest; it is not a
separately signed file.

This version does not use an Audit key, so the JSON is not independently
tamper-evident. Copy ``production_records`` to access-controlled, backed-up or
append-only manufacturing storage. Do not place the full JSON inside the
signed-image output.

7. Generate OTP commands for production OTP Programming
------------------------------------------------------------

Use the helper script gen_otp_command.py to generate OTP programming commands instead of writing them by hand.

The tool can be found under `Factory repository <https://github.com/synaptics-astra/factory/tree/#release#>`__ at
``factory/scripts/[klamath]``. Where
``klamath``: SL26xx.

Update the ``factory/scripts/[klamath]/config/oem_config.conf`` settings as needed.
For OTP fields, please refer to :ref:`OTP_Field_Definitions_Table` for details.

.. warning::
    Remember **don't change oem_segid = 0x2E32000A (as example) in this step as it should be updated in step 1**.
    As keystores generated in step 2 are derived from the oem_segid(segmentation ID). Also production
    images generated in step 3 and resigned USB boot images in step 4 depend on oem_segid value. Therefore,
    changing oem_segid here will lead to a mismatch between OTP settings and images, causing boot failures.

A sample configuration file is shown below

::

        ### This file contains default settings for OTP programming during manufacturing.
        ### Modify the parameters as needed for your specific OEM requirements.
        ### Items commented out are optional and can be enabled if required.

        [Chip Info]
        chip_name = klamath
        chip_rev = A0

        [Segmentation ID]
        oem_segid = 0x4f4c4548

        [Image Production Flag]
        Image_production_flag = 1

        [OTP_OEM_IMAGE_SECURE_BOOT_EN]
        oem_security_enable = 0x10011001

        [OTP_OEM_IMAGE_VERSION]
        # Set to a non-zero value to enable OEM image anti-rollback.
        oem_image_version = 0

        [OTP_JTAG_ACCESS_CONTROL]
        jtag_access_control = 0x00000000

Examples: (Klamath: SL26xx)
   ::

   $sdk/factory/scripts/klamath$ ./gen_otp_command.py

When the command completes, two files will be generated in the current directory:

    - otp_commands_uboot.txt:  U-Boot otpwrite commands

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

      boot/u-boot/configs/klamath_usb_suboot_defconfig

      CONFIG_CMD_SOURCE=y


3. Verify OTP Programming
------------------------------

After programming the OTP, it is important to verify that the OTP has been correctly written. You can use the following U-Boot command 
to view all OTP values:
  
   ::

      => otpdump
       Idx   Name
       -----------------------------------------------------
       72    0x00000000  OTP_JTAG_ACCESS_CONTROL
       80    0x92dc58d7  OTP_K0_OEM_HASH_0
       81    0x81a0c5cc  OTP_K0_OEM_HASH_1
       82    0x7b4b0fae  OTP_K0_OEM_HASH_2
       83    0x9dac32a9  OTP_K0_OEM_HASH_3
       84    0xd4a4ea7e  OTP_K0_OEM_HASH_4
       85    0x83596267  OTP_K0_OEM_HASH_5
       86    0xadb93b00  OTP_K0_OEM_HASH_6
       87    0x753ac64c  OTP_K0_OEM_HASH_7
       88    0x2c2f2c42  OTP_K0_OEM_HASH_8
       89    0xf1bee7aa  OTP_K0_OEM_HASH_9
       90    0xbb063fe1  OTP_K0_OEM_HASH_10
       91    0x56cbb296  OTP_K0_OEM_HASH_11
       92    0x4c6c5b6d  OTP_K0_OEM_HASH_12
       93    0xcbca7c34  OTP_K0_OEM_HASH_13
       94    0x8977cb87  OTP_K0_OEM_HASH_14
       95    0xa661193e  OTP_K0_OEM_HASH_15
       112   0xdeafbeaf  OTP_CCGK_0
       113   0xdeafbeaf  OTP_CCGK_1
       114   0xdeafbeaf  OTP_CCGK_2
       115   0xdeafbeaf  OTP_CCGK_3
       116   0xdeafbeaf  OTP_CCGK_4
       117   0xdeafbeaf  OTP_CCGK_5
       118   0xdeafbeaf  OTP_CCGK_6
       119   0xdeafbeaf  OTP_CCGK_7
       120   0xdeafbeaf  OTP_CCUK_0
       121   0xdeafbeaf  OTP_CCUK_1
       122   0xdeafbeaf  OTP_CCUK_2
       123   0xdeafbeaf  OTP_CCUK_3
       124   0xdeafbeaf  OTP_CCUK_4
       125   0xdeafbeaf  OTP_CCUK_5
       126   0xdeafbeaf  OTP_CCUK_6
       127   0xdeafbeaf  OTP_CCUK_7
       128   0x00000000  OTP_CCUK_ID_0
       129   0x00000000  OTP_CCUK_ID_1
       131   0x10011001  OTP_OEM_IMAGE_SECURE_BOOT_ENABLE
       135   0x4f4c4548  OTP_OEM_SEGID
       145   0x00000000  OTP_OEM_IMAGE_VERSION
       556   0x8a189d32  OTP_SOC_UID_0
       557   0x72bc7b7f  OTP_SOC_UID_1
       558   0x2f9d0f85  OTP_SOC_UID_2
       559   0x36786362  OTP_SOC_UID_3
       577   0x00000000  OTP_MAC_ADDRESS_0
       578   0x00000000  OTP_MAC_ADDRESS_1

Please verify that the following table contains all the necessary OTP indices and their corresponding values after programming.

+-------------+----------------------------------+---------------------------------------------+
| Index       | Name                             | Comments                                    |
+=============+==================================+=============================================+
| 72          | OTP_JTAG_ACCESS_CONTROL          | JTAG access control                         |
+-------------+----------------------------------+---------------------------------------------+
| 80--95      | OTP_K0_OEM_HASH_0--15            | OEM Root Public Key Hash (512-bit)          |
+-------------+----------------------------------+---------------------------------------------+
| 112--119    | OTP_CCGK_0--7                    | Customer Chip Global Key (256-bit)          |
+-------------+----------------------------------+---------------------------------------------+
| 131         | OTP_OEM_IMAGE_SECURE_BOOT_EN     | Enable OEM image secure boot                |
+-------------+----------------------------------+---------------------------------------------+
| 135         | OTP_OEM_SEGID                    | OEM segmentation ID                         |
+-------------+----------------------------------+---------------------------------------------+
| 145         | OTP_OEM_IMAGE_VERSION            | OEM image version                           |
+-------------+----------------------------------+---------------------------------------------+

For OTP_CCGK_0-7, as the OTP field is write-only, so the values cannot be read back after programming.
It just showed dummy data (e.g., 0xdeafbeaf). This is expected behavior for write-only OTP fields. 
User can just check the programming status (e.g., if there's error log during programming).


Below table shows the Per-Device OTP values that can be programmed in other sessions.

+-------+-------------------------------+---------------------------------------------+
| Index | Name                          | Comments                                    |
+=======+===============================+=============================================+
| 120   | OTP_CCUK_0                    | Customer Chip Unique Key Word 0 (256-bit)   |
+-------+-------------------------------+---------------------------------------------+
| 121   | OTP_CCUK_1                    | Customer Chip Unique Key Word 1             |
+-------+-------------------------------+---------------------------------------------+
| 122   | OTP_CCUK_2                    | Customer Chip Unique Key Word 2             |
+-------+-------------------------------+---------------------------------------------+
| 123   | OTP_CCUK_3                    | Customer Chip Unique Key Word 3             |
+-------+-------------------------------+---------------------------------------------+
| 124   | OTP_CCUK_4                    | Customer Chip Unique Key Word 4             |
+-------+-------------------------------+---------------------------------------------+
| 125   | OTP_CCUK_5                    | Customer Chip Unique Key Word 5             |
+-------+-------------------------------+---------------------------------------------+
| 126   | OTP_CCUK_6                    | Customer Chip Unique Key Word 6             |
+-------+-------------------------------+---------------------------------------------+
| 127   | OTP_CCUK_7                    | Customer Chip Unique Key Word 7             |
+-------+-------------------------------+---------------------------------------------+
| 128   | OTP_CCUK_ID_0                 | Customer Chip Unique Key ID Word 0 (64-bit) |
+-------+-------------------------------+---------------------------------------------+
| 129   | OTP_CCUK_ID_1                 | Customer Chip Unique Key ID Word 1          |
+-------+-------------------------------+---------------------------------------------+
| 577   | OTP_MAC_ADDRESS_0             | Ethernet MAC address lower 32 bits          |
+-------+-------------------------------+---------------------------------------------+
| 578   | OTP_MAC_ADDRESS_1             | Ethernet MAC address upper 16 bits          |
+-------+-------------------------------+---------------------------------------------+