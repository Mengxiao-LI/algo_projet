import sys
import json
import os  
from hybrid_trie import HybridTrie

# Vérifier le nombre de paramètres
if len(sys.argv) < 3:
    print("Usage: python trie_suppression.py x nom_fichier.txt")
    sys.exit(1)

x = int(sys.argv[1])
words_file = sys.argv[2]

# Définir les dossiers et les noms de fichiers
result_dir = "Hybrid_trie/result"
os.makedirs(result_dir, exist_ok=True)  # S'assurer que le dossier existe


input_file = os.path.join(result_dir, "trie.json")
output_file = os.path.join(result_dir, "trie.json")


# Charger un arbre existant ou en créer un nouveau
try:
    with open(input_file, "r") as f:
        data = json.load(f)
        trie = HybridTrie.from_dict(data)
        print(f"Loaded tree from {input_file}.")
        print("Initial words in the tree:", trie.liste_mots())
except FileNotFoundError:
    print(f"File {input_file} not found. Creating a new Trie.")
    trie = HybridTrie()


# Supprimer des mots
try:
    with open(words_file, "r") as f:
        for line in f:
            word = line.strip()
            print(f"Attempting to delete word: '{word}'")
            if trie.recherche(word):  # Vérifier si le mot existe
                trie.suppression(word)
                print(f"Successfully deleted '{word}'.")
            else:
                print(f"Word '{word}' not found in the tree. No action taken.")
except FileNotFoundError:
    print(f"Error: {words_file} not found.")
    sys.exit(1)

# Vérifier si l'arbre est vide
if trie.is_empty():
    print("The tree is completely empty.")
else:
    print("The tree still contains nodes.")

# Sauvegarder l'arbre modifié dans le dossier result
with open(output_file, "w") as f:
    json.dump(trie.to_dict(), f, indent=4)
print(f"Modified tree saved to {output_file}.")
