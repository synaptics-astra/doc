*********************************
Astra Yocto Linux Developer Guide
*********************************

.. highlight:: console

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
  * Docker 20.10 or later provided by the standard Ubuntu package ``docker.io``

Other versions of Linux and Docker may also work but may need special configuration. You can find more information on
how to install Docker in Ubuntu in :ref:`install_docker`.

The Synaptics Astra SDK is known to work also on Ubuntu 22.04 installed inside Windows Subsystem For Linux (WSL) 2.0
on Windows 11. You can find more information on how to install WSL2 in :ref:`wsl_setup`.

The build can also be executed directly on a Linux host provided that the Yocto build dependencies are installed.
This configuration is not supported by Synaptics.

.. _wsl_setup:

WSL 2 Setup (required only when using Windows)
----------------------------------------------

.. note::

    If you previously installed WSL1, installed another WSL2 distribution or disabled the hyper-v support on
    your machine you may need to perform some additional steps. See the :ref:`troubleshooting` section for some
    suggested steps.

First install Windows Subsystem for Linux with the following command in PowerShell (as administrator):

.. code-block:: ps1con

    PS C:\Users\username> wsl --install

This command will setup WSL and the default distribution which is Ubuntu 22.04 at the time of writing.
You can find more details on installation procedure the `WSL website <https://learn.microsoft.com/en-us/windows/wsl/install>`__.

By default WSL only uses up to 50% of the RAM of the host, this may not be enough to reach the memory required to build
an image. If that's the case you can in increase the memory adding the following to the file ``.wslconfig`` in your
user directory (normally ``C:\Users\<Username``):

.. code-block:: ini

    [wsl2]
    memory=24GB

Then to apply the changes in powershell run the command:

.. code-block:: ps1con

    PS C:\Users\username> wsl.exe --shutdown

You can find more information about WSL configuration `here <https://learn.microsoft.com/en-us/windows/wsl/wsl-config>`__.

Once you setup the WSL2 environment you can start a terminal from the start menu by selecting
the Windows Terminal App and then select the Ubuntu-22.04 distribution.

Once you are in the terminal you can install Docker as described in :ref:`install_docker`

.. _install_docker:

Docker setup
------------

To install docker use the following steps:

1. Install the docker package::

    $ sudo apt install docker.io

2. Add the current user to the docker group so that it will be able to use docker::

   $ sudo adduser ${USER} docker

3. The change of user will not be automatically applied until a reboot (in some situation a log-in may suffice). To
   apply the changes to the current shell you can also run the following command::

       $ newgrp docker
       $ newgrp ${USER}

.. _yocto_build_image:

How to build an image
=====================

.. _start_build_env:

Start the build environment
---------------------------

.. note::

    The following steps require an hosts with docker correctly installed,
    you can find more information on how to setup docker in :ref:`yocto_prerequisites`.

.. warning::

    When using WSL2 build from ``/mnt/c`` and other host file system drives is not supported. Your build
    folder must reside on the native WSL2 file system (e.g. ``/home/${USER}``)

In order to ensure a correctly configured and clean environment, the build
must be performed within a Docker container. To do so you need to start
a new temporary container that will host the build. The container can be
terminated when the build is finished and a new container can be started
later to rebuild with the same command.

To start the container use the following command line::

    $ docker run --rm -it -v $(pwd):$(pwd) ghcr.io/synaptics-astra/crops:1.0.0 --workdir=$(pwd)

This will spawn a shell inside the container. The current directory of the host
is mounted inside the container so that the workspace is available within
the container.

.. note::
   On Ubuntu 20 and 18 LTS the seccomp protection feature of docker has to be
   disabled when creating the build container by adding the parameter
   ``--security-opt "seccomp=unconfined"`` after the ``--rm`` parameter in the
   command line above.

.. note::
  If your environment requires a proxy to connect to the internet, please follow these instructions
  for `Configuring the Docker daemon <https://docs.docker.com/config/daemon/proxy/>`_
  and `Configuring the Docker client <https://docs.docker.com/network/proxy/#configure-the-docker-client>`_ to use a proxy server.

.. note::
  Synaptics provides a pre-built container at ``ghcr.io/synaptics-astra/crops``  that is automatically downloaded
  when you run the command above but you can also compile from the sources available
  `here <https://github.com/synaptics-astra/crops>`_.

Obtain the sources
------------------

The sources of the Synaptics Yocto release can be downloaded by cloning a `top
level git repo <https://github.com/synaptics-astra/sdk>`_. The repository contains
all the required layers as submodules.

To clone the repository within the build environment started with the instructions in :ref:`start_build_env`
use the following command::

     pokyuser@xyz:/path/to/workspace $ git clone -b v#release# --recurse-submodules \
                                                 https://github.com/synaptics-astra/sdk

The recipes contained in the ``meta-synaptics`` layer point to the relevant git repository and will be downloaded
using the standard bitbake fetching mechanism of Yocto.

Build an image
--------------

To build an image execute the following commands::

  pokyuser@xyz:/path/to/workspace $ cd sdk

  pokyuser@xyz:/path/to/workspace/sdk $ source meta-synaptics/setup/setup-environment

  pokyuser@xyz:/path/to/workspace/sdk/build-XYZ $ bitbake astra-media

The resulting image can be found in ``build-${MACHINE}/tmp/deploy/images/${MACHINE}/SYNAIMG/``.

To build an image without multimedia capabilities, build the astra-core image using the command ``bitbake astra-core``.

.. note::
  The astra-core image is included in v1.2.0 and later releases.

The image can be flashed to an evaluation kit board as described in :ref:`prepare_to_boot`.

After flashing the board, to log in to the board please refer to :ref:`linux_login`.

.. _yocto_build_app:

How to develop an application
=============================

One of the key features of the Yocto project is the ability to create a standalone SDK that includes everything you
need to develop and test applications for a given target image.

The standalone toolchain is a precompiled set of tools, libraries, and headers that match the configuration of your
Yocto Project build. It provides a consistent and controlled development environment that closely mirrors the
target system. This ensures that the applications you develop will be compatible with the specific image that
you're deploying on your embedded devices.

Using the standalone toolchain, you can compile on your development machine before
deploying them to the target device. This can greatly speed up the development process, as you don't need to
compile the entire image each time you want to test a change.

Pre-compiled toolchains for the default Astra Machina images are also available
on `GitHub <https://github.com/synaptics-astra/sdk/releases>`__.

Once you obtained the toolchain, you can install it on your development machine. The toolchain includes a script
that sets up the environment variables needed to use the tools. The recommended and supported configuration of the
development machine is the same as described in :ref:`yocto_prerequisites` but the toolchain is compatible with
a wide range of environments.

To setup the toolchain you first uncompress it as follows::

  $ ./poky-glibc-x86_64-astra-media-${CPUTYPE}-${MACHINE}-toolchain-4.0.9.sh
  Poky (Yocto Project Reference Distro) SDK installer version 4.0.9
  =================================================================
  Enter target directory for SDK (default: /opt/poky/4.0.9): toolchain
  You are about to install the SDK to "/home/user/toolchain". Proceed [Y/n]?
  Extracting SDK.................................................................................................................................................................................................................................................................................................................................done
  Setting it up...done
  SDK has been successfully set up and is ready to be used.
  Each time you wish to use the SDK in a new shell session, you need to source the environment setup script e.g.
    $ . /home/user/toolchain/environment-setup-armv7at2hf-neon-vfpv4-pokymllib32-linux-gnueabi
    $ . /home/user/toolchain/environment-setup-cortexa73-poky-linux

The exact names of the toolchain environment files depend on the target board: ``CPUTYPE`` for ``sl1680`` is
``cortexa73``, for ``sl1620`` and ``sl1640`` is ``cortexa55``

Then to configure the build environment you need to source a configuration script as follows::

  $ . toolchain/environment-setup-${CPUTYPE}-poky-linux

With the environment setup, you can use the provided cross-compiler to compile your applications. The
toolchain also includes libraries and headers for the various components included in the image, so you can develop
applications that take full advantage of these components. You can use the environment variables set by the script
such as ``CC`` to invoke the cross-compiler and build your application with it.

More information about the standalone toolchain are available in the
`Yocto documentation <https://docs.yoctoproject.org/sdk-manual/using.html>`__.

How to re-build a standalone toolchain
--------------------------------------

You can re-generate a toolchain in your Yocto build environment configured as described in :ref:`yocto_build_image`
by running the following command::

  pokyuser@xyz:/path/to/workspace $ cd sdk

  pokyuser@xyz:/path/to/workspace/sdk $ source meta-synaptics/setup/setup-environment

  pokyuser@xyz:/path/to/workspace/sdk/build-XYZ $ bitbake astra-media -c do_populate_sdk

The build proces will generate the toolchain in the directory ``build-${MACHINE}/tmp/deploy/sdk``.


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

  DISTRO_EXTRA_RDEPENDS:append = " qtwayland"

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
configurations can be found by inspecting https://github.com/synaptics-astra/boot-preboot-prebuilts .

.. _partitions_config:

Partition tables
----------------

Partition tables are configured in the file ``emmc.pt`` found in the directory
``product/${SYNA_SDK_CONFIG_NAME}/emmc.pt`` found at http://github.com/synaptics-astra/configs .
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

.. _troubleshooting:

Troubleshooting
===============

The build fails at the package ``gdk-pixbuf-native`` with error ``Failed to
close file descriptor for child process`` on Ubuntu 20 or 18.

  This problem is caused by an incompatibility of the package build system with the ``libseccomp``
  library on the host that is running docker. To solve this issue update the libseccomp2 library
  on the host that runs docker or add the parameter ``--security-opt "seccomp=unconfined`` to
  the docker command line when creating the docker build environment.

The build fails at package ``astra-media`` with the error ``path mismatch``.

  This error can occur when adding a new package to the ``astra-media`` image. Preforming a clean on
  the ``astra-media`` package and then rebuilding it will fix the issue::

    bitbake -c clean astra-media

Build of packages with out-of-trees modules (such as ``synasdk-synap-module``) fail with error
``Kernel configuration is invalid.``.

  Under some circumstances the state of the recipe ``make-mod-scripts`` may become corrupted. To fix
  the issue clean the recipe with the command::

    bitbake -c cleansstate make-mod-scripts

Docker commands fail with the error ``permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/version": dial unix /var/run/docker.sock: connect: permission denied``

  Make sure your user is in the ``docker`` group::

    $ getent group docker
    docker:x:133:yourusername

  and that your current session is logged in to the ``docker`` group::

    $ id
    uid=1000(yourusername) gid=1000(yourusername) groups=1000(yourusername),133(docker)

  To add your user to the docker group user the following command::

    $ sudo adduser yourusername docker

  To ensure your session logged in to the ``docker`` group use the following command::

    $ newgrp docker

The build fails on WSL2 when building from ``/mnt/c``

    The Yocto build requires a case-sensitive file system. By default WSL2 mounts of the ``C:`` drive found in ``/mnt/c`` is not. This leads to the following error::
    
        pokyuser@868531cb885f:/mnt/c/work/astra/sdk/build-sl1680$ bitbake astra-media
        WARNING: You are running bitbake under WSLv2, this works properly but you should optimize your VHDX file eventually to avoid running out of storage space
        ERROR:  OE-core's config sanity checker detected a potential misconfiguration.
            Either fix the cause of this error or at your own risk disable the checker (see sanity.conf).
            Following is the list of potential problems / advisories:
        The TMPDIR (/mnt/c/work/astra/sdk/build-sl1680/tmp) can't be on a case-insensitive file system.

    To solve this problem, either setup the build in the WSL2 home directory (i.e. ``cd ~``) or enable case-sensitive on the main Windows file system with the following command in an admin PowerShell:

    .. code-block:: ps1con

        PS C:> fsutil.exe file SetCaseSensitiveInfo C:\work\astra\sdk

    Where ``C:\work\astra\sdk\`` is the directory containing the sdk repository clone.

WSL2 is not working correctly on my Windows machine

    You may try the following things to reset the state on your machine:

    1. Enable the Windows Subsystem for Linux:

        .. code-block:: ps1con

            PS C:\Users\username> dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

    2. Enable Virtual Machine feature:

        .. code-block:: ps1con

            PS C:\Users\username> dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

    3. Restart your PC

    4. Download the `Linux kernel update package <https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi>`__
       and install it

    5. Set WSL 2 as default version:

        .. code-block:: ps1con

            PS C:\Users\username> wsl --set-default-version 2

    6. Install Ubuntu 22.04 LTS from `Microsoft Store <https://www.microsoft.com/store/apps/9PN20MSR04DW>`__

    7. Set default distro to Ubuntu-22.04:

        .. code-block:: ps1con

            PS C:\Users\username> wsl --set-default Ubuntu-22.04
