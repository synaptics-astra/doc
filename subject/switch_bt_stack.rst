=============================
Switching the Bluetooth Stack
=============================

Astra uses ``bluez`` as the default bluetooth stack. Some advanced Bluetooth
features can only be supported using the Synaptics BTD Bluetooth stack. This
guide describes how to disable the ``bluez`` stack so that the hardware is available
for use with BTD.

Disable ``bluez`` at Runtime
----------------------------

Check that if the ``brcm`` and ``bluealsa`` processes are running.

::

    ps | grep -E 'brcm_patchram_plus|bluealsa' | grep -v grep

The following processes should be printed.

::

    /usr/bin/brcm_patchram_plus -d --tosleep=300000 --baudrate 3000000 --use_baudrate_for_download --no2bytes --enable_hci --patchram /lib/firmware/bcm /dev/ttyS1
    /usr/bin/bluealsa --profile=a2dp-source --profile=a2dp-sink --profile=hfp-hf --profile=hfp-ag


Disable the ``brcm_bt_start`` service.

::

    systemctl disable brcm_bt_start.service

Wait 3 seconds and then reboot.

After rebboting check to see if the ``brcm`` and ``bluealsa`` processes are running.

::

    ps | grep -E 'brcm_patchram_plus|bluealsa' | grep -v grep

You should not see any output.

Disable ``bluez`` in the Build
-------------------------------

To disable ``brcm_bt_start`` during the build process you need to add a line to
``meta-synaptics/recipes-devtools/synasdk/synasdk-brcm-bt-start_git.bb`` to stop the
service from starting.

::

    diff --git a/recipes-devtools/synasdk/synasdk-brcm-bt-start_git.bb b/recipes-devtools/synasdk/synasdk-brcm-bt-start_git.bb
    index 847de9ba..45cb3e03 100644
    --- a/recipes-devtools/synasdk/synasdk-brcm-bt-start_git.bb
    +++ b/recipes-devtools/synasdk/synasdk-brcm-bt-start_git.bb
    @@ -41,6 +41,8 @@ do_install() {
        fi
    }

    +SYSTEMD_AUTO_ENABLE ?= "disable"
    +
    SYSTEMD_SERVICE:${PN} += "${@bb.utils.contains('DISTRO_FEATURES', 'bluetooth', 'brcm_bt_start.service', '', d)}"
    INITSCRIPT_NAME:${PN} = "brcm_bt_start"
    INITSCRIPT_PACKAGES = "${PN}"

