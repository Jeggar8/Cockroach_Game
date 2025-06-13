import pandas as pd
from tqdm import tqdm
import csv

fs_level_data = 'data/friendship_level_data.csv'
fs_data = 'data/friendship_data.csv'

def calculate_friendship_exp(level):
    return 1000 * (1.04 ** level - 1)
        
def create_friendship_data(file_path):
    data = {
        'level': [],
        'exp': []
    }
    
    for i in tqdm(range(1, 100)):
        data['level'].append(i)
        data['exp'].append(round(calculate_friendship_exp(i))) 

    df = pd.DataFrame(data)

    df.to_csv(file_path, index=False)
    print(f"Friendship data created and saved to {file_path}")

def load_friendship_data(level_data_path, data_path):
    try:
        level_data = pd.read_csv(level_data_path)
        data = pd.read_csv(data_path)
        return level_data, data
    
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def get_fs_level(exp):
    df, _ = load_friendship_data(fs_level_data, fs_data)
    level = df.loc[df['exp'] <= exp, 'level'].max()
    
    if pd.isna(level):
        return None
    
    return int(level)

def display_dialogue(name, heart_level, friendship_data_csv):
    """
    从CSV文件读取并显示对话，按回车键显示下一句
    :param csv_file: CSV文件路径
    """
    csv_file = f"data/stories/{name}/{name}_{heart_level}.csv"
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # 跳过标题行（如果有）
            next(reader, None)
            
            print("对话开始（按回车键继续）...\n")
            
            for row in reader:
                if len(row) >= 3:  # 确保行有足够的数据
                    dialogue_id, speaker, content = row[0], row[1], row[2]
                    input(f"{speaker}：{content}")
                
            print("\n对话结束！")
            # 更新好感度数据
            friendship_data = pd.read_csv(friendship_data_csv)
            friendship_data.loc[friendship_data['name'] == name, f"{heart_level}_heart_story"] = 2
            friendship_data.to_csv(friendship_data_csv, index=False)
    
    except FileNotFoundError:
        print(f"错误：文件 {csv_file} 未找到")
    except Exception as e:
        print(f"发生错误：{e}")

def update_friendship_exp(name, exp, friendship_data_csv):
    
    friendship_data = pd.read_csv(friendship_data_csv)
    friendship_data.loc[friendship_data['name'] == name, "friendship_exp"] += exp
    #print(friendship_data.loc[friendship_data['name'] == name, "friendship_exp"][0])
    #print(friendship_data.loc[friendship_data['name'] == "ymh", f"{5}_heart_story"])
    level = get_fs_level(friendship_data.loc[friendship_data['name'] == name, "friendship_exp"][0])
    for i in range(1, 7):
        if friendship_data.loc[friendship_data['name'] == name, f"{5*i}_heart_story"][0] != 2 and level >= 5 * i:
            #print(f"{5*i}_heart_story")
            friendship_data.loc[friendship_data['name'] == name, f"{5*i}_heart_story"] = 1
        
    friendship_data.to_csv(friendship_data_csv, index=False)
    
def check_stories_status(fs_data):
    """
    检查角色好感故事阅读情况
    :param csv_file: CSV文件路径
    """
    with open(fs_data, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # 跳过标题行
        
        all_ok = True  # 标记是否所有人都已完成所有故事
        num = 0
        dict = {"allok": True}  # 用于存储未读故事的字典
        
        for row in reader:                
            name = row[0]
            stories = row[2:8]  # 第3到第8列是故事状态
            unread_stories = []
            unread_stories_str = []
            
            for i, status in enumerate(stories, start=1):
                if status == '1':  # 1表示未阅读
                    unread_stories.append(i)
                    unread_stories_str.append(str(i))
            
            #print(unread_stories)
            
            if unread_stories:
                all_ok = False
                dict["allok"] = False
                num += 1
                stories_str = "、".join(unread_stories_str)  # 用顿号分隔故事编号
                #print(f"{name}有{stories_str}号好感故事未阅读, 输入{num}阅读")
                dict[str(num)] = [name, min(unread_stories)]
        
        return dict

#_, df = load_friendship_data(fs_level_data, fs_data)
#print(get_fs_level(df.loc[df['name'] == "ymh", "friendship_exp"][0]))
#update_friendship_exp("ymh", 1000, fs_data)
