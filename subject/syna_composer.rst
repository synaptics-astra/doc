===============
Syna Compositor
===============

The **Syna Compositor Plugin** delivers foundational
capabilities for compositing multiple video streams in a GStreamer
pipeline. It supports dynamic pad management, basic layout, and
synchronized output rendering.

This release is focused on establishing core functionality of Syna
Compositor by using hardware capabilities.

Features
========

1. **Multiple Sink Pad Support**: Accepts dynamic sink pads (sink_%u) to
   ingest multiple input streams.

2. **Frame Synchronization**: Uses GstVideoAggregator to align incoming
   buffers based on timestamps.

3. **Basic Composition**: Composites input video streams using Open GL,
   based on provided layout.

4. **Custom Cap Negotiation**: Supports fixed caps (NV12 at input side
   and BGRA at output side).

5. **Zero Memory Copy at Sink Side:** DMABuf-backed input buffers are
   directly imported into OpenGL textures, eliminating CPU-side memory
   copies and improving performance and latency.

Syna Compositor Plugin Info
===========================

::

   Factory Details:
      Rank                     primary + 1 (257)
      Long-name                Syna Compositor
      Klass                    Filter/Editor/Video/SynaCompositor
      Description              Composite multiple video streams
      Author                   Synaptics Inc

   Plugin Details:
      Name                     synacompositor
      Description              synacompositor
      Filename                 /usr/lib/gstreamer-1.0/libgstsynacompositor.so
      Version                  1.22.8
      License                  LGPL
      Source module            gstreamer-plugins-syna
      Binary package           gstreamer-plugins-syna
      Origin URL               https://www.synaptics.com/

   GObject
   +----GInitiallyUnowned
         +----GstObject
               +----GstElement
                     +----GstAggregator
                           +----GstVideoAggregator
                                 +----GstSynaCompositor

   Implemented Interfaces:
      GstChildProxy

   Pad Templates:
      SINK template: 'sink_%u'
         Availability: On request
         Capabilities:
            video/x-raw(memory:DMABuf)
                     format: { (string)NV12, (string)NV12M }
                        width: [ 1, 2147483647 ]
                     height: [ 1, 2147483647 ]
                  framerate: [ 0/1, 2147483647/1 ]
            video/x-raw
                     format: { (string)NV12, (string)NV12M }
                        width: [ 1, 2147483647 ]
                     height: [ 1, 2147483647 ]
                  framerate: [ 0/1, 2147483647/1 ]
         Type: GstSynaCompositorPad
         Pad Properties:

            alpha               : Alpha of the picture
                                 flags: readable, writable, controllable
                                 Double. Range:               0 -               1 Default:               1

            emit-signals        : Send signals to signal data consumption
                                 flags: readable, writable
                                 Boolean. Default: false

            height              : Height of the picture
                                 flags: readable, writable, controllable
                                 Double. Range:               0 -            2160 Default:               0

            max-last-buffer-repeat: Repeat last buffer for time (in ns, -1=until EOS), behaviour on EOS is not affected
                                 flags: readable, writable, changeable in NULL, READY, PAUSED or PLAYING state
                                 Unsigned Integer64. Range: 0 - 18446744073709551615 Default: 18446744073709551615

            repeat-after-eos    : Repeat the last frame after EOS until all pads are EOS
                                 flags: readable, writable, controllable
                                 Boolean. Default: false

            width               : Width of the picture
                                 flags: readable, writable, controllable
                                 Double. Range:               0 -            3840 Default:               0

            xpos                : X Position of the picture
                                 flags: readable, writable, controllable
                                 Double. Range:               0 -            3840 Default:               0

            ypos                : Y Position of the picture
                                 flags: readable, writable, controllable
                                 Double. Range:               0 -            2160 Default:               0

            zorder              : Z Order of the picture
                                 flags: readable, writable, controllable
                                 Double. Range:              -1 -               1 Default:               0


   SRC template: 'src'
      Availability: Always
      Capabilities:
         video/x-raw(memory:DMABuf)
                  format: { (string)BGRA }
                     width: [ 1, 2147483647 ]
                  height: [ 1, 2147483647 ]
               framerate: [ 0/1, 2147483647/1 ]
         video/x-raw
                  format: { (string)BGRA }
                     width: [ 1, 2147483647 ]
                  height: [ 1, 2147483647 ]
               framerate: [ 0/1, 2147483647/1 ]
      Type: GstAggregatorPad
      Pad Properties:

         emit-signals        : Send signals to signal data consumption
                              flags: readable, writable
                              Boolean. Default: false


   Element has no clocking capabilities.
   Element has no URI handling capabilities.

   Pads:
   SRC: 'src'
      Pad Template: 'src'

   Element Properties:

   background          : Background Color of Compositor (in ARGB hex value)
                           flags: readable, writable, controllable
                           Unsigned Integer. Range: 0 - 4294967295 Default: 0

   emit-signals        : Send signals
                           flags: readable, writable
                           Boolean. Default: false

   force-live          : Always operate in live mode and aggregate on timeout regardless of whether any live sources are linked upstream
                           flags: readable, writable
                           Boolean. Default: false

   height              : Height of the Compositor
                           flags: readable, writable, controllable
                           Double. Range:               0 -            2160 Default:            1080

   latency             : Additional latency in live mode to allow upstream to take longer to produce buffers for the current position (in nanoseconds)
                           flags: readable, writable
                           Unsigned Integer64. Range: 0 - 18446744073709551615 Default: 0

   min-upstream-latency: When sources with a higher latency are expected to be plugged in dynamically after the aggregator has started playing, this allows overriding the minimum latency reported by the initial source(s). This is only taken into account when larger than the actually reported minimum latency. (nanoseconds)
                           flags: readable, writable
                           Unsigned Integer64. Range: 0 - 18446744073709551615 Default: 0

   name                : The name of the object
                           flags: readable, writable
                           String. Default: "synacompositor0"

   parent              : The parent of the object
                           flags: readable, writable
                           Object of type "GstObject"

   start-time          : Start time to use if start-time-selection=set
                           flags: readable, writable
                           Unsigned Integer64. Range: 0 - 18446744073709551615 Default: 18446744073709551615

   start-time-selection: Decides which start time is output
                           flags: readable, writable
                           Enum "GstAggregatorStartTimeSelection" Default: 0, "zero"
                              (0): zero             - GST_AGGREGATOR_START_TIME_SELECTION_ZERO
                              (1): first            - GST_AGGREGATOR_START_TIME_SELECTION_FIRST
                              (2): set              - GST_AGGREGATOR_START_TIME_SELECTION_SET

   width               : Width of the Compositor
                           flags: readable, writable, controllable
                           Double. Range:               0 -            3840 Default:            1920


   Element Signals:

   "samples-selected" :  void user_function (GstElement * object,
                                             GstSegment * arg0,
                                             guint64 arg1,
                                             guint64 arg2,
                                             guint64 arg3,
                                             GstStructure * arg4,
                                             gpointer user_data);



Example Pipeline
================

::

   gst-launch-1.0 synacompositor name=comp \
   sink_0::xpos=0 sink_0::ypos=0 sink_0::height=540 sink_0::width=960 \
   sink_1::xpos=0 sink_1::ypos=540 sink_1::height=540 sink_1::width=960 \
   sink_2::xpos=960 sink_2::ypos=0 sink_2::height=540 sink_2::width=960 \
   sink_3::xpos=960 sink_3::ypos=540 sink_3::height=540 sink_3::width=960 \
   ! waylandsink sync=false \
   multifilesrc loop=true caps=\"video/x-h264, framerate=25/1\" \
   location=/home/root/demos/videos/h264/sample_1_1080p.h264 ! h264parse ! \
   v4l2h264dec ! comp.sink_0 \
   multifilesrc loop=true caps=\"video/x-h264, framerate=25/1\" \
   location=/home/root/demos/videos/h264/sample_2_1080p.h264 ! h264parse ! \
   v4l2h264dec ! comp.sink_1 \
   multifilesrc loop=true caps=\"video/x-h264, framerate=25/1\" \
   location=/home/root/demos/videos/h264/sample_3_1080p.h264 ! h264parse ! \
   v4l2h264dec ! comp.sink_2 \
   multifilesrc loop=true caps=\"video/x-h264, framerate=25/1\" \
   location=/home/root/demos/videos/h264/sample_4_1080p.h264 ! h264parse ! \
   v4l2h264dec ! comp.sink_3

Performance Comparison with similar plugins
===========================================

+---------+------------------------------------+-----------------------------------------+-------------------+-------------------+
| Sr No   | Use Case                           | COMPOSITOR                              | GLVIDEOMIXER      | SYNACOMPOSITOR    |
+=========+====================================+===================+=====================+===================+===================+
|         |                                    | CPU               | GPU                 | CPU      | GPU    | CPU      | GPU    |
+---------+------------------------------------+-------------------+---------------------+----------+--------+----------+--------+
| 1.      | Composition of 4 videos            | 71%               | 6% (Not Considered  | 25%      | 45%    | 29%      | 20%    |
|         |                                    |                   |                     |          |        |          |        |
|         | (1920x1080 resolution) scaled      |                   | as this is not GPU  |          |        |          |        |
|         |                                    |                   |                     |          |        |          |        |
|         | and positioned to fit 4 quadrants  |                   | based compositor)   |          |        |          |        |
|         |                                    |                   |                     |          |        |          |        |
|         | of 1920x1080p display.             |                   |                     |          |        |          |        |
+---------+------------------------------------+-------------------+---------------------+----------+--------+----------+--------+

Known Issues
============

1. **Only DMABuf is Supported at Sink Side -** The compositor currently
   accepts only DMA-BUF backed input buffers at the sink pads. Support
   for other memory types (e.g., system memory or GLMemory) is not
   implemented. Pipelines using non-DMABuf buffers will fail or result
   in undefined behavior.

2. **Memory Leak on Pipeline Shutdown -** When the pipeline is stopped
   or the compositor element is removed, some internal resources are not
   fully released. This leads to memory leaks over time, especially if
   the pipeline is repeatedly started and stopped, and may eventually
   result in a crash.

Known Limitations
=================

1. **Fixed Input and Output Formats (NV12 → BGRA) -** Syna Compositor
   supports only NV12 as the input format and BGRA as the output format.
   There is no support for automatic format negotiation or color space
   conversion. Any input in a different format must be converted
   upstream (e.g., using videoconvert), and output format is fixed

2. **No Alpha Blending -** Alpha blending is not implemented. All input
   layers are treated as fully opaque, and any overlapping content will
   result in one layer completely overwriting the other. This limits
   support for transparency and soft edges in compositing.

3. **No Z-Order Support -** There is no functionality to define or
   modify the stacking (depth) order of input layers. Inputs are
   composited in the order in which their sink pads are added. As a
   result, users cannot control which layer appears in front or behind
   others.
