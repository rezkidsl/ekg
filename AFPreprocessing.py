import AFBwr as bwr

def signal_preprocessing(raw_signal):
    len_sample = len(raw_signal)
    sampled_window = len_sample

    clean_ecg = []
    squared = []
    baseline, raw_signal = bwr.bwr(raw_signal)

    filtered_lp = low_pass_filter(raw_signal)
    filtered_hp = high_pass_filter(filtered_lp)
    for i in range(sampled_window):
        clean_ecg.append(filtered_hp[i - 1])

    ecg_squared = signal_squared(filtered_hp)
    for i in range(len(ecg_squared)):
        squared.append(ecg_squared[i - 1])

    return raw_signal, clean_ecg, squared

def low_pass_filter(signal):
    result = []
    for index, value in enumerate(signal): # index = index value, value = signal value
        if index >= 1:
            value += 2 * result[index - 1]
        if index >= 2:
            value -= result[index - 2]
        if index >= 6:
            value -= 2 * signal[index - 6]
        if index >= 12:
            value += signal[index - 12]
        result.append(value)
    return result

def high_pass_filter(signal):
    result = []
    for index, value in enumerate(signal):
        value = -value
        if index >= 1:
            value -= result[index - 1]
        if index >= 16:
            value += 32 * signal[index - 16]
        if index >= 32:
            value += signal[index - 32]
        result.append(value)
    return result

def signal_squared(raw_signal):
    diff1 = []
    for i in range(len(raw_signal)-1):
        diff1.append(raw_signal[i+1] - raw_signal[i])
    diff2 = []
    for i in range(len(diff1)-1):
        diff2.append(diff1[i + 1] - diff1[i])
    result_squared = []
    for i in range(len(diff2)):
        result_squared.append(diff2[i] * diff2[i])
    return result_squared

