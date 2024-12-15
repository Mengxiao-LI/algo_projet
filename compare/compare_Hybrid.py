import time
import os
import json
import sys
import matplotlib.pyplot as plt

# 添加 HybridTrie 模块路径
sys.path.append("../Hybrid_trie")
from hybrid_trie import HybridTrie

# 更新路径
input_folder = "./Shakespeare"  # Shakespeare 文件夹路径
output_folder = "./result"      # 输出结果的文件夹
test_file = "./test/word.txt"  # 新单词的测试文件路径
os.makedirs(output_folder, exist_ok=True)

# 初始化计时器和结果
file_results = {}

# Hybrid Trie 测试
print("Constructing Hybrid Trie...")
overall_trie = HybridTrie()
start_time_total = time.time()

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        print(f"Processing {filename}...")
        file_path = os.path.join(input_folder, filename)
        single_trie = HybridTrie()

        # 重置计数器
        single_trie.operation_count = {
            "insert_comparisons": 0,
            "search_comparisons": 0,
            "delete_comparisons": 0,
        }

        file_start_time = time.time()
        word_count = 0

        # 插入单词
        with open(file_path, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    single_trie.insert(word)
                    overall_trie.insert(word)  # 插入总树
                    word_count += 1

        file_end_time = time.time()

        # 搜索测试
        with open(file_path, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    single_trie.recherche(word)

        # 插入新单词并记录时间
        # 读取测试单词
        with open(test_file, "r") as f:
            test_words = [line.strip().lower() for line in f if line.strip()]
        for word in test_words:
            start_time = time.time()
            single_trie.insert(word)
            end_time = time.time()
            insertion_times= end_time - start_time
        # 删除测试
        with open(test_file, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    single_trie.suppression(word)  # 删除操作

        # 保存当前文件的结果
        file_results[filename] = {
            "Word Count": word_count,
            "Construction Time (seconds)": file_end_time - file_start_time,
            "Height": single_trie.hauteur(),
            "Average Depth": single_trie.profondeur_moyenne(),
            "Insert Comparisons": single_trie.operation_count["insert_comparisons"],
            "Search Comparisons": single_trie.operation_count["search_comparisons"],
            "Delete Comparisons": single_trie.operation_count["delete_comparisons"],
            "Insertion NEW LIST WORD Times (milliseconds)": insertion_times* 1000000,
        }

total_end_time = time.time()

# 统计总体结果
overall_results = {
    "Total Word Count": sum([result["Word Count"] for result in file_results.values()]),
    "Total Construction Time (seconds)": sum([result["Construction Time (seconds)"] for result in file_results.values()]),
    "Overall Height": overall_trie.hauteur(),
    "Overall Average Depth": overall_trie.profondeur_moyenne(),
}

# 保存到 JSON 文件
with open(os.path.join(output_folder, "file_results.json"), "w") as file_result_file:
    json.dump(file_results, file_result_file, indent=4)

with open(os.path.join(output_folder, "overall_results.json"), "w") as overall_result_file:
    json.dump(overall_results, overall_result_file, indent=4)

print("Hybrid Trie results saved to result folder.")
