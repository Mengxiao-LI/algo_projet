import sys
import json
import os
from hybrid_trie import HybridTrie

# 检查参数数量
if len(sys.argv) < 3:
    print("Usage: python trie_fusion.py <file1.json> <file2.json>")
    sys.exit(1)

file1 = sys.argv[1]
file2 = sys.argv[2]

# 设置结果文件夹路径
result_dir = "Hybrid_trie/result"
os.makedirs(result_dir, exist_ok=True)  # 确保结果文件夹存在

# 将文件路径调整为 result 文件夹中的文件
file1_path = os.path.join(result_dir, file1)
file2_path = os.path.join(result_dir, file2)
output_file = os.path.join(result_dir, "trie.json")  # 合并后的结果文件

# 加载两棵树
try:
    with open(file1_path, "r") as f1:
        trie1 = HybridTrie.from_dict(json.load(f1))
except FileNotFoundError:
    print(f"Error: {file1_path} not found.")
    sys.exit(1)

try:
    with open(file2_path, "r") as f2:
        trie2 = HybridTrie.from_dict(json.load(f2))
except FileNotFoundError:
    print(f"Error: {file2_path} not found.")
    sys.exit(1)

# 融合两棵树
all_words = set(trie1.liste_mots() + trie2.liste_mots())  # 合并去重的单词列表
fused_trie = HybridTrie()
for word in all_words:
    fused_trie.insert(word)

# 保存融合后的树到 result 文件夹
fused_trie.to_json(output_file)
print(f"Fusion of {file1} and {file2} saved to {output_file}")

# 打印两棵树的单词列表
words1 = trie1.liste_mots()
words2 = trie2.liste_mots()
fused_words = fused_trie.liste_mots()

print(f"Words in {file1}: {words1}")
print(f"Words in {file2}: {words2}")
print(f"Words in the fused trie: {fused_words}")

# 验证融合是否正确
if set(fused_words) == set(words1 + words2):
    print("Fusion is correct: All words from both tries are present.")
else:
    print("Fusion is incorrect: Missing or duplicate words detected.")
