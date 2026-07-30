# SL2610 Devfreq Manual Test Guide

## NPU (f7600000.synpu)

### 1. Switch to userspace governor

```bash
echo userspace > /sys/class/devfreq/f7600000.synpu/governor
```

### 2. Check supported frequencies

```bash
cat /sys/class/devfreq/f7600000.synpu/available_frequencies
# 800000000 1000000000
```

### 3. Set NPU frequency

```bash
# Set to 1 GHz
echo 1000000000 > /sys/class/devfreq/f7600000.synpu/userspace/set_freq
```

#### Verify

```bash
cat /sys/class/devfreq/f7600000.synpu/cur_freq

# Set back to 800 MHz
echo 800000000 > /sys/class/devfreq/f7600000.synpu/userspace/set_freq

# Verify
cat /sys/class/devfreq/f7600000.synpu/cur_freq
```

### 4. Check Vcore

```bash
cat /sys/kernel/debug/regulator/regulator_summary | grep -A2 vcore
```

## GPU (f7980000.gpu)

### 1. Switch to userspace governor

```bash
echo userspace > /sys/class/devfreq/f7980000.gpu/governor
```

### 2. Check supported frequencies

```bash
cat /sys/class/devfreq/f7980000.gpu/available_frequencies
# 800000000 700000000
```

### 3. Set GPU frequency

```bash
# Set to 800 MHz
echo 800000000 > /sys/class/devfreq/f7980000.gpu/userspace/set_freq

# Verify
cat /sys/class/devfreq/f7980000.gpu/cur_freq

# Set back to 700 MHz
echo 700000000 > /sys/class/devfreq/f7980000.gpu/userspace/set_freq

# Verify
cat /sys/class/devfreq/f7980000.gpu/cur_freq
```

### 4. Check Vcore

```bash
cat /sys/kernel/debug/regulator/regulator_summary | grep -A2 vcore
```

## Expected Results

`cur_freq` changes to the requested frequency.

`vcore` changes according to the selected OPP.

Since **CPU, GPU and NPU share the same Vcore regulator**, the regulator voltage always reflects the **highest voltage requested** by any active device. For voltage verification, it is recommended to keep the other devices idle.