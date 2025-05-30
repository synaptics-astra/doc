=============================================================
Seamless Real-Time Communication with GStreamer's WebRTC Sink
=============================================================

Introduction
============

Astra revolutionizes real-time communication by tapping into GStreamer's
WebRTC sink, delivering lightning-fast, high-quality audio and video
streaming. Built on the robust GStreamer framework, Astra offers
developers a seamless, scalable solution for modern communication
demands.

Use Case
========

The WebRTC GStreamer plugin (``webrtcsink``) facilitates real-time
peer-to-peer media streaming through WebRTC technology. This plugin
allows GStreamer-based applications to transmit and receive audio and
video streams over WebRTC, incorporating essential features such as
built-in signaling, ICE (Interactive Connectivity Establishment),
STUN/TURN, and data channels.

Test
====

.. note::

   The plugin is included exclusively in the OOBE image.

To verify its functionality, please follow the steps outlined below:

Using the GStreamer ``webrtcsink`` plugin, we aim to stream audio and video
to an IP address. To enable seamless playback, we need a webpage that
integrates WebRTC to display the stream in real time. The webpage has
already been created and is available in the root filesystem directory,
specifically located at ``/home/root/demos/webrtc``.

Please add the below script to /home/root directory on the board, run
chmod +x syna-webrtc.sh and then execute it.

::

   #!/bin/bash

   FOLDER="/home/root/demos/SynaWebRTC"

   ip_addr=$(ifconfig eth0 | grep 'inet addr:' | awk -F: '{print $2}' | awk '{print $1}')
   echo "Copy this address and paste it into your web browser: http://$ip_addr:8000"

   cleanup() {
      echo -e "\nCleaning up background processes..."
      jobs -p | xargs -r kill -9
      exit 0
   }

   trap cleanup EXIT INT TERM

   # Start signalling server in background
   gst-webrtc-signalling-server &
   GST_SERVER_PID=$!

   # Start Python HTTP server if folder exists
   if [ -d "$FOLDER" ]; then
      echo "Folder exists. Starting HTTP server on port 8000..."
      python3 -m http.server 8000 -d "$FOLDER" &
      PYTHON_SERVER_PID=$!
   else
      echo "Folder not found: $FOLDER"
      cleanup
   fi

   show_menu() {
      echo "========== MENU =========="
      echo "1. VideoTestSrc"
      echo "2. Filesrc"
      echo "3. Camera"
      echo "4. Exit"
      echo "=========================="
      read -r -p "Choose an option [1-4]: " choice

      case $choice in
         1)
               echo "Running Sample Video and Audio..."
               GST_PLUGIN_FEATURE_RANK=v4l2vp8enc:NONE \
               gst-launch-1.0 webrtcsink name=ws videotestsrc ! ws. audiotestsrc ! ws. &
               wait
               ;;
         2)
               read -r -p "Enter exact file path: " loc
               if [ -f "$loc" ]; then
                  echo "File exists. Running command..."
                  GST_PLUGIN_FEATURE_RANK=v4l2vp8enc:NONE \
                  gst-launch-1.0 webrtcsink name=ws \
                  filesrc location="$loc" ! qtdemux name=demux \
                  demux.video_0 ! queue ! h264parse ! avdec_h264 ! videoconvert ! videoscale ! videorate ! \
                  video/x-raw,format=I420,width=640,height=360,framerate=30/1 ! ws. \
                  demux.audio_0 ! queue ! aacparse ! avdec_aac ! audioconvert ! audioresample ! \
                  audio/x-raw,format=S16LE,rate=48000,channels=2 ! ws. &
                  wait
               else
                  echo "[ERROR] File not found."
               fi
               ;;
         3)
               cam_path=$(v4l2-ctl --list-devices | awk '/usb/ {getline; print $1}')
               if [ -n "$cam_path" ]; then
                  echo "[SUCCESS] USB camera found at $cam_path. Running command..."
                  GST_PLUGIN_FEATURE_RANK=v4l2vp8enc:NONE \
                  gst-launch-1.0 webrtcsink name=ws \
                  v4l2src device="$cam_path" ! video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! \
                  videoconvert ! videoscale ! videorate ! \
                  video/x-raw,format=I420,width=640,height=480,framerate=30/1 ! ws. &
                  wait
               else
                  echo "[ERROR] USB camera not connected."
               fi
               ;;
         4)
               echo "Exiting..."
               cleanup
               ;;
         *)
               echo "Invalid option. Try again."
               ;;
      esac
   }

   while true; do
      show_menu
   done



After running the script, you will notice that an IP address is printed
in the console. Simply copy this address and paste it into any browser
you have, whether it's on your personal laptop or directly on the board
itself. Ensure that you are connected to the same network.

The IP address will resemble the following format:::

   <Board_IP_ADDR>:8000

Once you open the IP address in the browser, a webpage will appear with
a link located in the top-left corner. Click on this link to allow the
stream to render, and you will be able to view your video or audio
streaming.

Use Case Pipelines
==================

Below are some example pipelines that are integrated into the script.

1. Basic Gstreamer pipeline:

::

   GST_PLUGIN_FEATURE_RANK=v4l2vp8enc:NONE gst-launch-1.0 webrtcsink
   name=ws videotestsrc ! ws. audiotestsrc ! ws.

The command is a fundamental GStreamer command designed for streaming
video and audio test sources.

2. To stream a sample video, utilize the filesrc element. To play a
   file, please replace the location attribute in the command below with
   the correct file path.

::

   GST_PLUGIN_FEATURE_RANK=v4l2vp8enc:NONE gst-launch-1.0 webrtcsink
   name=ws filesrc location=demos/videos/mp4/astra_intro.mp4 ! qtdemux
   name=demux demux.video_0 ! queue ! h264parse ! avdec_h264 !
   videoconvert ! videoscale ! videorate !
   video/x-raw,format=I420,width=640,height=360,framerate=30/1 ! ws.
   demux.audio_0 ! queue ! aacparse ! avdec_aac ! audioconvert !
   audioresample ! audio/x-raw,format=S16LE,rate=48000,channels=2 ! ws.

3. To stream video from your camera, begin by identifying the camera and
   audio device after connecting it using the below commands:

::

   v4l2-ctl --list-devices

   arecord -l

Next, replace the ``CAM_DEVICE`` and ``AUDIO_DEVICE`` (ex: hw:1,0) variables
in the command below with the appropriate device name:

::

   GST_PLUGIN_FEATURE_RANK=v4l2vp8enc:NONE gst-launch-1.0 webrtcsink
   name=ws v4l2src device=<CAM_DEVICE> !
   video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 !
   videoconvert ! videoscale ! videorate !
   video/x-raw,format=I420,width=320,height=240,framerate=30/1 ! ws.
   alsasrc device=<AUDIO_DEVICE> !
   audio/x-raw,format=S16LE,rate=48000,channels=2 ! audioconvert !
   audioresample ! ws.

**We can design a diverse range of pipelines customized to meet our
unique requirements.**

.. note::

   For detailed information about the WebRTC plugin, please refer to the
   links provided below:
   https://gstreamer.freedesktop.org/documentation/rswebrtc/webrtcsink.html?gi-language=c

   The WebRTC plugin is now integrated into our Astra image. For more
   details, please refer to this commit.

   https://github.com/synaptics-astra/meta-synaptics/commit/778db26bad70895d94fd261da3688a82e3165eac
