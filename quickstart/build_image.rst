Building and installing a custom system image
=============================================

.. highlight:: console

.. note::

    To build a new image you need a host device as described :ref:`here <yocto_prerequisites>`

To build a image run the following commands:

1. Start a build environment container::

    $ docker run --rm -it -v $(pwd):$(pwd) ghcr.io/synaptics-astra/crops:#release# --workdir=$(pwd)

3. Clone the sources from `GitHub <https://github.com/synaptics-astra/sdk>`_ ::

    pokyuser@xyz:/path/to/workspace $ git clone -b v#release# --recurse-submodules \
                                                https://github.com/synaptics-astra/sdk

4. Setup the build tree::

    pokyuser@xyz:/path/to/workspace $ cd sdk

    pokyuser@xyz:/path/to/workspace/sdk $ source meta-synaptics/setup/setup-environment

    Select the MACHINE you want to build:

    1) sl1620
    2) sl1640
    3) sl1680

    You selection: 1

5. Modify the image configuration metadata as desired (e.g. by adding more packages to the image by
   tweaking the ``conf/local.conf`` file). For more information on how to configure the image refer to :doc:`/yocto`

6. Build the image::

    pokyuser@xyz:/path/to/workspace/sdk/build-slXYZ $ bitbake astra-media

The image will be available in ``build-${MACHINE}/tmp/deploy/images/${MACHINE}/SYNAIMG/`` and can be flashed with
the procedure described in :ref:`prepare_to_boot`.

For more details, troubleshooting and information check the :ref:`Synaptics Astra Yocto Guide <yocto_build_image>`.
