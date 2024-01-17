Convert and test an AI model
============================

.. highlight:: console

.. note::

   In addition to the :ref:`prerequisites for flashing <flashing_prerequisites>` you also need a host with
   docker installed, an ethernet cable and a local network with DHCP

To convert your own AI model and run it on an evaluation kit use the following steps:

1. Install a pre-built image and connect to the board as described :doc:`here <flash_image>`

2. Connect the board to a local network using the ethernet cable

3. Download ``1.tflite`` from `Kaggle <https://www.kaggle.com/models/tensorflow/mobilenet-v2/frameworks/tfLite/variations/1-0-224-quantized>`_

4. Install an alias in the shell of the host to run the SyNAP Toolkit container::

    $ alias synap_convert='docker run --rm -u $(id -u):$(id -g) -v $(pwd):$(pwd) --workdir $(pwd) ghcr.io/syna-astra/synap'

5. Convert the model with the default configuration by running the following command on the host::

    $ cd DIRECTORY_WITH_1.tflite

    $ synap_convert --model 1.tflite --target VS680 --out-format ebg --out-dir converted-model

   This command converts ``1.tflite`` to ``converted-model/1.nb`` and ``converted-model/1.json``, the model converted
   for execution on the evaluation kit.

6. Find the ip address of the board with the following command on the target::

    # ifconfig eth0
    eth0      Link encap:Ethernet  HWaddr 22:0F:36:10:03:E7
              inet addr:192.168.1.110  Bcast:192.168.1.255  Mask:255.255.255.0
              inet6 addr: fe80::200f:36ff:fe10:3e7/64 Scope:Link
              inet6 addr: 2a02:1210:7c76:3a00:200f:36ff:fe10:3e7/64 Scope:Global
              UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
              RX packets:15720 errors:0 dropped:316 overruns:0 frame:0
              TX packets:1334 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:1000
              RX bytes:5226689 (4.9 MiB)  TX bytes:108559 (106.0 KiB)
              Interrupt:45 Base address:0xa000

7. Upload the converted model to the board by running the following command on the host::

    $  scp converted-model/model.json converted-model/model.nb root@192.168.1.110:/tmp

8. Then connect to the board and issue the following command::

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


