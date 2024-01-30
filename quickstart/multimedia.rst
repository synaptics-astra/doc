Play a video with hardware acceleration
========================================

.. highlight:: console

To play a video on a Synaptics Astra evaluation kit:

1. Install a pre-built image and connect to the board as described :doc:`here <flash_image>`

2. Connect the screen to the HDMI TX port of the board and power on the board

3. Connect the board to a local network with DHCP using the ethernet cable

4. Download a demo video to the board::

      $ wget https://download.blender.org/durian/trailer/sintel_trailer-720p.mp4

5. Play the video::

      $ export XDG_RUNTIME_DIR=/run/user/0
      $ export WAYLAND_DISPLAY=wayland-1
      $ gst-launch-1.0 filesrc location=sintel_trailer-720p.mp4 ! demux ! queue ! parser ! decoder ! videosink

To learn about other multimedia demos refer to :ref:`multimedia`.

