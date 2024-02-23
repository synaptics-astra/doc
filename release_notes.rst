*************
Release Notes
*************

.. highlight:: console

.. _v0.0.1:

Version 0.0.1
=============

Known issues
------------

System shell

    The build requires ``bash`` to be set as system shell ``/bin/sh``, this already configured in the crops docker that is the recommended build environment but is not by default the case on Ubuntu 22.04 LTS.
    
    To configure the default system shell to bash on Ubuntu 22.04 use the following command::

        $ echo 'dash dash/sh boolean false' | debconf-set-selections && DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash

Warnings during build

    During the build the following messages are displayed::
    
        WARNING: synasdk-tools-native-0.0.1+gitAUTOINC+5b2d1a4ff6-r1 do_unpack: Failed to find a git repository in WORKDIR: /home/astra-test/sdk/build-sl1680/tmp/work/x86_64-linux/synasdk-tools-native/0.0.1+gitAUTOINC+5b2d1a4ff6-r1
        WARNING: synasdk-security-0.0.1+gitAUTOINC+5b2d1a4ff6-r2 do_unpack: Failed to find a git repository in WORKDIR: /home/astra-test/sdk/build-sl1680/tmp/work/sl1680-poky-linux/synasdk-security/0.0.1+gitAUTOINC+5b2d1a4ff6-r2
         linux-firmware-syna-5.15.140-r0 do_package_qa: QA Issue: Recipe LICENSE includes obsolete licenses GPLv2 [obsolete-license]
    
    These warnings can be ignored.
