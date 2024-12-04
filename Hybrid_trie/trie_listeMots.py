import os
import sys
import json
from hybrid_trie import HybridTrie

if len(sys.argv) < 1:
    print("Usage: python trie_listeMots.py <file.json>")
    sys.exit(1)

# 获取输入文件名
input_file = sys.argv[1]

# 设置输入文件夹和文件路径
input_folder = "result"  # 输入文件夹
input_path = os.path.join(input_folder, input_file)

# 设置输出文件夹和文件路径
output_folder = "result"  # 输出文件夹
output_file = os.path.join(output_folder, "mot.txt")

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 加载树
try:
    with open(input_path, "r") as f:
        trie = HybridTrie.from_dict(json.load(f))
except FileNotFoundError:
    print(f"Error: {input_path} not found.")
    sys.exit(1)

# 列出所有单词
words = trie.liste_mots()

# 保存到文件
with open(output_file, "w") as f:
    for word in words:
        f.write(word + "\n")

print(f"Words listed from {input_path} and saved to {output_file}")
