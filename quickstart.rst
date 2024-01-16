Quick start
***********

To get started with the Synaptics Astra SDK, you can do the following things:

.. _quickstart_install:

Install and use a pre-built image
=================================

To install a pre-built image on a Synaptics Astra evaluation kit:

1. Download a prebuilt image suitable for your development kit from `GitHub <https://github.com/syna-astra/sdk/releases/>`_

2. Follow the instructions in :ref:`flashing` to install the image on the board

3. Connect to the board using the instructions in :ref:`shell`

.. _quickstart_multimedia_demos:

Play a video with hardware acceleration
========================================

To play a video on a Synaptics Astra evaluation kit:

1. Install a pre-built image and connect to the board as described in :ref:`quickstart_install`
2. TBD

To learn about other multimedia demos refer to :ref:`multimedia_demos`.

.. _quickstart_ai_demos:

Run a neural network using hardware acceleration
================================================

To run a image classification neural network on a random image using an evaluation kit:

1. Install a pre-built image and connect to the board as described in :ref:`quickstart_install`

2. Run the following commands on the target::

      $ synap_cli -m /path/to/model/tbd random

To learn about other ai demos refer to :ref:`ai_demos`.

Convert and test your own AI model
==================================

To convert your own AI model and run it on an evaluation kit use the following steps:

1. Install a pre-built image and connect to the board as described in :ref:`quickstart_install`

2. Convert the model with a basic configuration by running the following command on the host::

        $ docker run --rm -it -v $(pwd):$(pwd) -u $(id -u):$(id -g) ghcr.io/syna-astra/synap mymodel.tflite

   where ``mymodel.tflite`` is the name of the model to convert that is present in the current working directory.

   This will create a file ``mymodel.synap`` in the local directory.

3. Upload the converted model to the board by running the following command on the host::

   $ scp mymodel.synap root@IP_ADDRESS_OF_BOARD:/tmp

4. Then connect to the board and issue the following command::

   $ synap_cli -m /tmp/model.synap random

To learn more about model conversion options, more model testing tools and how to use the model in your own
application refer to :ref:`synap`.
