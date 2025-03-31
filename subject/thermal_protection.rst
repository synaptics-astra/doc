=======================================
CPU Thermal Protection on Astra Machina
=======================================

Astra Machina uses the Linux Kernel's Thermal Framework to limit CPU speed to prevent the CPU from overheating. Astra Machina
defines two level protection policy.

* If the CPU reaches temperatures greater than 105°C, the thermal framework will trigger a ``cpu_alert`` protection. This will cause
  the CPUFreq subsystem to reduce the clock frequency of the CPU to reduce the temperature.

* If the CPU reaches a temperature greater than 110°C, the thermal framework will trigger a ``cpu_critical`` protection. This will cause
  the kernel to shutdown the device to prevent overheating.

Device Tree Configuration
=========================

The Thermal Zones and trips are defined in platform dts files located in ``build-sl1680/workspace/sources/linux-syna/arch/arm64/boot/dts/synaptics``.

+-----------------+---------------+------------------+-----------------+
|                 | SL1620        | SL1640           | SL1680          |
+-----------------+---------------+------------------+-----------------+
| DTS             | myna2.dtsi    | platypus.dtsi    | dolphin.dtsi    |
+-----------------+---------------+------------------+-----------------+

Documentation on Thermal Zones in Device Tree can be found `here <https://web.git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/devicetree/bindings/thermal/thermal-zones.yaml?h=v5.15.140>`__.

Userspace Controls
==================

The ``cpu_alert`` and ``cpu_critical`` temperature thresholds can be adjusted using the ``thermal`` sysfs interface.

Set the ``cpu_alert`` threshold by writing a value to ``/sys/class/thermal/thermal_zone0/trip_point_0_temp``. To set the
``cpu_critical`` threshold, write a value to ``/sys/class/thermal/thermal_zone0/trip_point_1_temp``.

The temperature value is in  millidegrees Celsius. This example sets the threshold to 30°C.

::

    echo 30000 > /sys/class/thermal/thermal_zone0/trip_point_0_temp

To test that the thermal policy is working you can check the current CPU frequency, set the 30°C threshold, and then check
the current CPU frequency again. Since, 30°C is a low threshold, the current CPU frequency should be reduced.

::

    cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
    echo 30000 > /sys/class/thermal/thermal_zone0/trip_point_0_temp
    cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq