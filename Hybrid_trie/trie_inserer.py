import os
import sys
import json
from hybrid_trie import HybridTrie

# 检查参数数量
if len(sys.argv) < 3:
    print("Usage: python trie_inserer.py <x> <file.txt>")
    sys.exit(1)

# 解析参数
x = int(sys.argv[1])
file_name = sys.argv[2]

# 确定输出文件夹和文件名
output_folder = "result"  # 定义结果保存的文件夹
if x == 0:
    output_file = os.path.join(output_folder, "pat.json")
elif x == 1:
    output_file = os.path.join(output_folder, "trie.json")
else:
    print("Error: Invalid value for x. Must be 0 or 1.")
    sys.exit(1)

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 加载现有的树或创建新的树
try:
    with open(output_file, "r") as f:
        data = json.load(f)
        trie = HybridTrie.from_dict(data)
except FileNotFoundError:
    print(f"File {output_file} not found. Creating a new Trie.")
    trie = HybridTrie()

# 插入单词
try:
    with open(file_name, "r") as f:
        for line in f:
            word = line.strip()
            print(f"Inserting word: {word}")  # 打印插入的单词
            trie.insert(word)
except FileNotFoundError:
    print(f"Error: {file_name} not found.")
    sys.exit(1)

# 保存树到 JSON 文件
trie.to_json(output_file)
print(f"Inserted words from {file_name} and saved to {output_file}")
