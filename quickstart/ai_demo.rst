Running a pre-converted neural network
======================================

.. highlight:: console

To run a image classification neural network on a random image using an evaluation kit:

1. Install a pre-built image and connect to the board as described :doc:`here <flash_image>`

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


To learn about other ai demos refer to :ref:`synap`.

