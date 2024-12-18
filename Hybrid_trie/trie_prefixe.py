import os
import sys
import json
from hybrid_trie import HybridTrie

# Vérifier le nombre de paramètres
if len(sys.argv) < 3:
    print("Usage: python trie_prefixe.py <file.json> <prefix>")
    sys.exit(1)

# Définir les chemins d'entrée et de sortie

input_file = sys.argv[1] # Lire le fichier depuis le dossier d'entrée
prefix = sys.argv[2]
output_folder = "Hybrid_trie/result"  # Dossier de sortie
output_file = os.path.join(output_folder, "prefixe.txt")  # Sauvegarder les résultats dans le dossier result

# S'assurer que le dossier de sortie existe
os.makedirs(output_folder, exist_ok=True)

# Charger l'arbre
try:
    with open(input_file, "r") as f:
        trie = HybridTrie.from_dict(json.load(f))
except FileNotFoundError:
    print(f"Error: {input_file} not found.")
    sys.exit(1)

# Calculer le nombre de mots avec le préfixe
prefix_count = trie.prefixe(prefix)

# Sauvegarder les résultats dans un fichier
try:
    with open(output_file, "w") as f:
        f.write(f"{prefix_count}\n")
    print(f"Prefix count for '{prefix}' from {input_file} saved to {output_file}")
except IOError as e:
    print(f"Error writing to {output_file}: {e}")
    sys.exit(1)
