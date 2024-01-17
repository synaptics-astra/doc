Quick start
***********

To get started with the Synaptics Astra SDK, you can do the following things:

.. highlight:: console

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

.. note::

    This doesn't work yet becaues v4l support is not merged yet on branch firebird

To play a video on a Synaptics Astra evaluation kit:

1. Install a pre-built image and connect to the board as described :ref:`here <quickstart_install>`

3. Connect the screen to the HDMI TX port of the board and power on the board

4. Connect the board to a local network with DHCP using the ethernet cable

5. Download a demo video to the board::

      $ wget https://download.blender.org/durian/trailer/sintel_trailer-720p.mp4

6. Play the video::

      $ XDG_RUNTIME_DIR=/run/user/0 WAYLAND_DISPLAY=wayland-1 \
            gst-launch-1.0 filesrc location=sintel_trailer-720p.mp4 do-timestamp=true ! \
            qtdemux name=demux demux.video_0 !  queue ! h264parse ! v4l2h264dec ! \
            waylandsink fullscreen=true demux.audio_0 ! \
            queue ! aacparse ! faad ! audioconvert ! alsasink device=hw:0,9


To learn about other multimedia demos refer to :ref:`multimedia_demos`.

.. _quickstart_ai_demos:

Run a neural network using hardware acceleration
================================================

To run a image classification neural network on a random image using an evaluation kit:

1. Install a pre-built image and connect to the board as described :ref:`here <quickstart_install>`

2. On the target first go to the model directory::

    $ cd /usr/share/synap/models/image_classification/imagenet/model/mobilenet_v2_1.0_224_quant/

3. Then test the model inference time using random inputs::

    $ synap_cli random
    Flush/invalidate: yes
    Loop period (ms): 0
    Network inputs: 1
    Network outputs: 1
    Input buffer: input size: 150528 : random
    Output buffer: output size: 1001

    Predict #0: 12.61 ms

    Inference timings (ms):  load: 28.37  init: 66.99  min: 12.60  median: 12.60  max: 12.60  stddev: 0.00  mean: 12.60


4. Then test the model accuracy with a sample image::

    $ synap_cli_ic ../../sample/goldfish_224x224.jpg

    Loading network: model.nb
    Input image: ../../sample/goldfish_224x224.jpg
    Classification time: 3.15 ms (pre:0.56, inf:2.53, post:0.05)
    Class  Confidence  Description
        1     18.9874  goldfish, Carassius auratus
      112      9.2959  conch
      927      8.7025  trifle
       29      8.2081  axolotl, mud puppy, Ambystoma mexicanum
      122      7.7136  American lobster, Northern lobster, Maine lobster, Homarus americanus


To learn about other ai demos refer to :ref:`ai_demos`.

Convert and test an AI model
============================

.. note::

    This example requires a host system with docker installed. See TODO for more details about the suggested
    configuration.

To convert your own AI model and run it on an evaluation kit use the following steps:

1. Install a pre-built image and connect to the board as described :ref:`here <quickstart_install>`

2. Connect the board to a local network with DHCP using the ethernet cable

3. Download ``1.tflite`` from `Kaggle <https://www.kaggle.com/models/tensorflow/mobilenet-v2/frameworks/tfLite/variations/1-0-224-quantized>`_

4. Install an alias in the shell of the host to run the SyNAP Toolkit container::

    $ alias synap_convert='docker run --rm -u $(id -u):$(id -g) -v $(pwd):$(pwd) --workdir $(pwd) ghcr.io/syna-astra/synap'

5. Convert the model with the default configuration by running the following command on the host::

    $ cd DIRECTORY_WITH_1.tflite

    $ synap_convert --model 1.tflite --target VS680 --out-format ebg --out-dir converted-model

   This command converts ``1.tflite`` to ``converted-model/1.nb`` and ``converted-model/1.json``, the model converted
   for execution on the evaluation kit.

5. Find the ip address of the board with the following command on the target::

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

6. Upload the converted model to the board by running the following command on the host::

    $  scp converted-model/model.json converted-model/model.nb root@192.168.1.110:/tmp

7. Then connect to the board and issue the following command::

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
