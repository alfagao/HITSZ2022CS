import pandas as pd
raw_info_path = "./dataWashed/patientSZ.csv"
washed_data_path = "./dataWashed/patientNoRepeat.csv"

def no_repeat():
    patientSZ = pd.read_csv(raw_info_path)
    patientNoRepeat = []
    for index, row in patientSZ.iterrows():
        data = {
            "confirmDate": row["confirmDate"],
            "patientGender": row["patientGender"],
            "patientAge": row["patientAge"],
            "homeLng": row["homeLng"],
            "homeLat": row["homeLat"]
        }
        if data not in patientNoRepeat:
            patientNoRepeat.append(data)
        else:
            print(data)
    pd.DataFrame(patientNoRepeat).to_csv(washed_data_path, index=False)
if __name__ == '__main__':
    no_repeat()
