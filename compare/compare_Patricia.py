import time
import os
import json
import sys
import matplotlib.pyplot as plt

# 添加 Patricia-Tries 到 sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取 compare_img.py 文件所在目录
parent_dir = os.path.join(current_dir, "../Patricia-Tries")  # Patricia-Tries 的相对路径
sys.path.append(parent_dir)  # 添加到 sys.path

from patricia import PatriciaTrie, hauteur,recherche, profondeurMoyenne,suppression  # 从 patricia.py 导入所需函数

# 更新路径
input_folder = "./Shakespeare"  # Shakespeare 文件夹路径
output_folder = "./result_Patricia"      # 输出结果的文件夹
test_file = "./test/word.txt"  # 新单词的测试文件路径
os.makedirs(output_folder, exist_ok=True)

print("Constructing Patricia Trie...")
overall_patricia = PatriciaTrie()
start_time_total = time.time()
  # 存储 single_patricia 的总构建时间
overall_patricia_total_time = 0  # 存储 overall_patricia 的总构建时间


file_results = {}  # 保存每个文件的结果

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):  # 只处理 .txt 文件
        print(f"Processing {filename}...")
        file_path = os.path.join(input_folder, filename)
        single_patricia = PatriciaTrie()  # 每个文件一个独立的 Patricia Trie
        single_patricia_total_time = 0
        # 重置计数器
        single_patricia.operation_count = {
            "insert_comparisons": 0,
            "search_comparisons": 0,
            "delete_comparisons": 0,
        }
        file_start_time = time.time()  # 开始时间
        word_count = 0
#插入构建
        with open(file_path, "r") as file:
            for line in file:
                word = line.strip().lower()  # 预处理单词
                if word:
                    # 记录 single_patricia 的插入时间
                    start_time = time.time()
                    single_patricia.inserer(word)  # 插入当前文件的 Patricia Trie
                    end_time = time.time()
                    single_patricia_total_time += (end_time - start_time)

                    # 记录 overall_patricia 的插入时间
                    start_time = time.time()
                    overall_patricia.inserer(word)  # 插入到总体 Patricia Trie
                    end_time = time.time()
                    overall_patricia_total_time += (end_time - start_time)

                    word_count += 1
        operation_count= single_patricia.operation_count

        # 搜索测试
        with open(file_path, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    recherche(single_patricia,word)

        # 插入新单词并记录时间
        # 读取测试单词
        with open(test_file, "r") as f:
            test_words = [line.strip().lower() for line in f if line.strip()]

        for word in test_words:
            start_time = time.time()
            single_patricia.inserer(word)
            end_time = time.time()
            insertion_times=end_time - start_time
        # 删除测试
        with open(test_file, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    suppression(single_patricia,word)  # 删除操作

        # 删除测试并记录时间
        delete_times = []  # 存储每次删除操作的时间
        with open(test_file, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    start_time = time.time()  # 开始时间
                    suppression(single_patricia, word)  # 删除操作
                    end_time = time.time()  # 结束时间
                    delete_times.append(end_time - start_time)  # 记录删除时间

        # 计算总删除时间
        total_delete_time = sum(delete_times)


        # 统计结果
        file_results[filename] = {
            "Word Count": word_count,
            "Single Construction Time (seconds)": single_patricia_total_time,
            "Overall Construction Time (seconds)": overall_patricia_total_time,
            "Height": hauteur(single_patricia),
            "Average Depth": profondeurMoyenne(single_patricia),
            "Insert Comparisons": operation_count["insert_comparisons"],
            "Search Comparisons": single_patricia.operation_count["search_comparisons"],
            "Delete Comparisons": single_patricia.operation_count["delete_comparisons"],
            "Insertion NEW LIST WORD Times (milliseconds)": insertion_times* 1000000,
            "Total Deletion Time (seconds)": total_delete_time,  # 添加删除时间
        }

# 保存每个文件的结果到 JSON 文件
with open(os.path.join(output_folder, "file_results_patricia.json"), "w") as file_result_file:
    json.dump(file_results, file_result_file, indent=4)
total_end_time = time.time()

overall_results = {
    "Total Word Count": sum([result["Word Count"] for result in file_results.values()]),
    "Total Construction Time (seconds)": sum([result["Single Construction Time (seconds)"] for result in file_results.values()]),
    "Overall Height": hauteur(overall_patricia),
    "Overall Average Depth": profondeurMoyenne(overall_patricia),
}

# 保存总体结果到 JSON 文件
with open(os.path.join(output_folder, "overall_results_patricia.json"), "w") as overall_result_file:
    json.dump(overall_results, overall_result_file, indent=4)

print("Patricia Trie results saved to result folder.")

