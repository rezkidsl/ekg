def signal_feature_extraction(data_ecg, sample_squared):

    list_peak_squared = detect_peak_squared(sample_squared)
    list_r_candidate = detect_R_candidates(data_ecg, list_peak_squared)
    list_RR = detect_True_R (data_ecg, list_r_candidate)
    list_qrs = detect_qrs(data_ecg, list_RR)
    return list_peak_squared, list_r_candidate, list_qrs

def detect_peak_squared (sample_squared):
    sample_squared_max = max(sample_squared)
    th_peak_squared = 0.03 * sample_squared_max # 3% Deboolena(2012)
    list_peak_squared = []
    search_peak_squared = []

    for i in range(len(sample_squared)):
        if (sample_squared[i] > th_peak_squared):
            if (len(search_peak_squared) == 0):
                search_peak_squared.append(sample_squared[i])
            else:
                search_peak_squared.append(sample_squared[i])
                if (i == len(sample_squared)-1):
                    seeked_peak = max(search_peak_squared)
                    index_peak = sample_squared.index(seeked_peak)
                    list_peak_squared.append([index_peak, seeked_peak])
                    search_peak_squared = []
                else:
                    if (sample_squared[i + 1] < th_peak_squared):
                        seeked_peak = max(search_peak_squared)
                        index_peak = sample_squared.index(seeked_peak)
                        list_peak_squared.append([index_peak, seeked_peak])
                        search_peak_squared = []
    return list_peak_squared

def detect_R_candidates(data_ecg, list_peak_squared):
    # data_ecg = [index_time, index_time_cv, data_signal]
    list_r_candidate = []
    for i in range(len(list_peak_squared)):
        index_peak = list_peak_squared[i][0]
        R_left = data_ecg[index_peak][2]
        index_left = index_peak
        if data_ecg[index_left-1][2] >= R_left:
            while data_ecg[index_left-1][2] >= R_left:
                index_left = index_left - 1
                R_left = data_ecg[index_left][2]
                if index_left-1 < 0:
                    break

        R_right = data_ecg[index_peak][2]
        index_right = index_peak
        if data_ecg[index_right+1][2] >= R_right:
            while data_ecg[index_right+1][2] >= R_right:
                index_right = index_right + 1
                R_right = data_ecg[index_right][2]
                if index_right+1 > len(data_ecg)-1:
                    break

        if R_left >= R_right:
            R_peak = R_left
            index_R = index_left
        else:
            R_peak = R_right
            index_R = index_right

        index_time = 0
        RR = 0
        R_peak = float(R_peak)
        list_r_candidate.append([index_time, index_R, R_peak, RR])

    # LOOKING FOR TWIN R PEAK
    false_R = list_r_candidate.copy()
    list_r_candidate = []
    prev_R_peak = false_R[0][2]
    for i in range(len(false_R)):
        index_R = false_R[i][1]
        R_peak = false_R[i][2]
        if i > 0:
            if R_peak == prev_R_peak:
                prev_R_peak = R_peak
            else:
                prev_R_peak = R_peak
                list_r_candidate.append([0, index_R, R_peak, 0])
        else:
            list_r_candidate.append([0, index_R, R_peak, 0])

    # LOOKING FOR R CANDIDATES RR INTERVAL
    # data_ecg.append([index_time, index_time_cv, data_signal, anotasi_signal])
    for i in range(len(list_r_candidate)):
        index_R = list_r_candidate[i][1]
        if (i == 0):
            index_time = data_ecg[index_R][1]
            RR = index_time - data_ecg [0][1]
            list_r_candidate[i][0] = index_time
            list_r_candidate[i][3] = RR
        else:
            prev_index_R = list_r_candidate[i - 1][1]
            index_time = data_ecg[index_R][1]
            prev_index_time = data_ecg[prev_index_R][1]
            RR = index_time - prev_index_time
            list_r_candidate[i][0] = index_time
            list_r_candidate[i][3] = RR

    return list_r_candidate

def detect_True_R (data_ecg, list_r_candidate):
    list_RR = []
    # LOOKING FOR TRUE R PEAK
    i_r = []
    search_r = []
    # QRS window = +- 75ms (0,075s), QRS width 150ms (0.15s), Heartrate normal = 60-100 bpm (0.6-1 bps)
    # th_rr = 0.075
    # th_rr = 0.15
    th_rr = 0.3
    for i in range(len(list_r_candidate)):
        RR = list_r_candidate[i][3]
        if (RR <= th_rr):
            i_r.append(list_r_candidate[i][1])
            search_r.append(list_r_candidate[i][2])
        else:
            if (len(search_r) == 0):
                i_r.append(list_r_candidate[i][1])
                search_r.append(list_r_candidate[i][2])
            else:
                seeked_peak = max(search_r)
                in_search_r = search_r.index(seeked_peak)
                index_peak = i_r[in_search_r]
                list_RR.append([0, index_peak, seeked_peak, 0])
                i_r = []
                search_r = []

                i_r.append(list_r_candidate[i][1])
                search_r.append(list_r_candidate[i][2])

        if (i == len(list_r_candidate) - 1):
            seeked_peak = max(search_r)
            in_search_r = search_r.index(seeked_peak)
            index_peak = i_r[in_search_r]
            list_RR.append([0, index_peak, seeked_peak, 0])
            i_r = []
            search_r = []

    return list_RR

def detect_qrs(data_ecg, list_RR):
    # LOOKING FOR RR INTERVAL
    for i in range(len(list_RR)):
        index_peak = list_RR[i][1]
        if (i == 0):
            index_time = data_ecg[index_peak][1]
            RR = index_time - data_ecg[0][1]
            list_RR[i][0] = index_time
            list_RR[i][3] = RR
        else:
            prev_index_peak = list_RR[i - 1][1]
            index_time = data_ecg[index_peak][1]
            prev_index_time = data_ecg[prev_index_peak][1]
            RR = index_time - prev_index_time
            list_RR[i][0] = index_time
            list_RR[i][3] = RR

    list_qrs = []
    # LOOKING FOR Q AND S PEAK
    for i in range(len(list_RR)):
        index_R = list_RR[i][1]
        R_peak = list_RR[i][2]
        RR_interval = list_RR[i][3]

        # Q PEAK
        index_Q = list_RR[i][1]
        Q_peak = data_ecg[index_Q][2]
        while index_Q - 1 >= 0:
            if Q_peak > data_ecg[index_Q - 1][2]:
                Q_peak = data_ecg[index_Q - 1][2]
                index_Q = index_Q - 1
            else:
                break

        # S PEAK
        index_S = list_RR[i][1]
        S_peak = data_ecg[index_S][2]
        while index_S+1 <= (len(data_ecg)-1):
            if S_peak > data_ecg[index_S + 1][2]:
                S_peak = data_ecg[index_S + 1][2]
                index_S = index_S + 1
            else:
                break

        # QRS WIDTH
        qrs_width = data_ecg[index_S][1]-data_ecg[index_Q][1]
        index_P = 0
        P_peak = 0
        index_T = 0
        T_peak = 0
        TP = 0
        PQ = 0
        anotasi = 0
        list_qrs.append([[index_P, P_peak],[index_Q, Q_peak], [index_R, R_peak], [index_S, S_peak], [index_T, T_peak],
                         RR_interval, qrs_width, TP, PQ, anotasi])

        # LOOKING FOR P AND T PEAK
        # T wave 15-55% of RR interval
        # P wave 65-95% of RR interval
        index_Q = list_qrs[i][1][0]
        if (i == 0):
            i_t_on = data_ecg[0][1] + (RR_interval * 15 / 100)
            i_t_off = data_ecg[0][1] + (RR_interval * 55 / 100)
            i_p_on = data_ecg[0][1] + (RR_interval * 65 / 100)
            i_p_off = data_ecg[index_Q - 2][1]

            j = 0
            index_T = j
            index_P = j

            index_time_t = data_ecg[0][1]
            T_peak = data_ecg[j][2]

        else:
            prev_index_time_R = list_RR[i-1][0]
            i_t_on = prev_index_time_R + (RR_interval * 15 / 100)
            i_t_off = prev_index_time_R + (RR_interval * 55 / 100)
            i_p_on = prev_index_time_R + (RR_interval * 65 / 100)
            # i_p_off = prev_index_time_R + (RR_interval * 95 / 100)
            index_Q = list_qrs[i][1][0]
            i_p_off = data_ecg[index_Q-2][1]

            j = list_RR[i - 1][1]
            index_T = j
            index_P = j

            index_time_t = list_RR[i - 1][0]
            T_peak = list_qrs[i-1][3][1]

        while index_time_t <= i_t_off and j < (len(data_ecg) - 1):
            if index_time_t >= i_t_on and index_time_t <= i_t_off:
                if T_peak <= data_ecg[j + 1][2]:
                    T_peak = data_ecg[j + 1][2]
                    index_T = j + 1
            else:
                T_peak = data_ecg[j + 1][2]
                index_T = j + 1
            index_time_t = data_ecg[j + 1][1]
            j = j + 1

        k = index_T+1
        P_peak = data_ecg[k][2]
        index_time_p = data_ecg[k][1]
        while index_time_p < i_p_off and k < (len(data_ecg) - 1):
            if index_time_p >= i_p_on and index_time_p <= i_p_off:
                if P_peak <= data_ecg[k + 1][2]:
                    P_peak = data_ecg[k + 1][2]
                    index_P = k + 1
            else:
                P_peak = data_ecg[k + 1][2]
                index_P = k + 1
            index_time_p = data_ecg[k + 1][1]
            k = k + 1

        if (i == 0):
            list_qrs[i][0][0] = index_P
            list_qrs[i][0][1] = P_peak
        elif (i == len(list_RR)-1):
            list_qrs[i-1][4][0] = index_T
            list_qrs[i-1][4][1] = T_peak
        else:
            list_qrs[i][0][0] = index_P
            list_qrs[i][0][1] = P_peak
            list_qrs[i-1][4][0] = index_T
            list_qrs[i-1][4][1] = T_peak

            TP = data_ecg[index_P][1] - data_ecg[index_T][1]
            PQ = data_ecg[index_Q][1] - data_ecg[index_P][1]
            list_qrs[i][7] = TP
            list_qrs[i][8] = PQ

    return list_qrs




