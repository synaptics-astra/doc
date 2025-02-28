==================================================
Astra Machina Video Decode and Encode Capabilities
==================================================

Astra Machina Decode Capabilities
=================================

+-----------------+----------------------------------------------+----------------------------------------------+
| Formats         | H.264 Decoding                               | H.265 Decoding                               |
+=================+================+=================+===========+================+=================+===========+
|                 | SL1680         | SL1640          | SL1620    | SL1680         | SL1640          | SL1620    |
|                 |                |                 |           |                |                 |           |
|                 | HW Accelerated | HW Accelerated  | FFMPEG SW | HW Accelerated | HW Accelerated  | FFMPEG SW |
|                 |                |                 |           |                |                 |           |
+-----------------+----------------+-----------------+-----------+----------------+-----------------+-----------+
| 3840x2160\@60   |     Yes        |     Yes         |    No     |     Yes        |     Yes         |    No     |
+-----------------+----------------+-----------------+-----------+----------------+-----------------+-----------+
| 4x1920x1080\@60 |     Yes        |     Yes         |    No     |     Yes        |     Yes         |    No     |
+-----------------+----------------+-----------------+-----------+----------------+-----------------+-----------+
| 3x1920x1080\@60 |     Yes        |     Yes         |    No     |     Yes        |     Yes         |    No     |
+-----------------+----------------+-----------------+-----------+----------------+-----------------+-----------+
| 2x1920x1080\@60 |     Yes        |     Yes         |    No     |     Yes        |     Yes         |    No     |
+-----------------+----------------+-----------------+-----------+----------------+-----------------+-----------+
| 4x1920x1080\@30 |     Yes        |     Yes         |    No     |     Yes        |     Yes         |    No     |
+-----------------+----------------+-----------------+-----------+----------------+-----------------+-----------+
| 1x1920x1080\@30 |     Yes        |     Yes         |    Yes    |     Yes        |     Yes         |    No     |
+-----------------+----------------+-----------------+-----------+----------------+-----------------+-----------+
| 1x1920x1080\@24 |     Yes        |     Yes         |    Yes    |     Yes        |     Yes         |    Yes    |
+-----------------+----------------+-----------------+-----------+----------------+-----------------+-----------+
| 9x1280x720\@25  |     Yes        |     Yes         |    No     |     Yes        |     Yes         |    No     |
+-----------------+----------------+-----------------+-----------+----------------+-----------------+-----------+
| 9x640x480\@25   |     Yes        |     Yes         |    No     |     Yes        |     Yes         |    No     |
+-----------------+----------------+-----------------+-----------+----------------+-----------------+-----------+
| 16x640x480\@25  |     Yes        |       No        |    No     |     Yes        |       No        |    No     |
+-----------------+----------------+-----------------+-----------+----------------+-----------------+-----------+
| 2x1280x720\@30  |     Yes        |     Yes         |    Yes    |     Yes        |     Yes         |    Yes    |
+-----------------+----------------+-----------------+-----------+----------------+-----------------+-----------+

.. note::

    - Measured using actual conditions, using GStreamer pipelines for decoding, composition, and display. Output
      was displayed with Wayland Desktop. Please refer to the datasheet for standalone capabilities of the Video
      decoder IP block.

    - In case of multiple video mixing, graphics content is set at 2K for SL1680/SL1640 and 1280x800 for SL1620.

    - For the consistency, cpufreq set to userspace and configured to be max.
      (SL1620: 1900000, SL1640: 2000000, SL1680: 2100000)

Astra Machina Encode Capabilities
=================================

+-----------------+------------------------------------------------+
| Formats         | H.264 Encoding                                 |
+=================+========================+=======================+
|                 | SL1680                 | SL1640                |
|                 |                        |                       |
|                 | HW Accelerated         | HW Accelerated        |
+-----------------+------------------------+-----------------------+
| 2x1920x1080\@60 |        Yes             |        No             |
+-----------------+------------------------+-----------------------+
| 3x1920x1080\@30 |        Yes             |        No             |
+-----------------+------------------------+-----------------------+
| 1x1920x1080\@30 |        Yes             |        Yes            |
+-----------------+------------------------+-----------------------+
| 7x1280x720\@30  |        Yes             |        No             |
+-----------------+------------------------+-----------------------+
| 2x1280x720\@30  |        Yes             |        Yes            |
+-----------------+------------------------+-----------------------+

.. note::

  Tested using the raw stream from HRX is being encoded for SL1680, while a video test source 
  (videotestsrc) is utilized for SL1640, with the data being dumped to a fakesink.

Astra Machina Simultaneous Encoding and Decoding Capabilities
=============================================================

+--------------------------+------------------------------------------------+
| Formats                  | H.264 Encoding                                 |
+==========================+========================+=======================+
|                          | SL1680                 | SL1640                |
|                          |                        |                       |
|                          | HW Accelerated         | HW Accelerated        |
+--------------------------+------------------------+-----------------------+
| Usecase #1               |       Yes              |          No           |
| Decode: 3x1920x1080\@60  |                        |                       |
| Encode: 1x1920x1080\@60  |                        |                       |
+--------------------------+------------------------+-----------------------+
| Usecase #2               |       Yes              |          No           |
| Decode: 6x1920x1080\@30  |                        |                       |
| Encode: 3x1920x1080\@30  |                        |                       |
+--------------------------+------------------------+-----------------------+
| Usecase #3               |       Yes              |          No           |
| Decode: 9x1280x720\@30   |                        |                       |
| Encode: 6x1280x720\@30   |                        |                       |
+--------------------------+------------------------+-----------------------+
| Usecase #4               |       Yes              |         Yes           |
| Decode: 7x1920x1080\@30  |                        |                       |
| Encode: 1x1920x1080\@30  |                        |                       |
+--------------------------+------------------------+-----------------------+
| Usecase #5               |       Yes              |         Yes           |
| Decode: 9x1280x720\@30   |                        |                       |
| Encode: 2x1280x720\@30   |                        |                       |
+--------------------------+------------------------+-----------------------+

Sample Gstreamer pipelines
--------------------------

Usercase #1:

::

  gst-launch-1.0 \
    v4l2src device=/dev/video7 ! video/x-raw,framerate=60/1,width=1920,height=1080 ! \
    tee name= t \
    t. ! queue ! v4l2h264enc ! h264parse ! fakesink \
    filesrc location=Sample_1080p60.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink \
    filesrc location=Sample_1080p60.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink \
    filesrc location=Sample_1080p60.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink

Usercase #2:

::

  gst-launch-1.0 \
    v4l2src device=/dev/video7 ! video/x-raw,framerate=30/1,width=1920,height=1080 ! tee name=t \
    t. ! queue ! v4l2h264enc ! h264parse ! fakesink \
    t. ! queue ! v4l2h264enc ! h264parse ! fakesink \
    t. ! queue ! v4l2h264enc ! h264parse ! fakesink \
    filesrc location=Sample_1080p30.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink \
    filesrc location=Sample_1080p30.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink \
    filesrc location=Sample_1080p30.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink \
    filesrc location=Sample_1080p30.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink \
    filesrc location=Sample_1080p30.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink \
    filesrc location=Sample_1080p30.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink

Usecase #4:

::

  gst-launch-1.0 videotestsrc is-live=true do-timestamp=true num-buffers=300 blocksize=3110400 ! \
      video/x-raw,format=NV12,width=1920,height=1080,framerate=30/1 ! tee name=t \
      t. ! queue ! v4l2h264enc ! video/x-h264,stream-format=byte-stream,alignment=au,profile=high ! h264parse ! fakesink \
      filesrc location=sample_1080p30.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink \
      filesrc location=sample_1080p30.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink \
      filesrc location=sample_1080p30.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink \
      filesrc location=sample_1080p30.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink \
      filesrc location=sample_1080p30.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink \
      filesrc location=sample_1080p30.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink \
      filesrc location=sample_1080p30.mp4 ! qtdemux ! h264parse ! v4l2h264dec ! queue ! waylandsink 

.. note::

  To verify performance for codec block, basic GStreamer pipelines were executed.  Adding extra overhead of video mixer
  or memory copy may impact the codec performance depending on usecase.