import os
import json
from hybrid_trie import HybridTrie  

# 定义输入文件夹和文件路径
input_folder = "result"  # 输入文件夹
input_file = os.path.join(input_folder, "trie.json")  # 输入 JSON 文件

# 定义输出文件夹和文件路径
output_folder = "result"  # 输出文件夹
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
