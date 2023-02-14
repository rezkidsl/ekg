import AFSignalProcessing as SP
import numpy as np

def Run_program(list_data, status):
    #DATA
    data_path_AF = 'Dataset/Data AF/'
    data_ecg_AF = list_data
    data_path_N = 'Dataset/Data NORMAL/'
    data_ecg_N = list_data
    real_time = 0

    # Signal Processing anda Feature Calculation
    featureAF = SP.AF_SP(data_path_AF, data_ecg_AF, signal_type = status)
    # np.savetxt("AFIB.csv", featureAF, delimiter=", ", fmt='% s')
    featureN = SP.AF_SP(data_path_N, data_ecg_N, signal_type = status)
    # np.savetxt("NORMAL.csv", featureN, delimiter=", ", fmt='% s')
    # print({'featureAF':featureAF, 'featureN':featureN})
    # print('='*100)
    return featureAF, featureN 

def test_program(list_data, status):
    #DATA
    data_path_AF = 'Dataset/Data TEST/ALL_DATA/'
    data_ecg_AF = list_data
    # Signal Processing anda Feature Calculation
    featureAF = SP.AF_SP(data_path_AF, data_ecg_AF, signal_type = status)
    # np.savetxt("AFIB.csv", featureAF, delimiter=", ", fmt='% s')
    # np.savetxt("NORMAL.csv", featureN, delimiter=", ", fmt='% s')
    # print({'featureAF':featureAF, 'featureN':featureN})
    # print('='*100)
    return featureAF 


# MAIN

# from os import listdir
# from os.path import isfile, join
# mypath = 'Dataset/Data AF'
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# onlyfiles = list(map(lambda x:x.split('.')[0], onlyfiles))
# print(onlyfiles)


# for i in range(len(onlyfiles)):
#     data_name = str(i+1)
#     Run_program([onlyfiles[i]])