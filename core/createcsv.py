import csv

headers = ['id', 'speaker', 'content']

# 创建并写入文件（文件不存在时会自动创建）
def create_csv_file(name):
    for i in range(1, 7):
        filename = f"{name}_{i * 5}.csv"
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

create_csv_file("chy")