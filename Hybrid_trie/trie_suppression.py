import sys
import json
import os  # 用于处理文件夹操作
from hybrid_trie import HybridTrie

# 检查参数数量
if len(sys.argv) < 3:
    print("Usage: python trie_suppression.py x nom_fichier.txt")
    sys.exit(1)

x = int(sys.argv[1])
words_file = sys.argv[2]

# 设置文件夹和文件名
result_dir = "result"
os.makedirs(result_dir, exist_ok=True)  # 确保文件夹存在

if x == 0:
    input_file = os.path.join(result_dir, "pat.json")
    output_file = os.path.join(result_dir, "pat.json")
elif x == 1:
    input_file = os.path.join(result_dir, "trie.json")
    output_file = os.path.join(result_dir, "trie.json")
else:
    print("Error: Invalid value for x. Must be 0 or 1.")
    sys.exit(1)

# 加载现有树或创建新树
try:
    with open(input_file, "r") as f:
        data = json.load(f)
        trie = HybridTrie.from_dict(data)
        print(f"Loaded tree from {input_file}.")
        print("Initial words in the tree:", trie.liste_mots())
except FileNotFoundError:
    print(f"File {input_file} not found. Creating a new Trie.")
    trie = HybridTrie()

# 删除单词
try:
    with open(words_file, "r") as f:
        for line in f:
            word = line.strip()
            print(f"Attempting to delete word: '{word}'")
            if trie.recherche(word):  # 检查单词是否存在
                trie.suppression(word)
                print(f"Successfully deleted '{word}'.")
            else:
                print(f"Word '{word}' not found in the tree. No action taken.")
except FileNotFoundError:
    print(f"Error: {words_file} not found.")
    sys.exit(1)

# 验证树是否为空
if trie.is_empty():
    print("The tree is completely empty.")
else:
    print("The tree still contains nodes.")

# 保存修改后的树到 result 文件夹
with open(output_file, "w") as f:
    json.dump(trie.to_dict(), f, indent=4)
print(f"Modified tree saved to {output_file}.")
