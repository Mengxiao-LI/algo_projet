# 测试脚本
import re
from hybrid_trie import HybridTrie

# python hb_test.py

# 创建 HybridTrie 实例
trie = HybridTrie()

# 插入单词
words = ["car", "cat", "cart", "dog", "bat"]
print("\n>>> Insertion des mots:")
for word in words:
    print(f"Insertion : {word}")
    trie.insert(word)

# 保存树到 JSON 文件
print("\n>>> Sauvegarder l'arbre dans un fichier JSON:")
trie.to_json("annexes.json")
print("Arbre sauvegardé dans 'annexes.json'")

# 从 JSON 文件加载树
print("\n>>> Charger l'arbre à partir d'un fichier JSON:")
loaded_trie = HybridTrie.from_json("annexes.json")
print("Arbre chargé depuis 'annexes.json'")

# 搜索单词
print("\n>>> Recherche des mots:")
search_words = ["cat", "rat", "car", "dog"]
for word in search_words:
    result = loaded_trie.recherche(word)
    print(f"Recherche '{word}': {result}")

# 列出所有单词
print("\n>>> Lister tous les mots:")
all_words = loaded_trie.liste_mots()
print("Tous les mots dans l'arbre :", all_words)

# 统计单词数量
print("\n>>> Nombre total de mots:")
word_count = loaded_trie.comptageMots(loaded_trie.root)
print("Nombre de mots :", word_count)

# 统计 NULL 指针数量
print("\n>>> Nombre de pointeurs NULL:")
null_count = loaded_trie.comptage_nil()  # 修正：不需要显式传递参数
print("Nombre de pointeurs NULL :", null_count)

# 计算树的高度
print("\n>>> Hauteur de l'arbre:")
tree_height = loaded_trie.hauteur()
print("Hauteur de l'arbre :", tree_height)

# 计算平均深度
print("\n>>> Profondeur moyenne:")
avg_depth = loaded_trie.profondeur_moyenne()
print("Profondeur moyenne :", avg_depth)

# 删除单词
print("\n>>> Suppression des mots:")
words_to_delete = ["cat", "cart"]
for word in words_to_delete:
    print(f"Suppression : {word}")
    loaded_trie.suppression(word)
    print("Après suppression, tous les mots :", loaded_trie.liste_mots())

# 统计以指定前缀开头的单词数量
print("\n>>> Compter les mots commençant par 'ca':")
prefix = "ca"
prefix_count = loaded_trie.prefixe(prefix)
print(f"Nombre de mots avec le préfixe '{prefix}' :", prefix_count)

# 再次保存树到 JSON 文件
print("\n>>> Sauvegarder l'arbre modifié dans un fichier JSON:")
loaded_trie.to_json("modified_trie.json")
print("Arbre modifié sauvegardé dans 'modified_trie.json'")

# 测试 3.8 的功能
print("\n>>> Tester la fonctionnalité 3.8:")

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
print("\n>>> Arbre non équilibré:")
print("Hauteur de l'arbre :", trie_unbalanced.hauteur())
print("Profondeur moyenne :", trie_unbalanced.profondeur_moyenne())
print("Tous les mots :", trie_unbalanced.liste_mots())

print("\n>>> Arbre équilibré:")
print("Hauteur de l'arbre :", trie_balanced.hauteur())
print("Profondeur moyenne :", trie_balanced.profondeur_moyenne())
print("Tous les mots :", trie_balanced.liste_mots())
