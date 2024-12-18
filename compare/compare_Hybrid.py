import time
import os
import json
import sys
import matplotlib.pyplot as plt

# Ajouter le chemin du module HybridTrie
sys.path.append("../Hybrid_trie")
from hybrid_trie import HybridTrie

# Définir les chemins
input_folder = "./Shakespeare"  # Chemin du dossier contenant les fichiers Shakespeare
output_folder = "./result"      # Dossier pour les résultats
test_file = "./test/word.txt"  # Chemin du fichier de test pour les nouveaux mots
os.makedirs(output_folder, exist_ok=True)

# Initialiser les chronomètres et les résultats
file_results = {}

# Test de Hybrid Trie
print("Constructing Hybrid Trie...")
overall_trie = HybridTrie()
start_time_total = time.time()
 # Temps total de construction pour le Patricia global
overall_patricia_total_time = 0

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        print(f"Processing {filename}...")
        file_path = os.path.join(input_folder, filename)
        single_trie = HybridTrie()
        single_patricia_total_time = 0

        # Réinitialiser le compteur d'opérations
        single_trie.operation_count = {
            "insert_comparisons": 0,
            "search_comparisons": 0,
            "delete_comparisons": 0,
        }

        file_start_time = time.time()
        word_count = 0

        # Insérer des mots
        with open(file_path, "r") as file:
            for line in file:
                word = line.strip().lower()  # Prétraiter le mot
                if word:
                    # Enregistrer le temps d'insertion pour single_patricia
                    start_time = time.time()
                    single_trie.insert(word)  # Insérer dans le Patricia Trie pour le fichier actuel
                    end_time = time.time()
                    single_patricia_total_time += (end_time - start_time)

                    # Enregistrer le temps d'insertion pour overall_patricia
                    start_time = time.time()
                    overall_trie.insert(word)  # Insérer dans le Patricia Trie global
                    end_time = time.time()
                    overall_patricia_total_time += (end_time - start_time)

                    word_count += 1
        operation_count=single_trie.operation_count

        # Test de recherche
        with open(file_path, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    single_trie.recherche(word)

        # Insérer de nouveaux mots et enregistrer le temps
        # Lire les mots de test
        with open(test_file, "r") as f:
            test_words = [line.strip().lower() for line in f if line.strip()]
        for word in test_words:
            start_time = time.time()
            single_trie.insert(word)
            end_time = time.time()
            insertion_times= end_time - start_time
        # Test de suppression
        with open(test_file, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    single_trie.suppression(word)  # Opération de suppression

        # Test de suppression avec enregistrement du temps
        delete_times = []
        with open(test_file, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    start_time = time.time()  # Heure de début
                    single_trie.suppression(word)  # Opération de suppression
                    end_time = time.time()  # Heure de fin
                    delete_times.append(end_time - start_time)  # Enregistrer le temps de suppression

        # Calculer le temps total de suppression
        total_delete_time = sum(delete_times)

        # Enregistrer les résultats pour le fichier actuel
        file_results[filename] = {
            "Word Count": word_count,
            "Single Construction Time (seconds)": single_patricia_total_time,
            "Overall Construction Time (seconds)": overall_patricia_total_time,
            "Height": single_trie.hauteur(),
            "Average Depth": single_trie.profondeur_moyenne(),
            "Insert Comparisons": operation_count["insert_comparisons"],
            "Search Comparisons": single_trie.operation_count["search_comparisons"],
            "Delete Comparisons": single_trie.operation_count["delete_comparisons"],
            "Insertion NEW LIST WORD Times (milliseconds)": insertion_times * 1000000,
            "Total Deletion Time (seconds)": total_delete_time,  # 添加删除时间
        }


total_end_time = time.time()

# Résultats globaux
overall_results = {
    "Total Word Count": sum([result["Word Count"] for result in file_results.values()]),
    "Total Construction Time (seconds)": sum([result["Single Construction Time (seconds)"] for result in file_results.values()]),
    "Overall Height": overall_trie.hauteur(),
    "Overall Average Depth": overall_trie.profondeur_moyenne(),
}

# Sauvegarder dans un fichier JSON
with open(os.path.join(output_folder, "file_results.json"), "w") as file_result_file:
    json.dump(file_results, file_result_file, indent=4)

with open(os.path.join(output_folder, "overall_results.json"), "w") as overall_result_file:
    json.dump(overall_results, overall_result_file, indent=4)

print("Hybrid Trie results saved to result folder.")
