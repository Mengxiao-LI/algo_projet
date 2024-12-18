import os
import json
import sys
from hybrid_trie import HybridTrie  
if len(sys.argv) < 2:
    print("Usage: python trie_listeMots.py <file.json>")
    sys.exit(1)


# Obtenir le nom du fichier d'entrée
input_file = sys.argv[1]


# Définir le dossier et le chemin du fichier de sortie
output_folder = "Hybrid_trie/result"  # Dossier de sortie
output_file = os.path.join(output_folder, "profondeur.txt")  # Chemin du fichier de sortie

# S'assurer que le dossier de sortie existe
os.makedirs(output_folder, exist_ok=True)

# Charger l'arbre
try:
    with open(input_file, "r") as f:
        data = json.load(f)
        trie = HybridTrie.from_dict(data)
except FileNotFoundError:
    print(f"Error: {input_file} not found.")
    exit(1)

# Calculer la profondeur moyenne
avg_depth = trie.profondeur_moyenne()

# Sauvegarder les résultats dans un fichier
try:
    with open(output_file, "w") as f:
        f.write(f"{avg_depth}\n")
    print(f"Average depth computed from {input_file} and saved to {output_file}")
except IOError as e:
    print(f"Error writing to {output_file}: {e}")
    exit(1)
