===================
USB Boot User Guide
===================

Astra Machina supports booting over the USB interface using USB :ref:`uboot`. USB boot is most commonly used for
performing software updates (see :ref:`firmware_update_usb`). But, Astra Machina also supports booting U-Boot or booting a minimal Linux environment.

USB Booting uses the ``astra-boot`` tool to load the boot images. The ``astra-boot`` tool is a lower level variant of the
`Astra Update <https://github.com/synaptics-astra/astra-update>`__ tool used for software update. Both tools are based on the ``astraupdate``
library, but ``astra-boot`` removes the update logic to only support booting.

Setting Up USB Boot
===================

Setting up ``astra-boot`` is the same as setting up ``astra-update`` (See :ref:`usb_boot_setup`). The ``astra-boot`` tool is included
in the `usb-tool <https://github.com/synaptics-astra/usb-tool>`__ repository in GitHub. Platform specific binaries are located in the
``bin/<plaform>`` directories.

Using ``astra-boot``
====================

The ``astra-boot`` tool requires the path to the `boot image <https://github.com/synaptics-astra/astra-update?tab=readme-ov-file#boot-images>`__.
It then loads the image and waits for a matching device to arrive.

In this example, the tool will boot the default SL1680 boot image. Once, booted the device will wait at the U-Boot prompt which
is accessed though the serial console.

::

    $ ./bin/linux/x86_64/astra-boot astra-usbboot-images/sl1680_suboot/
    Astra Boot

    Boot Image: sl1680 rdk (9930c714-375e-11f0-b558-0242ac110002)
        Secure Boot: genx
        Memory Layout: 4GB
        U-Boot Console: UART
        uEnt.txt Support: enabled
        U-Boot Variant: Synaptics U-Boot

    Waiting for Astra Device (06CB:00B1)

Custom Boot Commands
--------------------

After USB U-Boot starts, it will load a file called ``uEnv.txt``. This file contains a list of commands which U-Boot will run.
The default behavior is to create an empty ``uEnv.txt`` file which will halt booting at the U-Boot prompt. Custom commands can
be sent to U-Boot by creating a custom ``uEnv.txt`` file in the boot image directory or by setting the ``-o`` option.

In this example, U-Boot will load and then run the ``fastboot`` command which will load fastboot.

::

    ./bin/linux/x86_64/astra-boot -o "fastboot -l 0x10000000 -s 0x8000000 usb 0" astra-usbboot-images/sl1680_suboot/

When using the ``-o`` option, ``astra-boot`` will generate a ``uEnv.txt`` at runtime and place the command in the ``bootcmd`` line of the file.
More complicated ``uEnv.txt`` files should be created before running the tool and placed in the boot image directory.

Booting Linux
-------------

Astra Machina also supports booting a minimal Linux environment using the USB interface. Booting Linux requires a kernel image,
devicetree image, and a rootfs image. Custom images can be built using the :doc:`../yocto`. Building an image with the ``sl16XXusb``
machine type will generate all of the required image files. Prebuilt USB Linux Images are also available on the
`SDK Releases <https://github.com/synaptics-astra/sdk/releases>`__ page.

The USB Linux image needs a custom ``uEnv.txt`` file in order for U-Boot to load and boot Linux. The custom ``uEnv.txt``
file should be created in the boot image directory.

Here, is an example ``uEnv.txt`` which can boot the prebuilt ``sl1640_usb_boot`` image on SL1640.

::

    skip_fdt_update=6
    fdt_high=FFFFFFFFFFFFFFFF
    #bootargs=console=ttyS0,115200 root=/dev/ram0
    bootargs=shell earlycon console=ttyS0,115200 rootwait rootfstype=ext4
    loadimage=usbload platypus-rdk.dtb 0x17c00000;usbload Image.gz 0x10000000;
    loadramdisk=usbload ramdisk.cpio.gz 0x8c00000;
    setparam=setenv bootm_low 0x0;setenv bootm_size 0x10000000;
    setkernel=setenv kernel_comp_addr_r 0x7c00000; setenv kernel_comp_size $filesize;
    bootcmd=run setparam;run loadimage; run setkernel; run setkernel;run loadramdisk; booti 0x10000000 0x8c00000:$filesize 0x17c00000

Astra Machina will now boot using the provided Linux kernel and rootfs. A linux prompt ``#`` will appear on the serial console when booting
is complete.