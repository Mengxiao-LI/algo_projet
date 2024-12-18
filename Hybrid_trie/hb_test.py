# Script de test
import re
from hybrid_trie import HybridTrie

# python hb_test.py

# Créer une instance de HybridTrie
trie = HybridTrie()

# Insérer des mots
words = ["car", "cat", "cart", "dog", "bat"]
print("\n>>> Insertion des mots:")
for word in words:
    print(f"Insertion : {word}")
    trie.insert(word)

# Sauvegarder l'arbre dans un fichier JSON
print("\n>>> Sauvegarder l'arbre dans un fichier JSON:")
trie.to_json("annexes.json")
print("Arbre sauvegardé dans 'annexes.json'")

# Charger l'arbre à partir d'un fichier JSON
print("\n>>> Charger l'arbre à partir d'un fichier JSON:")
loaded_trie = HybridTrie.from_json("annexes.json")
print("Arbre chargé depuis 'annexes.json'")

# Rechercher des mots
print("\n>>> Recherche des mots:")
search_words = ["cat", "rat", "car", "dog"]
for word in search_words:
    result = loaded_trie.recherche(word)
    print(f"Recherche '{word}': {result}")

# Lister tous les mots
print("\n>>> Lister tous les mots:")
all_words = loaded_trie.liste_mots()
print("Tous les mots dans l'arbre :", all_words)

# Compter le nombre de mots
print("\n>>> Nombre total de mots:")
word_count = loaded_trie.comptageMots(loaded_trie.root)
print("Nombre de mots :", word_count)

# Compter le nombre de pointeurs NULL
print("\n>>> Nombre de pointeurs NULL:")
null_count = loaded_trie.comptage_nil() 
print("Nombre de pointeurs NULL :", null_count)

# Calculer la hauteur de l'arbre
print("\n>>> Hauteur de l'arbre:")
tree_height = loaded_trie.hauteur()
print("Hauteur de l'arbre :", tree_height)

# Calculer la profondeur moyenne
print("\n>>> Profondeur moyenne:")
avg_depth = loaded_trie.profondeur_moyenne()
print("Profondeur moyenne :", avg_depth)

# Supprimer des mots
print("\n>>> Suppression des mots:")
words_to_delete = ["cat", "cart"]
for word in words_to_delete:
    print(f"Suppression : {word}")
    loaded_trie.suppression(word)
    print("Après suppression, tous les mots :", loaded_trie.liste_mots())


# Compter le nombre de mots commençant par un préfixe donné
print("\n>>> Compter les mots commençant par 'ca':")
prefix = "ca"
prefix_count = loaded_trie.prefixe(prefix)
print(f"Nombre de mots avec le préfixe '{prefix}' :", prefix_count)

# Sauvegarder à nouveau l'arbre dans un fichier JSON
print("\n>>> Sauvegarder l'arbre modifié dans un fichier JSON:")
loaded_trie.to_json("modified_trie.json")
print("Arbre modifié sauvegardé dans 'modified_trie.json'")

# Tester la fonctionnalité 3.8
print("\n>>> Tester la fonctionnalité 3.8:")

# Créer un arbre non équilibré et un arbre équilibré
trie_unbalanced = HybridTrie()
trie_balanced = HybridTrie()

# Insérer des mots
test_words = [
    "bat", "apple", "banana", "cherry", "dog", "cat", "cart", "car", "date", "elephant",
    "ant", "ball", "zebra", "xylophone", "yak", "queen", "king", "jungle", "house", "mouse",
    "orange", "lemon", "grape", "peach", "melon", "kiwi", "lime", "plum", "pear", "pineapple"
]
for word in test_words:
    trie_unbalanced.insert(word)
    trie_balanced.insert_with_balance(word)

# Comparer la structure des deux arbres
print("\n>>> Arbre non équilibré:")
print("Hauteur de l'arbre :", trie_unbalanced.hauteur())
print("Profondeur moyenne :", trie_unbalanced.profondeur_moyenne())
print("Tous les mots :", trie_unbalanced.liste_mots())

print("\n>>> Arbre équilibré:")
print("Hauteur de l'arbre :", trie_balanced.hauteur())
print("Profondeur moyenne :", trie_balanced.profondeur_moyenne())
print("Tous les mots :", trie_balanced.liste_mots())
