import pandas as pd
from tqdm import tqdm
import csv

user_data_csv = 'data/user_data.csv'

"""def load_user_data():
    with open("user_data.csv", "r") as file:
        file_data = file.readlines()
        data = []
        for line in file_data:
            line_text = line.split(" = ")
            line_text[1] = str(line_text[1].splitlines()[0])
            data.append(line_text)
    user_data_dict = {line[0]: line[1] for line in data}
    return user_data_dict"""

def load_user_data():
    with open(user_data_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # 读取列名
        row_data = next(reader)  # 读取数据行（仅第一行）
        
        # 将列名和对应值组合成字典
        return dict(zip(headers, row_data))

#print(load_user_data())