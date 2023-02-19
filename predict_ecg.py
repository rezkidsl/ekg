import pandas as pd 
import pickle
import AFSignalProcessing
import pickle
import json

loaded_model = pickle.load(open('model_ecg_xgboost_tuned.sav', 'rb'))

def predict(lines, status):
    extraction_all = AFSignalProcessing.make_fiture(lines,status)
    fitur_n_json = []
    for x in [extraction_all]:    
        dictnya = {}
        for i,j in zip(x[0], x[1]):
            dictnya[i] = j 
        fitur_n_json.append(dictnya)
        

    df_test = pd.DataFrame(fitur_n_json)
    prediksi = loaded_model.predict(df_test.values)
    prediksi = loaded_model.predict_proba(df_test.values)
    if prediksi.argmax() == 1:
        return {'predict': 'AF', 'confidence': round(prediksi[0][prediksi.argmax()],2)}
    else:
        return {'predict': 'Normal', 'confidence': round(prediksi[0][prediksi.argmax()],2)}