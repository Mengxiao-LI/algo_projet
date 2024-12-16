import os
import json
import sys
from hybrid_trie import HybridTrie  
if len(sys.argv) < 2:
    print("Usage: python trie_listeMots.py <file.json>")
    sys.exit(1)

# 获取输入文件名
input_file = sys.argv[1]


# 定义输出文件夹和文件路径
output_folder = "Hybrid_trie/result"  # 输出文件夹
output_file = os.path.join(output_folder, "profondeur.txt")  # 输出文件路径

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 加载树
try:
    with open(input_file, "r") as f:
        data = json.load(f)
        trie = HybridTrie.from_dict(data)
except FileNotFoundError:
    print(f"Error: {input_file} not found.")
    exit(1)

# 计算平均深度
avg_depth = trie.profondeur_moyenne()

# 保存结果到文件
try:
    with open(output_file, "w") as f:
        f.write(f"{avg_depth}\n")
    print(f"Average depth computed from {input_file} and saved to {output_file}")
except IOError as e:
    print(f"Error writing to {output_file}: {e}")
    exit(1)
