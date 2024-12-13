import time
import os
import json
import sys
import matplotlib.pyplot as plt

"""JSON 文件：

individual_results.json：记录每个文件独立构建树的时间、高度和平均深度。
merge_results.json：记录合并树的时间、最终树的高度和平均深度。
生成的图表：

construction_and_merge_time.png：独立构建树时间和合并时间的对比图。
height_per_file.png：每个文件对应的独立树的高度。
average_depth_per_file.png：每个文件对应的独立树的平均深度。
"""

# 添加 HybridTrie 模块路径
sys.path.append("../Hybrid_trie")
from hybrid_trie import HybridTrie

# 更新路径
input_folder = "./Shakespeare"  # Shakespeare 文件夹路径
output_folder = "./result"      # 输出结果的文件夹
os.makedirs(output_folder, exist_ok=True)

# 初始化计时器和结果
file_results = {}

# 独立构建多个树并记录时间
print("Constructing individual tries...")
individual_tries = []  # 用于存储独立树的列表
construction_times = []  # 用于存储每棵树的构建时间

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        print(f"Processing {filename}...")
        file_path = os.path.join(input_folder, filename)
        single_trie = HybridTrie()

        start_time = time.time()
        with open(file_path, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    single_trie.insert(word)
        end_time = time.time()

        # 将独立树及其构建时间保存
        individual_tries.append(single_trie)
        construction_times.append(end_time - start_time)

        # 保存每个文件的结果
        file_results[filename] = {
            "Construction Time (seconds)": end_time - start_time,
            "Height": single_trie.hauteur(),
            "Average Depth": single_trie.profondeur_moyenne(),
        }

# 合并这些独立的树
print("Merging individual tries into a complete trie...")
merged_trie = HybridTrie()
merge_start_time = time.time()

for trie in individual_tries:
    for word in trie.liste_mots():  # 提取每棵独立树中的所有单词
        merged_trie.insert(word)

merge_end_time = time.time()
merge_time = merge_end_time - merge_start_time

# 总体结果
overall_results = {
    "Total Construction Time (seconds)": sum(construction_times),
    "Merge Time (seconds)": merge_time,
    "Total Time (seconds)": sum(construction_times) + merge_time,
    "Final Trie Height": merged_trie.hauteur(),
    "Final Trie Average Depth": merged_trie.profondeur_moyenne(),
}

# 保存到 JSON 文件
with open(os.path.join(output_folder, "individual_results.json"), "w") as file_result_file:
    json.dump(file_results, file_result_file, indent=4)

with open(os.path.join(output_folder, "merge_results.json"), "w") as overall_result_file:
    json.dump(overall_results, overall_result_file, indent=4)

print("Results saved to result folder.")

# 生成图表
def plot_results(file_results, construction_times, merge_time):
    # 准备数据
    files = list(file_results.keys())
    heights = [file_results[file]["Height"] for file in files]
    avg_depths = [file_results[file]["Average Depth"] for file in files]

    # 构建时间图
    plt.figure(figsize=(12, 6))
    plt.bar(files, construction_times, color="skyblue", label="Individual Construction Time")
    plt.axhline(y=merge_time, color="red", linestyle="--", label="Merge Time")
    plt.xlabel("Files")
    plt.ylabel("Time (seconds)")
    plt.title("Individual Construction Time and Merge Time")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "construction_and_merge_time.png"))
    plt.close()

    # 高度图
    plt.figure(figsize=(12, 6))
    plt.bar(files, heights, color="salmon")
    plt.xlabel("Files")
    plt.ylabel("Trie Height")
    plt.title("Trie Height Per File")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "height_per_file.png"))
    plt.close()

    # 平均深度图
    plt.figure(figsize=(12, 6))
    plt.bar(files, avg_depths, color="lightgreen")
    plt.xlabel("Files")
    plt.ylabel("Average Depth")
    plt.title("Average Depth Per File")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "average_depth_per_file.png"))
    plt.close()

    print("Charts generated.")

# 绘制图表
plot_results(file_results, construction_times, merge_time)

print("Experiment complete.")
