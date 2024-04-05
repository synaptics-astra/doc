Converting and running a custom neural network
==============================================

.. highlight:: console

.. note::

   In addition to the :ref:`prerequisites for flashing <prepare_to_boot>` you also need a host with
   docker installed, an ethernet cable and a local network with DHCP.

To convert your own AI model and run it on an evaluation kit use the following steps:

1. Install a pre-built image and connect to the board as described :doc:`here <flash_image>`

2. Connect the board to a local network using the ethernet cable

3. Download ``1.tflite`` from `Kaggle <https://www.kaggle.com/models/tensorflow/mobilenet-v2/frameworks/tfLite/variations/1-0-224-quantized>`_
   and save it as ``mymodel.tflite``.

4. Download the docker image of the SyNAP toolkit on the host::

    $ docker pull ghcr.io/synaptics-synap/toolkit:3.0.0

5. Install an alias in the shell of the host to run the SyNAP Toolkit container::

    $ alias synap='docker run -i --rm -u $(id -u):$(id -g) -v ${MOUNTPATH}:${MOUNTPATH} \
                   -w $(pwd) ghcr.io/synaptics-synap/toolkit:3.0.0'

   where ``${MOUNTPATH}`` is the absolute path of the directory of the host to mount inside the container.
   This command can be executed in any directory and will be valid for the current session.
   You can add it to your shell startup file (e.g. ``.bashrc`` or ``.zshrc``).

   You can get help on the available toolkit commands by running it without parameters::

    $ synap

6. Convert the model with the following command::

    $ synap convert --model mymodel.tflite --target ${CHIP_NAME} --out-dir converted

   where ``${CHIP_NAME}`` is either ``SL1620``, ``SL1640`` or ``SL1680`` depending on the target device.

   This command converts ``mymodel.tflite`` to ``converted/model.synap``, the model converted
   for execution on the evaluation kit.

7. Find the ip address of the board with the following command on the target::

    # ifconfig eth0 | grep "/inet addr/"
              inet addr:192.168.1.110  Bcast:192.168.1.255  Mask:255.255.255.0

8. Upload the converted model to the board by running the following command on the host::

    $  scp converted-model/model.synap root@192.168.1.110:/tmp

9. Connect to the board and issue the following command::

    # cd /tmp
    # synap_cli random
    Flush/invalidate: yes
    Loop period (ms): 0
    Network inputs: 1
    Network outputs: 1
    Input buffer: input size: 150528 : random
    Output buffer: output size: 1001

    Predict #0: 12.49 ms

    Inference timings (ms):  load: 30.72  init: 3.35  min: 12.49  median: 12.49  max: 12.49  stddev: 0.00  mean: 12.49

To learn more about model conversion options, more model testing tools and how to use the model in your own
application refer to :ref:`synap`.


