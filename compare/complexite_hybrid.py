import time
import os
import json
import matplotlib.pyplot as plt
import sys
import signal

sys.path.append("../Hybrid_trie")  # 替换为 hybrid_trie 文件所在的实际路径
from hybrid_trie import HybridTrie


# 定义超时异常
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Timed out!")

signal.signal(signal.SIGALRM, timeout_handler)

def safe_execution(func, *args, timeout=10):
    """安全执行函数，防止超时"""
    try:
        signal.alarm(timeout)
        result = func(*args)
        signal.alarm(0)
        return result
    except TimeoutException:
        return float('inf')

def load_words_from_file(file_path, limit):
    """从文件中读取指定数量的单词"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().split()
        return content[:limit]

def test_methods(words):
    """测试 Hybrid Trie 的所有方法"""
    hybrid_trie = HybridTrie()
    results = {
        "Recherche": 0,
        "ComptageMots": 0,
        "ListeMots": 0,
        "ComptageNil": 0,
        "Hauteur": 0,
        "ProfondeurMoyenne": 0,
        "Prefixe": 0,
        "Suppression": 0,
    }

    # 插入单词到 Hybrid Trie
    for word in words:
        hybrid_trie.insert(word)

    # 搜索
    start_time = time.time()
    for word in words:
        safe_execution(hybrid_trie.recherche, word, timeout=5)
    results["Recherche"] = time.time() - start_time

    # 统计单词数量
    start_time = time.time()
    safe_execution(hybrid_trie.comptageMots, hybrid_trie.root, timeout=5)
    results["ComptageMots"] = time.time() - start_time

    # 列出所有单词
    start_time = time.time()
    safe_execution(hybrid_trie.liste_mots, timeout=5)
    results["ListeMots"] = time.time() - start_time

    # 统计空指针
    start_time = time.time()
    safe_execution(hybrid_trie.comptage_nil, timeout=5)
    results["ComptageNil"] = time.time() - start_time

    # 树高度
    start_time = time.time()
    safe_execution(hybrid_trie.hauteur, timeout=5)
    results["Hauteur"] = time.time() - start_time

    # 平均深度
    start_time = time.time()
    safe_execution(hybrid_trie.profondeur_moyenne, timeout=5)
    results["ProfondeurMoyenne"] = time.time() - start_time

    # 前缀搜索
    start_time = time.time()
    safe_execution(hybrid_trie.prefixe, "a", timeout=5)
    results["Prefixe"] = time.time() - start_time

    # 删除所有单词
    start_time = time.time()
    for word in words:
        safe_execution(hybrid_trie.suppression, word, timeout=5)
    results["Suppression"] = time.time() - start_time

    return results

# 初始化变量
input_sizes = [100, 500, 1000, 5000, 10000]
shakespeare_folder = "./Shakespeare"
all_results = {method: [0] * len(input_sizes) for method in ["Recherche", "ComptageMots", "ListeMots", "ComptageNil", "Hauteur", "ProfondeurMoyenne", "Prefixe", "Suppression"]}
file_count = 0

# 遍历文件并测试
for filename in os.listdir(shakespeare_folder):
    file_path = os.path.join(shakespeare_folder, filename)
    if os.path.isfile(file_path):
        print(f"Processing file: {filename}")
        file_count += 1

        for idx, input_size in enumerate(input_sizes):
            words = load_words_from_file(file_path, input_size)
            if not words:
                continue
            results = test_methods(words)

            # 累加结果
            for method in all_results.keys():
                all_results[method][idx] += results[method]

# 取平均值
for method in all_results.keys():
    all_results[method] = [time / file_count for time in all_results[method]]

# 结果保存路径
result_img_folder = "./result_img/complexity"
os.makedirs(result_img_folder, exist_ok=True)

# 绘制图表：Recherche 和 Suppression
plt.figure(figsize=(10, 6))
for method in ["Recherche", "Suppression"]:
    plt.plot(input_sizes, all_results[method], label=method, linewidth=2)
plt.title("Average Execution Time (Hybrid Trie): Recherche and Suppression")
plt.xlabel("Input Size (Number of Words)")
plt.ylabel("Average Execution Time (seconds)")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(os.path.join(result_img_folder, "complexity_Hybrid_recherche_suppression.png"))
plt.show()

# 绘制图表：其他方法
plt.figure(figsize=(10, 6))
for method in ["ComptageMots", "ListeMots", "ComptageNil", "Hauteur", "ProfondeurMoyenne", "Prefixe"]:
    plt.plot(input_sizes, all_results[method], label=method, linewidth=2)
plt.title("Average Execution Time (Hybrid Trie): Other Methods")
plt.xlabel("Input Size (Number of Words)")
plt.ylabel("Average Execution Time (seconds)")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(os.path.join(result_img_folder, "complexity_Hybrid_other_methods.png"))
plt.show()

print("Hybrid Trie Average Execution analysis completed and plots saved.")
