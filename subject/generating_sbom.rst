Generating the SBOM with Yocto
==============================

-  `1. Overview <#GuideofgeneratingSBOMforYoctocompilatio>`__

-  `2. Core Configuration <#GuideofgeneratingSBOMforYoctocompilatio>`__

-  `3. Results <#GuideofgeneratingSBOMforYoctocompilatio>`__

   -  `3.1 Document
      Structure <#GuideofgeneratingSBOMforYoctocompilatio>`__

1. Overview
-----------

| This guide explains how to generate SPDX-format SBOMs for Yocto-based
  images using the create-spdx class.
| It covers the required configuration, build steps, and output
  locations so that OEMs can produce SBOMs for their own builds and meet
  CRA-related documentation requirements.

2. Core Configuration
---------------------

To enable and customize SPDX generation, add the following variables to
your project’s fileconf/local.conf

.. list-table::
   :header-rows: 1
   :widths: 36 29 35

   * - **Configuration**
     - **Purpose & Description**
     - **Example / Value Notes**
   * - ``INHERIT += "create-spdx"``
     - Enables the SPDX generation class (required).
     - N/A
   * - ``SPDX_PRETTY``
     - Formats JSON for human readability and debugging.
     - 1 (Enabled) / 0 (Disabled)
   * - ``SPDX_ARCHIVE_PACKAGED``
     - Archives the packaged files.
     - 1 (Enabled) / 0 (Disabled)
   * - ``SPDX_INCLUDE_SOURCES``
     - Includes source file-level information in the SBOM.
     - 1 (Enabled) / 0 (Disabled)
   * - ``SPDX_ARCHIVE_SOURCES``
     - Archives the source code. *(Note: Significantly increases build time and storage.)*
     - 1 (Enabled) / 0 (Disabled)
   * - ``SPDX_ORG``
     - Identifies the organization responsible for creating or managing the SPDX document.
     - "Synaptics Incorporated"
   * - ``SPDX_SUPPLIER``
     - Identifies the supplier who directly provides the software package or component.
     - "Organization: Synaptics Incorporated"
   * - ``SPDX_NAMESPACE_PREFIX``
     - Defines the base URI namespace for the SPDX documents.
     - "https://synaptics.com/spdxdocs/astra/${ASTRA_VERSION}"
   * - ``SPDX_CUSTOM_ANNOTATION_VARS``
     - Specifies build variables to include as custom annotations in the document.
     - "ASTRA_VERSION DISTRO_VERSION MACHINE"

Example::

  INHERIT += "create-spdx"
  SPDX_PRETTY = "1"
  SPDX_ARCHIVE_PACKAGED = "1"
  SPDX_INCLUDE_SOURCES = "0"
  SPDX_ARCHIVE_SOURCES = "0"
  SPDX_ORG = "Synaptics Incorporated"
  SPDX_SUPPLIER = "Organization: Synaptics Incorporated"
  SPDX_NAMESPACE_PREFIX =
  "https://synaptics.com/spdxdocs/astra/${ASTRA_VERSION}"
  SPDX_CUSTOM_ANNOTATION_VARS = "ASTRA_VERSION DISTRO_VERSION MACHINE"

3. Results
----------

After running ``bitbake <your-image>``, the SPDX artifacts are packaged and
placed in the ``tmp/deploy/image/${MACHINE}/`` directory. The output archive
is typically named ``<image-name>.rootfs.spdx.tar.zst``.

Example::

  $ ls -la tmp/deploy/images/sl2619-coralboard/\*oobe\*.spdx.\* -lh
  -rw-r--r-- 2 tay dialout 4.7M Sep 28 15:07 tmp/deploy/images/sl2619-coralboard/astra-media-oobe-sl2619-coralboard.rootfs-20260928065003.spdx.tar.zst

::

  $ grep "Synaptics Incorporated"\\\|"synaptics.com"\\|ASTRA_VERSION\\|DISTRO_VERSION\\|MACHINE dropbear.spdx.json recipe-dropbear.spdx.json -rnE recipe-dropbear.spdx.json:8: "Organization: Synaptics Incorporated",
  recipe-dropbear.spdx.json:14: "documentNamespace": "https://synaptics.com/spdxdocs/astra/scarthgap_6.12_v2.6.0/recipe-dropbear-a4d00820-28b5-5b4d-bced-183185131a4f",
  recipe-dropbear.spdx.json:121: "comment": "ASTRA_VERSION=scarthgap_6.12_v2.6.0"
  recipe-dropbear.spdx.json:127: "comment": "DISTRO_VERSION=5.0.9"
  recipe-dropbear.spdx.json:133: "comment": "MACHINE=sl1680"
  recipe-dropbear.spdx.json:155: "supplier": "Organization: Synaptics Incorporated",
  ......

3.1 Document Structure
~~~~~~~~~~~~~~~~~~~~~~

Unzip this package <image-name>.rootfs.spdx.tar.zst, you will see many
files underneath, some documents are described below:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - **File Type**
     - **Purpose**
   * - ``<image-name>.spdx.json``
     - Root document and main entry point. Describes the rootfs image and links all dependency packages. Example: ``astra-media-sl1680.rootfs-20260929180818.spdx.json``.
   * - ``<package-name>.spdx.json``
     - Metadata for each installed package, including its file list (paths, checksums, and licenses).
   * - ``recipe-<name>.spdx.json``
     - Metadata for each build recipe, including source URLs, declared licenses, and build dependencies.
   * - ``runtime-<name>.spdx.json``
     - Runtime dependency relationships for each package.
   * - ``index.json``
     - Document manifest used for integrity verification and namespace-to-filename mapping.
