Building an application
=======================

.. highlight:: console

.. note::

    To build an application it is recommended to use a host device as described :ref:`here <yocto_prerequisites>`.
    This guide assumes you set-up your Astra Machina board with a working image as explained in
    :ref:`quickstart_install` and you connected the host and the board to the same network.

To build an application follows these steps:

1. Download a pre-built toolchain package from the `release page <https://github.com/synaptics-astra/sdk/releases>`__.

2. Unpack the toolchain package, the ``CPUTYPE`` for ``sl1680`` is ``cortexa73``, for ``sl1620`` and ``sl1640`` is
   ``cortexa55``::

    $ ./poky-glibc-x86_64-astra-media-${CPUTYPE}-${MACHINE}-toolchain-4.0.9.sh
    Poky (Yocto Project Reference Distro) SDK installer version 4.0.9
    =================================================================
    Enter target directory for SDK (default: /opt/poky/4.0.9): toolchain
    You are about to install the SDK to "/home/user/toolchain". Proceed [Y/n]?
    Extracting SDK.................................................................................................................................................................................................................................................................................................................................done
    Setting it up...done
    SDK has been successfully set up and is ready to be used.
    Each time you wish to use the SDK in a new shell session, you need to source the environment setup script e.g.
      $ . /home/user/toolchain/environment-setup-${CPUTYPE_32}-pokymllib32-linux-gnueabi
      $ . /home/user/toolchain/environment-setup-${CPUTYPE}-poky-linux

3. Create a test application::

    $ echo -e '#include <stdio.h>\nint main(void) { printf("hello world\\n");}' > test.c

4. Setup the build environment variables::

    $ . toolchain/environment-setup-${CPUTYPE}-poky-linux

5. Build the application::

    $ ${CC} test.c -o test

6. Find the ip address of the board with the following command on the target::

    # ifconfig eth0 | grep "/inet addr/"
              inet addr:192.168.1.110  Bcast:192.168.1.255  Mask:255.255.255.0

7. Upload application to the board by running the following command on the host::

    $ scp test root@192.168.1.110:/tmp

8. Run the application on the board::

    $ ssh root@192.168.1.110 /tmp/test

For more details, troubleshooting and information check the :ref:`Synaptics Astra Yocto Guide <yocto_build_app>`.
