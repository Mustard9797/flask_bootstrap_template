import csv
import random
from .CH_DBModel import TestTable

dict_csvColumn_CH2EN = {
    '年度': 'year',
    '縣市別': 'city',
    '包制戶數': 'HouseholdsOfTypeA',
    '包制售電量': 'ElecSalesOfTypeA',
    '表制戶數': 'HouseholdsOfTypeB',
    '表制售電量': 'ElecSalesOfTypeB',
    'LED戶數': 'HouseholdsOfLED',
    'LED售電量': 'ElecSalesOfLED',
}

dict_csvColumn_EN2CH = {
    'year': '年度',
    'city': '縣市別',
    'HouseholdsOfTypeA':'包制戶數',
    'ElecSalesOfTypeA': '包制售電量',
    'HouseholdsOfTypeB': '表制戶數',
    'ElecSalesOfTypeB': '表制售電量',
    'HouseholdsOfLED': 'LED戶數',
    'ElecSalesOfLED': 'LED售電量',
}

def read_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data

def write_random_data(filePPath, db, lastIdx):
    data = read_csv(filePPath)
    random_index = random.randint(1, len(data) - 1) # 需要扣掉欄位標題的那一個 row
    random_row = data[random_index]
    test_data = TestTable(
        idx = int(lastIdx+1),
        year=int(random_row[dict_csvColumn_EN2CH['year']]),
        city=random_row[dict_csvColumn_EN2CH['city']],
        HouseholdsOfTypeA=int(random_row[dict_csvColumn_EN2CH['HouseholdsOfTypeA']].replace(",", "")),
        ElecSalesOfTypeA=int(random_row[dict_csvColumn_EN2CH['ElecSalesOfTypeA']].replace(",", "")),
        HouseholdsOfTypeB=int(random_row[dict_csvColumn_EN2CH['HouseholdsOfTypeB']].replace(",", "")),
        ElecSalesOfTypeB=int(random_row[dict_csvColumn_EN2CH['ElecSalesOfTypeB']].replace(",", "")),
        HouseholdsOfLED=int(random_row[dict_csvColumn_EN2CH['HouseholdsOfLED']].replace(",", "")),
        ElecSalesOfLED=int(random_row[dict_csvColumn_EN2CH['ElecSalesOfLED']].replace(",", ""))
    )
    db.session.add(test_data)
    db.session.commit()