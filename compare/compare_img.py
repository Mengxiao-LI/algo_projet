import json
import os
import matplotlib.pyplot as plt

# 定义 JSON 文件路径
hybrid_result_folder = "./result"
patricia_result_folder = "./result_Patricia"

# 读取 Hybrid Trie 和 Patricia Trie 的结果
def load_results(folder, file_name):
    file_path = os.path.join(folder, file_name)
    with open(file_path, "r") as file:
        return json.load(file)

# 加载 JSON 数据
hybrid_file_results = load_results(hybrid_result_folder, "file_results.json")
hybrid_overall_results = load_results(hybrid_result_folder, "overall_results.json")
patricia_file_results = load_results(patricia_result_folder, "file_results_patricia.json")
patricia_overall_results = load_results(patricia_result_folder, "overall_results_patricia.json")

# 提取每个文件的对比数据
files = list(hybrid_file_results.keys())
# hybrid_construction_times = [hybrid_file_results[file]["Construction Time (seconds)"] for file in files]
# patricia_construction_times = [patricia_file_results[file]["Construction Time (seconds)"] for file in files]

hybrid_single_construction_times = [hybrid_file_results[file]["Single Construction Time (seconds)"] for file in files]
patricia_single_construction_times = [patricia_file_results[file]["Single Construction Time (seconds)"] for file in files]

hybrid_all_construction_times = [hybrid_file_results[file]["Overall Construction Time (seconds)"] for file in files]
patricia_all_construction_times = [patricia_file_results[file]["Overall Construction Time (seconds)"] for file in files]

hybrid_heights = [hybrid_file_results[file]["Height"] for file in files]
patricia_heights = [patricia_file_results[file]["Height"] for file in files]

hybrid_avg_depths = [hybrid_file_results[file]["Average Depth"] for file in files]
patricia_avg_depths = [patricia_file_results[file]["Average Depth"] for file in files]

hybrid_insert_comparisons = [hybrid_file_results[file]["Insert Comparisons"] for file in files]
patricia_insert_comparisons = [patricia_file_results[file]["Insert Comparisons"] for file in files]

hybrid_search_comparisons = [hybrid_file_results[file]["Search Comparisons"] for file in files]
patricia_search_comparisons = [patricia_file_results[file]["Search Comparisons"] for file in files]

# 提取删除时间数据
hybrid_delete_times = [hybrid_file_results[file]["Total Deletion Time (seconds)"] for file in files]
patricia_delete_times = [patricia_file_results[file]["Total Deletion Time (seconds)"] for file in files]


# 定义绘图函数
def plot_comparison(metric, hybrid_values, patricia_values, y_label, title, file_name):
    plt.figure(figsize=(12, 6))
    bar_width = 0.35
    x_indexes = range(len(files))

    # 绘制柱状图
    plt.bar([x - bar_width/2 for x in x_indexes], hybrid_values, width=bar_width, label="Hybrid Trie", color="skyblue")
    plt.bar([x + bar_width/2 for x in x_indexes], patricia_values, width=bar_width, label="Patricia Trie", color="salmon")

    # 添加图例、标题和轴标签
    plt.xlabel("Files")
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(ticks=x_indexes, labels=files, rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    # 保存图表
    plt.savefig(os.path.join("./result_img", file_name))
    plt.close()

# 创建输出文件夹
os.makedirs("./result_img", exist_ok=True)

# 绘制对比图
plot_comparison("Construction Time", hybrid_single_construction_times, patricia_single_construction_times,
                "Construction Time (seconds)", "Comparison of Construction Time per File", "Construction Time per File.png")
# 绘制对比图
plot_comparison("Construction Time", hybrid_all_construction_times, patricia_all_construction_times,
                "Construction Time (seconds)", "Comparison of Cumulative Construction Time", "Cumulative Construction Time.png")

plot_comparison("Height", hybrid_heights, patricia_heights,
                "Trie Height", "Comparison of Trie Heights", "height_comparison.png")

plot_comparison("Average Depth", hybrid_avg_depths, patricia_avg_depths,
                "Average Depth", "Comparison of Average Depths", "average_depth_comparison.png")

plot_comparison("Insert Comparisons", hybrid_insert_comparisons, patricia_insert_comparisons,
                "Insert Comparisons", "Comparison of Insert Comparisons", "insert_comparisons_comparison.png")

plot_comparison("Search Comparisons", hybrid_search_comparisons, patricia_search_comparisons,
                "Search Comparisons", "Comparison of Search Comparisons", "search_comparisons_comparison.png")

# 绘制删除时间的比较图
plot_comparison(
    "Deletion Time",
    hybrid_delete_times,
    patricia_delete_times,
    "Deletion Time (seconds)",
    "Comparison of Deletion Time",
    "deletion_time_comparison.png"
)


# 删除比较图
plot_comparison(
    "Delete Comparisons",
    [hybrid_file_results[file]["Delete Comparisons"] for file in files],
    [patricia_file_results[file]["Delete Comparisons"] for file in files],
    "Delete Comparisons",
    "Comparison of Delete Comparisons",
    "delete_comparisons_comparison.png",
)
plot_comparison(
    "Insertion NEW LIST WORD Times",
    [hybrid_file_results[file]["Insertion NEW LIST WORD Times (milliseconds)"]for file in files],
    [patricia_file_results[file]["Insertion NEW LIST WORD Times (milliseconds)"] for file in files],
    "Insertion Times (milliseconds)",
    "Comparison of Insertion NEW LIST WORD Times",
    "insertion_new_list_word_times_comparison.png",
)

print("Comparison charts saved to './result_img' folder.")
