import os
import sys
import json
from hybrid_trie import HybridTrie

if len(sys.argv) < 1:
    print("Usage: python trie_listeMots.py <file.json>")
    sys.exit(1)

# Obtenir le nom du fichier d'entrée
input_file = sys.argv[1]


input_path = input_file

# Définir le dossier et le chemin du fichier de sortie
output_folder = "Hybrid_trie/result"  # Dossier de sortie
output_file = os.path.join(output_folder, "mot.txt")

# S'assurer que le dossier de sortie existe
os.makedirs(output_folder, exist_ok=True)

# Charger l'arbre
try:
    with open(input_path, "r") as f:
        trie = HybridTrie.from_dict(json.load(f))
except FileNotFoundError:
    print(f"Error: {input_path} not found.")
    sys.exit(1)

# Lister tous les mots
words = trie.liste_mots()

# Sauvegarder dans un fichier
with open(output_file, "w") as f:
    for word in words:
        f.write(word + "\n")

print(f"Words listed from {input_path} and saved to {output_file}")
