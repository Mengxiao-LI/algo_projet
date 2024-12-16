import os
import sys
import json
from hybrid_trie import HybridTrie

# 检查参数数量
if len(sys.argv) < 3:
    print("Usage: python trie_prefixe.py <file.json> <prefix>")
    sys.exit(1)

# 定义输入和输出路径

input_file = sys.argv[1] # 从输入文件夹读取文件
prefix = sys.argv[2]
output_folder = "Hybrid_trie/result"  # 输出文件夹
output_file = os.path.join(output_folder, "prefixe.txt")  # 保存结果到 result 文件夹

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 加载树
try:
    with open(input_file, "r") as f:
        trie = HybridTrie.from_dict(json.load(f))
except FileNotFoundError:
    print(f"Error: {input_file} not found.")
    sys.exit(1)

# 计算前缀单词数量
prefix_count = trie.prefixe(prefix)

# 保存结果到文件
try:
    with open(output_file, "w") as f:
        f.write(f"{prefix_count}\n")
    print(f"Prefix count for '{prefix}' from {input_file} saved to {output_file}")
except IOError as e:
    print(f"Error writing to {output_file}: {e}")
    sys.exit(1)
