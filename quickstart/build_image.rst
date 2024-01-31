Build a new image
=================

.. highlight:: console

.. warning::

    During the initial preview, access to Synaptics Astra software is protected with authentication. Before
    performing these steps ensure you have successfully logged in as described in the :ref:`release notes <v0.0.1>`.

.. note::

    To build a new image you need a host device as described :ref:`here <yocto_prerequisites>`

To build a image run the following commands:

1. Clone the sources from `github <https://github.com/syna-astra/sdk>`_ ::

    $ git clone --recursive https://github.com/syna-astra/sdk

2. Start a build environment container::

    $ docker run --rm -it -v $(pwd):$(pwd) ghcr.io/syna-astra/crops --workdir=$(pwd)

3. Setup the build tree::

    pokyuser@xxxx:yyyy$ source meta-synaptics/setup/setup-environment

    Select the MACHINE you want to build:

    1) sl1620
    2) sl1640
    3) sl1680

    You selection: 1

4. Build the image::

    pokyuser@xxxx:yyyy$ bitbake astra-media

The image will be available in ``build-${MACHINE}/tmp/deploy/images/${MACHINE}/SYNAIMG/`` and can be flashed with
the procedure described in :ref:`prepare_to_boot`.

For more details, troubleshooting and information check the :ref:`Synaptics Astra Yocto Guide <yocto_build_image>`.
