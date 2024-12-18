import os
import sys
import json
from hybrid_trie import HybridTrie

# Vérifier le nombre de paramètres
if len(sys.argv) < 3:
    print("Usage: python trie_inserer.py <x> <file.txt>")
    sys.exit(1)

# Analyser les paramètres
x = int(sys.argv[1])
file_name = sys.argv[2]

# Définir le dossier et le nom du fichier de sortie
output_folder = "Hybrid_trie/result"  # Définir le dossier où les résultats seront enregistrés

output_file = os.path.join(output_folder, "trie.json")


# S'assurer que le dossier de sortie existe
os.makedirs(output_folder, exist_ok=True)

# Charger un arbre existant ou en créer un nouveau
try:
    with open(output_file, "r") as f:
        data = json.load(f)
        trie = HybridTrie.from_dict(data)
except FileNotFoundError:
    print(f"File {output_file} not found. Creating a new Trie.")
    trie = HybridTrie()

# Insérer les mots
try:
    with open(file_name, "r") as f:
        for line in f:
            word = line.strip()
            print(f"Inserting word: {word}")  # Afficher le mot inséré
            trie.insert(word)
except FileNotFoundError:
    print(f"Error: {file_name} not found.")
    sys.exit(1)

# Sauvegarder l'arbre dans un fichier JSON
trie.to_json(output_file)
print(f"Inserted words from {file_name} and saved to {output_file}")
