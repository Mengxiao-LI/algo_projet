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

        # 保存当前文件的结果
        file_results[filename] = {
            "Word Count": word_count,
            "Construction Time (seconds)": file_end_time - file_start_time,
            "Height": single_trie.hauteur(),
            "Average Depth": single_trie.profondeur_moyenne(),
            "Insert Comparisons": single_trie.operation_count["insert_comparisons"],
            "Search Comparisons": single_trie.operation_count["search_comparisons"],
        }

total_end_time = time.time()

# 统计总体结果
overall_results = {
    "Total Word Count": sum([result["Word Count"] for result in file_results.values()]),
    "Total Construction Time (seconds)": total_end_time - start_time_total,
    "Overall Height": overall_trie.hauteur(),
    "Overall Average Depth": overall_trie.profondeur_moyenne(),
}

# 保存到 JSON 文件
with open(os.path.join(output_folder, "file_results.json"), "w") as file_result_file:
    json.dump(file_results, file_result_file, indent=4)

with open(os.path.join(output_folder, "overall_results.json"), "w") as overall_result_file:
    json.dump(overall_results, overall_result_file, indent=4)

print("Hybrid Trie results saved to result folder.")

# 生成图表
def plot_results(file_results):
    # 准备数据
    files = list(file_results.keys())
    construction_times = [file_results[file]["Construction Time (seconds)"] for file in files]
    heights = [file_results[file]["Height"] for file in files]
    avg_depths = [file_results[file]["Average Depth"] for file in files]

    # 构建时间图
    plt.figure(figsize=(12, 6))
    plt.bar(files, construction_times, color="skyblue")
    plt.xlabel("Files")
    plt.ylabel("Construction Time (seconds)")
    plt.title("Hybrid Trie Construction Time Per File")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "construction_time.png"))
    plt.close()

    # 高度图
    plt.figure(figsize=(12, 6))
    plt.bar(files, heights, color="salmon")
    plt.xlabel("Files")
    plt.ylabel("Trie Height")
    plt.title("Hybrid Trie Height Per File")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "height.png"))
    plt.close()

    # 平均深度图
    plt.figure(figsize=(12, 6))
    plt.bar(files, avg_depths, color="lightgreen")
    plt.xlabel("Files")
    plt.ylabel("Average Depth")
    plt.title("Hybrid Trie Average Depth Per File")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "average_depth.png"))
    plt.close()

    print("Construction Time, Height, and Average Depth charts generated.")

def plot_comparison_results(file_results):
    files = list(file_results.keys())
    insert_comparisons = [file_results[file]["Insert Comparisons"] for file in files]
    search_comparisons = [file_results[file]["Search Comparisons"] for file in files]

    # 插入比较图
    plt.figure(figsize=(12, 6))
    plt.bar(files, insert_comparisons, color="orange")
    plt.xlabel("Files")
    plt.ylabel("Insert Comparisons")
    plt.title("Insert Comparisons Per File")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "insert_comparisons.png"))
    plt.close()

    # 搜索比较图
    plt.figure(figsize=(12, 6))
    plt.bar(files, search_comparisons, color="purple")
    plt.xlabel("Files")
    plt.ylabel("Search Comparisons")
    plt.title("Search Comparisons Per File")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "search_comparisons.png"))
    plt.close()

    print("Insert and Search Comparisons charts generated.")

# 调用绘图函数
plot_results(file_results)
plot_comparison_results(file_results)

print("Charts saved to result folder.")
