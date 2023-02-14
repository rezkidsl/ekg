import requests
data_ecg = f'Dataset/Data TEST/ALL_DATA/AF_218.csv'
f = open(data_ecg, 'r')
lines = f.readlines()
f.close()



payload = {
    'Lines_ECG': lines,
    'Status' : 1
}
data = requests.post('https://ekg-production.up.railway.app/predict_ecg', json=payload)
print(data.json())
