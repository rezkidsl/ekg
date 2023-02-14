import AFPreprocessing as pre
import AFFeatureExtraction as fe
import numpy as np
import matplotlib.pyplot as plt
# from tqdm import tqdm

def convert_time(data_time):
    # 00:00:14.940:1 --> example of the time format in the dataset file
    t = data_time.split(":")
    Hours = float(t[0]) * 3600
    Minute = float(t[1]) * 60
    Second = float(t[2])
    if len(t) == 4:
        
        Day = float(t[3]) * 86400
    else:
        Day = 0
    index_t = Day + Hours + Minute + Second
    return index_t

def dataset_reading (path, data, signal_type): # signal type = ECG1 or ECG2, ECG1 = 1 and ECG2 = 2
    data_ecg = path + data + '.csv'
    data_title = data
    f = open(data_ecg, 'r')
    lines = f.readlines()
    f.close()

    raw_signal = []
    for i in range(len(lines)-1):
        raw_signal.append(float(lines[i + 1].split(',')[signal_type]))
    return raw_signal, lines, data_title

def AF_SP(path_training, data_training, signal_type):
    total_qrs = []
    total_qrs.append(['maxRR','minRR','meanRR','stdevRR','maxQRS','minQRS','meanQRS','stdevQRS','maxTP','minTP','meanTP','stdevTP',
                      'maxPQ','minPQ','meanPQ','stdevPQ'])
    for i in range(len(data_training)):
        # ECG DATASET READING
        raw_signal, lines, data_title = dataset_reading(path_training, data_training[i], signal_type)
        
        # PREPROCESSING
        raw_signal, clean_ecg, sample_squared = pre.signal_preprocessing(raw_signal)

        data_ecg = []
        print(data_title) 
        for j in range(len(lines) - 1):
            index_time = str(lines[j + 1].split(',')[0])
            
            index_time_cv = convert_time(index_time)
            
            data_signal = clean_ecg[j]
            data_ecg.append([index_time, index_time_cv, data_signal])

        # FEATURE EXTRACTION
        list_peak_squared, list_r_candidate, list_qrs = fe.signal_feature_extraction(data_ecg, sample_squared)
        list_baru_RR = []
        list_baru_qrs = []
        list_baru_TP = []
        list_baru_PQ = []
        for j in range(len(list_qrs)):
            RR_interval = list_qrs[j][5]
            QRS_width = list_qrs[j][6]
            TP_TP = list_qrs[j][7]
            PQ_PQ = list_qrs[j][8]
            list_baru_RR.append(RR_interval)
            list_baru_qrs.append(QRS_width)
            list_baru_TP.append(TP_TP)
            list_baru_PQ.append(PQ_PQ)

        # RR Interval
        maxRR = max(list_baru_RR)
        minRR = min(list_baru_RR)
        meanRR = np.mean(list_baru_RR)
        stdevRR = np.std(list_baru_RR)

        # QRS Duration
        maxQRS = max(list_baru_qrs)
        minQRS = min(list_baru_qrs)
        meanQRS = np.mean(list_baru_qrs)
        stdevQRS = np.std(list_baru_qrs)

        # TP Duration
        maxTP = max(list_baru_TP)
        minTP = min(list_baru_TP)
        meanTP = np.mean(list_baru_TP)
        stdevTP = np.std(list_baru_TP)

        # PQ Duration
        maxPQ = max(list_baru_PQ)
        minPQ = min(list_baru_PQ)
        meanPQ = np.mean(list_baru_PQ)
        stdevPQ = np.std(list_baru_PQ)

        total_qrs.append([maxRR,minRR,meanRR,stdevRR,maxQRS,minQRS,meanQRS,stdevQRS,maxTP,minTP,meanTP,stdevTP,maxPQ,minPQ,meanPQ,stdevPQ])

        # SHOWING ECG PLOT
        # ecg_plot(data_title, raw_signal, clean_ecg, list_qrs)
        # plt.show()
    return total_qrs

def make_fiture(lines, signal_type):
    raw_signal = []
    for i in range(len(lines)-1):
        raw_signal.append(float(lines[i + 1].split(',')[signal_type]))
    # PREPROCESSING
    raw_signal, clean_ecg, sample_squared = pre.signal_preprocessing(raw_signal)

    data_ecg = []
    for j in range(len(lines) - 1):
        index_time = str(lines[j + 1].split(',')[0])
        
        index_time_cv = convert_time(index_time)
        
        data_signal = clean_ecg[j]
        data_ecg.append([index_time, index_time_cv, data_signal])

    # FEATURE EXTRACTION
    list_peak_squared, list_r_candidate, list_qrs = fe.signal_feature_extraction(data_ecg, sample_squared)
    list_baru_RR = []
    list_baru_qrs = []
    list_baru_TP = []
    list_baru_PQ = []
    for j in range(len(list_qrs)):
        RR_interval = list_qrs[j][5]
        QRS_width = list_qrs[j][6]
        TP_TP = list_qrs[j][7]
        PQ_PQ = list_qrs[j][8]
        list_baru_RR.append(RR_interval)
        list_baru_qrs.append(QRS_width)
        list_baru_TP.append(TP_TP)
        list_baru_PQ.append(PQ_PQ)

    total_qrs = []
    # RR Interval
    maxRR = max(list_baru_RR)
    minRR = min(list_baru_RR)
    meanRR = np.mean(list_baru_RR)
    stdevRR = np.std(list_baru_RR)

    # QRS Duration
    maxQRS = max(list_baru_qrs)
    minQRS = min(list_baru_qrs)
    meanQRS = np.mean(list_baru_qrs)
    stdevQRS = np.std(list_baru_qrs)

    # TP Duration
    maxTP = max(list_baru_TP)
    minTP = min(list_baru_TP)
    meanTP = np.mean(list_baru_TP)
    stdevTP = np.std(list_baru_TP)

    # PQ Duration
    maxPQ = max(list_baru_PQ)
    minPQ = min(list_baru_PQ)
    meanPQ = np.mean(list_baru_PQ)
    stdevPQ = np.std(list_baru_PQ)
    total_qrs.append(['maxRR','minRR','meanRR','stdevRR','maxQRS','minQRS','meanQRS','stdevQRS','maxTP','minTP','meanTP','stdevTP',
            'maxPQ','minPQ','meanPQ','stdevPQ'])
    total_qrs.append([maxRR,minRR,meanRR,stdevRR,maxQRS,minQRS,meanQRS,stdevQRS,maxTP,minTP,meanTP,stdevTP,maxPQ,minPQ,meanPQ,stdevPQ])
    return total_qrs


def ecg_plot (data_title, raw_signal, clean_ecg, list_qrs):
    plt.figure()
    plt.subplot(211)
    plt.title('Raw Signal ' + data_title)
    plt.plot(range(len(raw_signal)), raw_signal)

    plt.subplot(212)
    plt.title('Clean Signal ' + data_title)
    plt.plot(range(len(clean_ecg)), clean_ecg)
    for j in range(len(list_qrs)):
        plt.plot(list_qrs[j][0][0], list_qrs[j][0][1], 'm.', markersize=10)
        plt.plot(list_qrs[j][1][0], list_qrs[j][1][1], 'y.', markersize=10)
        plt.plot(list_qrs[j][2][0], list_qrs[j][2][1], 'r.', markersize=10)
        plt.plot(list_qrs[j][3][0], list_qrs[j][3][1], 'g.', markersize=10)
        plt.plot(list_qrs[j][4][0], list_qrs[j][4][1], 'b.', markersize=10)