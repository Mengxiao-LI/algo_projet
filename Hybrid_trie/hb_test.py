# 测试脚本
import re
from hybrid_trie import HybridTrie

# 创建 HybridTrie 实例
trie = HybridTrie()

# 插入单词
words = ["car", "cat", "cart", "dog", "bat"]
print("\n>>> 插入单词:")
for word in words:
    print(f"Inserting: {word}")
    trie.insert(word)

# 保存树到 JSON 文件
print("\n>>> 将树保存为 JSON 文件:")
trie.to_json("annexes.json")
print("Trie saved to annexes.json")

# 从 JSON 文件加载树
print("\n>>> 从 JSON 文件加载树:")
loaded_trie = HybridTrie.from_json("annexes.json")
print("Trie loaded from annexes.json")

# 搜索单词
print("\n>>> 搜索单词:")
search_words = ["cat", "rat", "car", "dog"]
for word in search_words:
    result = loaded_trie.recherche(word)
    print(f"Search '{word}': {result}")

# 列出所有单词
print("\n>>> 列出所有单词:")
all_words = loaded_trie.liste_mots()
print("All words in trie:", all_words)

# 统计单词数量
print("\n>>> 单词总数:")
word_count = len(all_words)
print("Word count:", word_count)

# 统计 NULL 指针数量
print("\n>>> NULL 指针数量:")
null_count = loaded_trie.comptage_nil()  # 修正：不需要显式传递参数
print("Number of NULL pointers:", null_count)

# 计算树的高度
print("\n>>> 树的高度:")
tree_height = loaded_trie.hauteur()
print("Tree height:", tree_height)

# 计算平均深度
print("\n>>> 平均深度:")
avg_depth = loaded_trie.profondeur_moyenne()
print("Average depth:", avg_depth)

# 删除单词
print("\n>>> 删除单词:")
words_to_delete = ["cat", "cart"]
for word in words_to_delete:
    print(f"Deleting: {word}")
    loaded_trie.suppression(word)
    print("After deletion, all words:", loaded_trie.liste_mots())

# 统计以指定前缀开头的单词数量
print("\n>>> 统计以 'ca' 开头的单词数量:")
prefix = "ca"
prefix_count = loaded_trie.prefixe(prefix)
print(f"Number of words with prefix '{prefix}': {prefix_count}")

# 再次保存树到 JSON 文件
print("\n>>> 将修改后的树保存为 JSON 文件:")
loaded_trie.to_json("modified_trie.json")
print("Modified trie saved to modified_trie.json")





# 测试 3.8 的功能
print("\n>>> 测试 3.8 的功能:")

# 创建未平衡和平衡树
trie_unbalanced = HybridTrie()
trie_balanced = HybridTrie()

# 插入单词
test_words = [
    "bat", "apple", "banana", "cherry", "dog", "cat", "cart", "car", "date", "elephant",
    "ant", "ball", "zebra", "xylophone", "yak", "queen", "king", "jungle", "house", "mouse",
    "orange", "lemon", "grape", "peach", "melon", "kiwi", "lime", "plum", "pear", "pineapple"
]
for word in test_words:
    trie_unbalanced.insert(word)
    trie_balanced.insert_with_balance(word)

# 比较两棵树的结构
print("\n>>> 未平衡树:")
print("树的高度:", trie_unbalanced.hauteur())
print("平均深度:", trie_unbalanced.profondeur_moyenne())
print("所有单词:", trie_unbalanced.liste_mots())

print("\n>>> 平衡树:")
print("树的高度:", trie_balanced.hauteur())
print("平均深度:", trie_balanced.profondeur_moyenne())
print("所有单词:", trie_balanced.liste_mots())
