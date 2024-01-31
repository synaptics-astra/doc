**********************
Astra Yocto User Guide
**********************

Overview
=========

This guide describes Synaptics specific configurations and procedures
required to build and use Yocto images with the supported Synaptics
SoC and development boards.

This guide assumes that the reader already has some familiarity
with Yocto concepts. For introductory material about Yocto and general
Yocto reference guides, please refer to the official
`Yocto Documentation <https://docs.yoctoproject.org/>`_.

This BSP works with the Yocto Kirkstone release and provides support
for the following machines, distributions and images:

.. table:: Supported machines, distributions and images

    +---------+--------------+-------------------+
    | Machine | Distribution | Images            |
    +=========+==============+===================+
    | sl1620  | poky         | astra-media       |
    +---------+--------------+-------------------+
    | sl1640  | poky         | astra-media       |
    +---------+--------------+-------------------+
    | sl1680  | poky         | astra-media       |
    +---------+--------------+-------------------+

.. _yocto_prerequisites:

Build host requirements
=======================

The recommended hardware is a ``x86_64`` host with at least:

  * 16 cores
  * 32 GB of RAM
  * 150 GB of disk

As an example, building from scratch the ``astra-media`` image for ``vs640`` on a
``c5a.4xlarge`` AWS instance, which matches the requirements above, takes
approximately 2 hours.

The Yocto build system can very efficiently exploit more cores if these are available.

.. note::
    Building entirely from NFS mounted directories is not supported
    by the Yocto build system. Please refer to
    `Yocto documentation on the TMPDIR variable <https://docs.yoctoproject.org/ref-manual/variables.html?highlight=nfs#term-TMPDIR>`_
    for more details.

The recommended software configuration is the following:

  * Ubuntu 22.04 LTS
  * Docker 20.10.25 as provided by the standard Ubuntu package ``docker.io``

Other versions of Linux and Docker may also work but may need special configuration.

The build can also be executed directly on the host provided that the Yocto build
dependencies are installed but this configuration is not supported by Synaptics.

.. _yocto_build_image:

How to build an image
=====================

Create the build environment
----------------------------

.. warning::

    During the initial preview, access to Synaptics Astra software is protected with authentication. Please
    follow the instructions in the :ref:`release notes <v0.0.1>` to setup an environment that works with
    authentication.

In order to ensure a correctly configured and clean environment, the build
must be performed within a Docker container. To do so you need to start
a new temporary container that will host the build. The container can be
terminated when the build is finished and a new container can be started
later to rebuild. To start the container use the following command line::

  $ docker run --rm -it -v $(pwd):$(pwd) ghcr.io/syna-astra/crops --workdir=$(pwd)

This will spawn a shell inside the container. The current directory of the host
is mounted inside the container so that the Yocto sources are available within
the container.

.. note::
   On Ubuntu 20 and 18 LTS the seccomp protection feature of docker has to be
   disabled when creating the build container by adding the parameter
   ``--security-opt "seccomp=unconfined"`` after the ``--rm`` parameter in the
   command line above.

.. note::
  Synaptics provides a pre-built container at ``ghcr.io/syna-astra/crops``  that is automatically downloaded
  when you run the command above but you can also compile from the sources available `here <https://github.com/syna-astra/crops>`_.

Obtain the sources
------------------

.. warning::

    During the initial preview, access to Synaptics Astra software is protected with authentication. Please
    follow the instructions in the :ref:`release notes <v0.0.1>` to setup an environment that works with
    authentication.

The sources of the Synaptics Yocto release can be downloaded by cloning a `top
level git repo <https://github.com/syna-astra/sdk>`_. The repository contains
all the required layers as submodules.

To clone the repository within the build environment use the following command:

    pokyuser@xxxx:yyyy$ git clone -b v0.0.1 --recursive https://github.com/syna-astra/sdk.git && cd sdk

The recipes contained in the ``meta-synaptics`` layer point to the relevant git
repository and will be downloaded using the standard bitbake fetching mechanism
of Yocto.

.. note::

    If you clone the repository above with a copy of git installed outside the build environment make sure you
    installed also installed ``git-lfs``

Build an image
--------------

To build an image execute the following commands::

  pokyuser@xxxx:yyyy$ source meta-synaptics/setup/setup-environment

  pokyuser@xxxx:yyyy$ bitbake astra-media

The resulting image can be found in ``build-${MACHINE}/tmp/deploy/images/${MACHINE}/SYNAIMG/``.

The image can be flashed to an evaluation kit board as described in :ref:`prepare_to_boot`.

After flashing the board, to log in to the board please refer to :ref:`linux_login`.

Compatible Layers
=================

This BSP is compatible with these layers:

  * ``poky`` [branch: ``kirkstone``]

  * ``meta-openembedded`` [branch: ``kirkstone``]

    * ``meta-oe`` (required by ``meta-python`` below)
    * ``meta-python`` (required by ``meta-multimedia`` below)
    * ``meta-multimedia`` (optional - for gstreamer support)

  * ``meta-qt`` [branch ``qt/upstream/kirkstone`` ] (optional)


Images
======

``astra-media``
---------------

The ``astra-media`` image, based on the ``poky`` distribution, provides a basic graphical
system with ``weston`` and it is suitable to test ``sl1640`` and ``sl1680`` features.

The image requires some specific configurations in ``conf/local.conf`` to work correctly. The
``meta-synaptics/setup/setup-environment`` script can be used to correctly setup a ``astra-media`` build automatically.

For more details about these configurations please refer to the comments in the
sample ``local.conf`` found in ``meta-synaptics/setup/conf/local.conf.sample``.

In order to be able to run qt application on wayland the following package must also
be added. This must be enable manually even when using ``setup/setup-environment``::

  DISTRO_EXTRA_RDEPENDS_append = " qtwayland"

Configuration
=============

Kernel command line
-------------------

The kernel command line is defined by the variable ``CMDLINE`` of the ``linux-syna``
recipe.


.. _system_memory_config:

System Memory configuration
---------------------------

System memory configuration is performed by changing the variables ``CONFIG_PREBOOT_``
in the configuration file pointed by ``SYNA_SDK_CONFIG_FILE`` variable. The available
configurations can be found by inspecting http://github.com/syna-astra/preboot-prebuilts .

.. _partitions_config:

Partition tables
----------------

Partition tables are configured in the file ``emmc.pt`` found in the directory
``product/${SYNA_SDK_CONFIG_NAME}/emmc.pt`` found at http://github.com/syna-astra/preboot-prebuilts .
The ``SYNA_SDK_CONFIG_NAME`` depends on the ``MACHINE`` and ``DISTRO_CONFIG`` variables.

To customize this file you can override the recipe ``syna-config-native``.

Some partitions are used by the early boot components stored in eMMC boot partition. These
partitions cannot be removed but can be moved. The early boot components locate these partitions
using the GPT found in the UDA. Loading from other hardware partitions is not supported.

Frequently Asked Questions
==========================

How do I override the value of to a recipe variable in ``local.conf``?

  To append the text ``some text`` to the variable ``FOO`` of recipe ``bar`` add
  the following line to ``local.conf``::

    FOO:append:pn-bar = " some text"

  Other changes to the variable can be performed with the standard operators
  described in the `Bitbake Guide <https://docs.yoctoproject.org/bitbake/2.4/bitbake-user-manual/bitbake-user-manual-metadata.html#basic-syntax>`_.

Troubleshooting
===============

The build fails at the package ``gdk-pixbuf-native`` with error ``Failed to
close file descriptor for child process`` on Ubuntu 20 or 18.

  This problem is caused by an incompatibility of the package build system with the ``libseccomp``
  library on the host that is running docker. To solve this issue update the libseccomp2 library
  on the host that runs docker or add the parameter ``--security-opt "seccomp=unconfined`` to
  the docker command line when creating the docker build environment.

Build of packages with out-of-trees modules (such as ``synasdk-synap-module``) fail with error
``Kernel configuration is invalid.``.

  Under some circumstances the state of the recipe ``make-mod-scripts`` may become corrupted. To fix
  the issue clean the recipe with the command::

    bitbake -c cleansstate make-mod-scripts
