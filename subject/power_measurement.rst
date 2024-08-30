=====================================
Power Measurements with Astra Machina
=====================================

Later revisions of Astra Machina contain the two power monitor ICs which can be used to measure the current
and voltage of the system. Values can be read using the Linux Kernel's `Hardware Monitoring Interface <https://www.kernel.org/doc/html/v5.15/hwmon/index.html>`__.

Astra Machina uses the `TI INA220 Current and Power Monitor <https://www.ti.com/lit/ds/symlink/ina220.pdf>`__ and
`TI INA3221 Shunt and Bus Voltage Monitor <https://www.ti.com/lit/ds/symlink/ina3221.pdf>`__ ICs.

Documentation for the hwmon kernel drivers can be found here: `ina220 <https://www.kernel.org/doc/html/v5.15/hwmon/ina2xx.html>`__
and `ina3221 <https://www.kernel.org/doc/html/v5.15/hwmon/ina3221.html>`__.

Performing Measurements
=======================

Here is an example of reading Current (mA) channels on SL1640:

::

    cat /sys/class/hwmon/hwmon0/curr1_input （ina322）
    856

    cat /sys/class/hwmon/hwmon0/curr2_input （ina322）
    32

    cat /sys/class/hwmon/hwmon0/curr3_input （ina322）
    60

    cat /sys/class/hwmon/hwmon1/curr1_input （ina2xx）
    7

    cat /sys/class/hwmon/hwmon2/curr1_input （ina2xx）
    67

    cat /sys/class/hwmon/hwmon3/curr1_input（ina2xx）
    63

Here is an example of reading Bus voltage (mV) channels on SL1640:

::

    cat /sys/class/hwmon/hwmon0/in1_input （ina322）
    800

    cat /sys/class/hwmon/hwmon0/in2_input （ina322）
    840

    cat /sys/class/hwmon/hwmon0/in3_input （ina322）
    1104

    cat /sys/class/hwmon/hwmon1/in1_input （ina2xx）
    624

    cat /sys/class/hwmon/hwmon2/in1_input （ina2xx）
    3384

    cat /sys/class/hwmon/hwmon3/in1_input （ina2xx）
    1860

Here is an example of reading Power (uW) channels on SL1640:

::

    cat /sys/class/hwmon/hwmon1/power1_input
    0

    cat /sys/class/hwmon/hwmon2/power1_input
    220000

    class/hwmon/hwmon3/power1_input
    140000

In this example we can calculate total power:

    | 856 * 800 = 684800 uW
    | 32 * 840 = 26880 uW
    | 60  * 1104 = 66240 uW
    | Total Power = 1137920uW = 1138mW

Supported Boards
================

Initial versions of Astra Machina did not contain the power monitor ICs. The following table
shows the Core Modules and I/O boards which can be used for power measurement.

=======  ==============    ==============
SoC      Core Module       I/O Board
=======  ==============    ==============
SL1620   Rev D or later    Rev D or later
SL1640   Rev B or later    Rev D or later
SL1680   Rev C or later    Rev D or later
=======  ==============    ==============
