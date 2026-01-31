====================================
Motion Vector with the H.264 Encoder
====================================

Astra SDK scarthgap_6.12_v2.2.0 adds support for accessing motion vectors from the H.264 encoder used
by SL1640 and SL1680. 

The ``vpu`` driver adds a new control ``SYNA_V4L2_CID_VENC_ENABLE_METADATA_MV`` which can be set to enable motion
vector data. https://github.com/synaptics-astra/linux_6_12-drivers-synaptics/commit/fd6bca6bf70637aa267d2d36159f05ecfa97a979

This example sets the V4L2 Control ID and Value::

    ctrl.id = SYNA_V4L2_CID_VENC_ENABLE_METADATA_MV;
    ctrl.value = true;
    dbg("setting (%d): %u", id, ctrl.value);
    ret = ::ioctl(mFd, VIDIOC_S_CTRL, &ctrl);

Motion Vector Data can be accessed from the capture buffer::

    v4l2_buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    ret = ::ioctrl(mFd, VIDIOC_DQBUF, &v4l2_buf);
    v4l2_buf plane[0]:  encoded ES data
    v4l2_buf plane[1]:  motion vector data

This example prints the Motion Vector data to a file::

    int write_motion_vector(void *mv,                /* plane[1] address */
                            size_t size,             /* plane[1]payload */
                            uint32_t frameIdx,       /* v4l2_buf sequence */
                            uint32_t width, uint32_t height)
    {
        uint32_t i;
        uint32_t mbPerRow = (width + 15) / 16;
        uint32_t mbPerCol = (height + 15) / 16;
        uint32_t mbPerFrame = mbPerRow * mbPerCol;
        MVInfo_t *mbInfo = (MVInfo_t *)mv;
        if (!mFp || !mv)
            return 0;
        /* Print motion vector for every macroblock. */
        fprintf(mFp, "\npic=%d  MV full-pixel X,Y "
                "for %d macroblocks (%dx%d) block=0\n",
                frameIdx, mbPerFrame, mbPerRow, mbPerCol);
        for (i = 0; i < mbPerFrame; i++) {
            uint32_t mb_type = mbInfo[i].mbType;
            uint32_t mb_y = i / mbPerRow;
            uint32_t mb_x = i % mbPerRow;
            uint32_t sx = mb_x * 16;
            uint32_t sy = mb_y * 16;
            fprintf(mFp, " MBxy:(%3d,%3d) Type:%8s ", sx, sy, mbModetostr(mb_type));
            if (mb_type == 6) { // P16x16
                fprintf(mFp, "MV(%3d,%3d )[%21s]", mbInfo[i].mvX[0], mbInfo[i].mvY[0], " ");
            } else if (mb_type == 7 || mb_type == 8) { // P16x8, P8x16
                fprintf(mFp, "MV(%3d,%3d ", mbInfo[i].mvX[0], mbInfo[i].mvY[0]);
                fprintf(mFp, "%3d,%3d) [%13s]", mbInfo[i].mvX[1], mbInfo[i].mvY[1], " ");
            } else if (mb_type == 9) { // P8x8
                fprintf(mFp, "MV(%3d,%3d ", mbInfo[i].mvX[0], mbInfo[i].mvY[0]);
                fprintf(mFp, "%3d,%3d ", mbInfo[i].mvX[1], mbInfo[i].mvY[1]);
                fprintf(mFp, "%3d,%3d ", mbInfo[i].mvX[2], mbInfo[i].mvY[2]);
                fprintf(mFp, "%3d,%3d)", mbInfo[i].mvX[3], mbInfo[i].mvY[3]);
            } else {
                fprintf(mFp, "MV[%31s]", " ");
            }
            if ((i % mbPerRow) == mbPerRow-1) fprintf(mFp, "\n");
        }
        fflush(mFp);
        return 0;
    }