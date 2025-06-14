from friendship import *
from combat import *
from rng import main as generate_random_numbers
import pandas as pd
from combat import storage, combat
from init import load_user_data
import csv

fs_level_data = 'data/friendship_level_data.csv'
fs_data = 'data/friendship_data.csv'

def return_to_menu():
    if input("按任意键返回...") != None:
        #print("Returning to main menu...")
        return 1
    else:
        pass
    # Placeholder for returning to the main menu functionality
    
def view_stories():
    #print("Viewing stories is not implemented yet.")
    dict = check_stories_status(fs_data)
    try:
        if dict["allok"] == True:
            print("所有好感故事已阅读！")
            input("按任意键返回...")
        else:
            for key in dict.keys():
                if key != "allok":
                    print(f"{dict[key][0]}有好感故事未阅读, 输入{key}阅读")
                    
            story = input("输入其它值返回首页")         
            if story in dict:
                display_dialogue(dict[story][0], 5 * dict[story][1], fs_data)
    except ValueError:
        pass

def choices(choices_list):
    print("请选择:")
    for i, choice in enumerate(choices_list, 1):
        print(f"{i}. {choice}")
    
    while True:
        try:
            user_choice = input("请选择 (1-{}): ".format(len(choices_list)))
            #print(user_choice.split(" "))
            if user_choice.split(" ")[0] == "/cheat" and user_choice.split(" ")[1] == "add_fs_exp":
                update_friendship_exp(user_choice.split(" ")[2], int(user_choice.split(" ")[3]), fs_data)
                print("成功作弊！")
            elif 1 <= int(user_choice) <= len(choices_list):
                return int(user_choice)
            else:
                print("Invalid choice. Please try again.")
                
        except ValueError:
            #None
            print("Invalid input. Please enter a number.")

def show_user_data():
    back = 0
    while back != 1:
        user_data_dict = load_user_data()
        print("User Data:")
        for key, value in user_data_dict.items():
            print(f"{key}: {value}")
        back = return_to_menu()

def csv_to_dict(csv_file):
    user_dict = {}
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # 跳过标题行（如果有）
        
        for row in reader:
                name, exp, story_1, story_2, story_3, story_4, story_5, story_6= row[0], row[1], row[2], row[3], row[4], row[5], row[6]
                user_dict[name] = [exp, story_1, story_2, story_3, story_4, story_5, story_6]  # 或用元组 (exp, status)
    
    return user_dict

new_stories = " (New!)"

def main():    
    level_data, friendship_data = load_friendship_data(fs_level_data, fs_data)
    if not level_data.empty:
        print("成功加载好感数据")
    else:
        print("加载好感数据失败")
    
    user_data_dict = load_user_data()
    if check_stories_status(fs_data)["allok"] == True:
        new_stories = ""
        
    print("##### 欢迎来到张思朗恋爱养成小游戏 #####")
    print("#####       制作者：Jigi       #####")
    
    while True:
        #print(check_stories_status(fs_data)["allok"])
        if check_stories_status(fs_data)["allok"] == True:
            new_stories = ""
        else:
            new_stories = " (New!)"
                    
        choices_list = [
            "用户数据",
            "背包",
            "战斗",
            "好感故事%s" % new_stories,
            "退出"
        ]
        
        do_dict = {
            1: show_user_data,
            2: storage,
            3: combat,
            4: view_stories,
            5: exit
        }   
        choice = choices(choices_list)
        if choice == 5:
            print("正在退出游戏...")
            break
        do_dict[choice]() # Call the function based on user choice
        
#print(get_fs_level(2000))
main()