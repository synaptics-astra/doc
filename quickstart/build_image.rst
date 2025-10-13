Building and installing a custom system image
=============================================

.. highlight:: console

.. note::

    To build a new image you need a host device as described :ref:`here <yocto_prerequisites>`

To build a image run the following commands:

1. Start a build environment container::

    $ docker run --rm -it -v $(pwd):$(pwd) ghcr.io/synaptics-astra/crops:1.1.0 --workdir=$(pwd)

2. Clone the sources from `GitHub <https://github.com/synaptics-astra/sdk>`_ ::

    pokyuser@xyz:/path/to/workspace $ git clone -b #release# --recurse-submodules \
                                                https://github.com/synaptics-astra/sdk

3. Setup the build tree::

    pokyuser@xyz:/path/to/workspace $ cd sdk

    pokyuser@xyz:/path/to/workspace/sdk $ . meta-synaptics/setup/setup-environment

    Select the MACHINE you want to build:

    1) conf/machine/sl1620.conf       3) conf/machine/sl1640.conf      5) conf/machine/sl1680.conf      7) conf/machine/sl1680usb.conf   9) conf/machine/sl1640spi.conf  11) conf/machine/sl2615.conf
    2) conf/machine/sl1620usb.conf    4) conf/machine/sl1640usb.conf   6) conf/machine/sl1680spi.conf   8) conf/machine/sl1620spi.conf  10) conf/machine/sl2611.conf     12) conf/machine/sl2619.conf

    You selection: 12

.. note::

    SL2619 is the only MACHINE type supported with Scarthgap_6.12_v2.0.1.

4. Modify the image configuration metadata as desired (e.g. by adding more packages to the image by
   tweaking the ``conf/local.conf`` file). For more information on how to configure the image refer to :doc:`/yocto`

5. Build the image::

    pokyuser@xyz:/path/to/workspace/sdk/build-slXYZ $ bitbake astra-media

The image will be available in ``build-${MACHINE}/tmp/deploy/images/${MACHINE}/SYNAIMG/`` and can be flashed with
the procedure described in :ref:`prepare_to_boot`.

For more details, troubleshooting and information check the :ref:`Synaptics Astra Yocto Guide <yocto_build_image>`.
