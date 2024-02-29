**********************
Astra Yocto User Guide
**********************

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

Other versions of Linux and Docker may also work but may need special configuration.

The Synaptics Astra SDK is known to work also on Ubuntu 22.04 installed inside Windows Subsystem For Linux (WSL) 2.0
on Windows 11.

The build can also be executed directly on a Linux host provided that the Yocto build dependencies are installed.
This configuration is not supported by Synaptics.

.. _yocto_build_image:

How to build an image
=====================

.. _workspace_setup:

Workspace setup
---------------

.. note::

    It is recommended to use a Ubuntu 22.04 host to run the following instructions. See :ref:`yocto_prerequisites` for
    more details.

The early access release of the Astra SDK is available only to registered users and for this reason it is required
to setup authentication to GitHub. In order to be able to access the release you need to make sure your GitHub account
has been invited to the `syna-astra Organization <https://github.com/syna-astra>`_ and that you accepted the invitation.
You can check you are able to access the organization by browsing to the `sdk git <https://github.com/syna-astra/sdk>`__.
You can review your organizations by checking your `profile settings <https://github.com/settings/organizations>`__.

WSL 2 Setup (required only when using Windows)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First install Windows Subsystem for Linux with the following command in PowerShell:

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

Docker setup
^^^^^^^^^^^^

To install docker use the following steps:

1. Install the docker package::

    $ sudo apt-get install docker.io

2. Add the current user to the docker group so that it will be able to use docker::

   $ sudo adduser ${USER} docker

3. The change of user will not be automatically applied until a reboot (in some situation a log-in may suffice). To
   apply the changes to the current shell you can also run the following command::

       $ newgrp docker
       $ newgrp ${USER}

.. _setup_docker_auth:

Setup authenticated Docker registry access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to be able to access the docker containers used by the Synaptics Astra SDK you will need to create a
personal access token:

1. Create a *classic* personal access token (PAT) with ``read:package`` permissions as described in the
   `GitHub documentation <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic>`__.

2. After obtaining the token run the following command::

    $ docker login ghcr.io
    Username: <enter your GitHub username>
    Password: <enter the token>

.. _setup_auth_ssh:

Setup authenticated git access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to be able to clone Synaptics Astra SDK repositories you need configure authenticated ssh access with
the following steps:

1. Create a local directory in your host where your workspace will be located::

     $ mkdir workspace

2. Create a directory to store the ssh configuration used in the workspace::

     $ cd workspace
     $ mkdir .ssh && chmod 700 .ssh

2. Use the following command line when starting the CROPS container (make sure you are in the workspace directory when
   executing the command)::

    $ docker run --rm -it -v $(pwd):$(pwd) \
      -v $(pwd)/.ssh:/home/pokyuser/.ssh ghcr.io/syna-astra/crops:#release# --workdir=$(pwd)

3. Create a ssh public/private keypair::

     pokyuser@xyz:/path/to/workspace $ ssh-keygen -t ed25519 -C "your_email@example.com"

   To simplify your setup you can leave the passphrase empty, if your IT mandates a passphrase you may do so but you
   will need to `setup an ssh-agent <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux#adding-your-ssh-key-to-the-ssh-agent>`__.

4. Add the generated public key to your GitHub profile as described in the `GitHub documentation <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?platform=linux&tool=webui>`__.

5. Import the GitHub public host key to the list of known hosts::

        pokyuser@xyz:/path/to/workspace $ ssh git@github.com
        The authenticity of host 'github.com (140.82.121.3)' can't be established.
        ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
        This key is not known by any other names
        Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
        Warning: Permanently added 'github.com' (ED25519) to the list of known hosts.
        Hi username! You've successfully authenticated, but GitHub does not provide shell access.

   You can validate the key using the information found in the `GitHub Documentation <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints>`_.

.. note::

   These steps explain how setup authenticated SSH access within the build container. It is important that ssh
   authentication to GitHub works within the container because it will be used by ``bitbake`` during the build
   process to fetch the sources of the Synaptics Astra SDK components.

.. _start_build_env:

Start the build environment
---------------------------

In order to ensure a correctly configured and clean environment, the build
must be performed within a Docker container. To do so you need to start
a new temporary container that will host the build. The container can be
terminated when the build is finished and a new container can be started
later to rebuild with the same command.

To start the container use the following command line::

    $ cd workspace

    $ docker run --rm -it -v $(pwd):$(pwd) \
                 -v $(pwd)/ssh:/home/pokyuser/.ssh \
                 ghcr.io/syna-astra/crops:#release# --workdir=$(pwd)

This will spawn a shell inside the container. The current directory of the host
is mounted inside the container so that the workspace is available within
the container.

.. note::
   On Ubuntu 20 and 18 LTS the seccomp protection feature of docker has to be
   disabled when creating the build container by adding the parameter
   ``--security-opt "seccomp=unconfined"`` after the ``--rm`` parameter in the
   command line above.

.. note::
  Synaptics provides a pre-built container at ``ghcr.io/syna-astra/crops``  that is automatically downloaded
  when you run the command above but you can also compile from the sources available
  `here <https://github.com/syna-astra/crops>`_.

Obtain the sources
------------------

The sources of the Synaptics Yocto release can be downloaded by cloning a `top
level git repo <https://github.com/syna-astra/sdk>`_. The repository contains
all the required layers as submodules.

To clone the repository within the build environment started with the instructions in :ref:`start_build_env`
use the following command::

     pokyuser@xyz:/path/to/workspace $ git clone -b v#release# --recurse-submodules \
                                                 git@github.com:syna-astra/sdk

The recipes contained in the ``meta-synaptics`` layer point to the relevant git repository and will be downloaded
using the standard bitbake fetching mechanism of Yocto.

.. note::

    If you clone the repository above with a copy of git installed outside the build environment make sure you
    installed also installed ``git-lfs``

Build an image
--------------

.. note::
   Make sure you have added the GitHub public ssh host keys as described in :ref:`setup_auth_ssh` otherwise
   the build will fail when fetching the sources for Synaptics recipes.

To build an image execute the following commands::

  pokyuser@xyz:/path/to/workspace $ cd sdk

  pokyuser@xyz:/path/to/workspace/sdk $ source meta-synaptics/setup/setup-environment

  pokyuser@xyz:/path/to/workspace/sdk/build-XYZ $ bitbake astra-media

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


The ``docker login`` command fails with error ``Error response from daemon: Get "https://ghcr.io/v2/": denied: denied``

  The password entered is not a valid GitHub Access Token. Please make sure you create an access token as described
  in :ref:`setup_docker_auth`.

Docker commands fail with error ``Error response from daemon: denied``

  Make sure you created and used to log-in to ghcr.io a classic token and not a fine grained token as described in
  :ref:`setup_docker_auth`.
