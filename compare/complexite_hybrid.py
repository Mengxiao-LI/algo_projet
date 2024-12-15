import time
import os
import json
import matplotlib.pyplot as plt
import sys
import signal

sys.path.append("../Hybrid_trie")  # 替换为 hybrid_trie 文件所在的实际路径
from hybrid_trie import HybridTrie


class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Timed out!")

signal.signal(signal.SIGALRM, timeout_handler)

def safe_execution(func, *args, timeout=10):
    try:
        signal.alarm(timeout)
        result = func(*args)
        signal.alarm(0)
        return result
    except TimeoutException:
        return float('inf')


def test_methods(input_size):
    hybrid_trie = HybridTrie()
    words = [f"word{i}" for i in range(input_size)]

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

    for word in words:
        hybrid_trie.insert(word)

    # Recherche (搜索)
    start_time = time.time()
    for word in words:
        safe_execution(hybrid_trie.recherche, word, timeout=5)
    results["Recherche"] = time.time() - start_time

    # ComptageMots (统计单词数量)
    start_time = time.time()
    safe_execution(hybrid_trie.comptageMots, hybrid_trie.root, timeout=5)
    results["ComptageMots"] = time.time() - start_time

    # ListeMots (列出所有单词)
    start_time = time.time()
    safe_execution(hybrid_trie.liste_mots, timeout=5)
    results["ListeMots"] = time.time() - start_time

    # ComptageNil (统计空指针)
    start_time = time.time()
    safe_execution(hybrid_trie.comptage_nil, timeout=5)
    results["ComptageNil"] = time.time() - start_time

    # Hauteur (计算高度)
    start_time = time.time()
    safe_execution(hybrid_trie.hauteur, timeout=5)
    results["Hauteur"] = time.time() - start_time

    # ProfondeurMoyenne (计算平均深度)
    start_time = time.time()
    safe_execution(hybrid_trie.profondeur_moyenne, timeout=5)
    results["ProfondeurMoyenne"] = time.time() - start_time

    # Prefixe (以指定前缀开头的单词数量)
    start_time = time.time()
    safe_execution(hybrid_trie.prefixe, "word", timeout=5)
    results["Prefixe"] = time.time() - start_time

    # Suppression (删除所有单词)
    start_time = time.time()
    for word in words:
        safe_execution(hybrid_trie.suppression, word, timeout=5)
    results["Suppression"] = time.time() - start_time

    return results


input_sizes = [100, 500, 1000, 5000, 10000]
all_results = {method: [] for method in ["Recherche", "ComptageMots", "ListeMots", "ComptageNil", "Hauteur", "ProfondeurMoyenne", "Prefixe", "Suppression"]}

for input_size in input_sizes:
    print(f"Testing with input size: {input_size}")
    results = test_methods(input_size)
    for method, time_taken in results.items():
        all_results[method].append(time_taken)
# 创建结果保存路径
result_img_folder = "./result_img"
os.makedirs(result_img_folder, exist_ok=True)

# 折线图 1: Recherche 和 Suppression
plt.figure(figsize=(10, 6))
for method in ["Recherche", "Suppression"]:
    plt.plot(input_sizes, all_results[method], label=method, linewidth=2)

plt.title("Complexity Analysis: Recherche and Suppression", fontsize=14)
plt.xlabel("Input Size (Number of Words)", fontsize=12)
plt.ylabel("Execution Time (seconds)", fontsize=12)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(os.path.join(result_img_folder, "complexity_Hybrid_recherche_suppression_Patricia.png"))

plt.show()

# 折线图 2: 其他方法
plt.figure(figsize=(10, 6))
for method in ["ComptageMots", "ListeMots", "ComptageNil", "Hauteur", "ProfondeurMoyenne", "Prefixe"]:
    plt.plot(input_sizes, all_results[method], label=method, linewidth=2)

plt.title("Complexity Analysis: Other Methods", fontsize=14)
plt.xlabel("Input Size (Number of Words)", fontsize=12)
plt.ylabel("Execution Time (seconds)", fontsize=12)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(os.path.join(result_img_folder, "complexity_Hybrid_other_methods.png"))
plt.show()

print("Complexity analysis completed and plots saved.")
