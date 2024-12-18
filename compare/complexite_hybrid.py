import time
import os
import json
import matplotlib.pyplot as plt
import sys
import signal

sys.path.append("../Hybrid_trie")  # Remplacer par le chemin réel du fichier hybrid_trie
from hybrid_trie import HybridTrie


# Définir une exception pour les dépassements de temps
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Timed out!")

signal.signal(signal.SIGALRM, timeout_handler)

def safe_execution(func, *args, timeout=10):
    """Exécution sécurisée d'une fonction avec gestion du dépassement de temps"""
    try:
        signal.alarm(timeout)
        result = func(*args)
        signal.alarm(0)
        return result
    except TimeoutException:
        return float('inf')

def load_words_from_file(file_path, limit):
    """Charger un nombre spécifié de mots depuis un fichier"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().split()
        return content[:limit]

def test_methods(words):
    """Tester toutes les méthodes de Hybrid Trie"""
    hybrid_trie = HybridTrie()
    results = {
        "Recherche": 0,
        "ComptageMots": 0,
        "ListeMots": 0,
        "ComptageNil": 0,
        "Hauteur": 0,
        "ProfondeurMoyenne": 0,
        "Prefixe": 0,
        "Suppression": 0,
    }

    # Insérer des mots dans le Hybrid Trie
    for word in words:
        hybrid_trie.insert(word)

    # Recherche
    start_time = time.time()
    for word in words:
        safe_execution(hybrid_trie.recherche, word, timeout=5)
    results["Recherche"] = time.time() - start_time

    # Comptage des mots
    start_time = time.time()
    safe_execution(hybrid_trie.comptageMots, hybrid_trie.root, timeout=5)
    results["ComptageMots"] = time.time() - start_time

    # Lister tous les mots
    start_time = time.time()
    safe_execution(hybrid_trie.liste_mots, timeout=5)
    results["ListeMots"] = time.time() - start_time

    # Comptage des pointeurs null
    start_time = time.time()
    safe_execution(hybrid_trie.comptage_nil, timeout=5)
    results["ComptageNil"] = time.time() - start_time

    # Hauteur de l'arbre
    start_time = time.time()
    safe_execution(hybrid_trie.hauteur, timeout=5)
    results["Hauteur"] = time.time() - start_time

    # Profondeur moyenne
    start_time = time.time()
    safe_execution(hybrid_trie.profondeur_moyenne, timeout=5)
    results["ProfondeurMoyenne"] = time.time() - start_time

    # Recherche par préfixe
    start_time = time.time()
    safe_execution(hybrid_trie.prefixe, "a", timeout=5)
    results["Prefixe"] = time.time() - start_time

    # Suppression de tous les mots
    start_time = time.time()
    for word in words:
        safe_execution(hybrid_trie.suppression, word, timeout=5)
    results["Suppression"] = time.time() - start_time

    return results

# Initialiser les variables
input_sizes = [0,2000, 4000, 6000, 8000, 10000]
shakespeare_folder = "./Shakespeare"
all_results = {method: [0] * len(input_sizes) for method in ["Recherche", "ComptageMots", "ListeMots", "ComptageNil", "Hauteur", "ProfondeurMoyenne", "Prefixe", "Suppression"]}
file_count = 0

# Parcourir les fichiers et effectuer les tests
for filename in os.listdir(shakespeare_folder):
    file_path = os.path.join(shakespeare_folder, filename)
    if os.path.isfile(file_path):
        print(f"Processing file: {filename}")
        file_count += 1

        for idx, input_size in enumerate(input_sizes):
            words = load_words_from_file(file_path, input_size)
            if not words:
                continue
            results = test_methods(words)

            # Ajouter les résultats
            for method in all_results.keys():
                all_results[method][idx] += results[method]

# Calculer les moyennes
for method in all_results.keys():
    all_results[method] = [time / file_count for time in all_results[method]]

# Chemin pour enregistrer les résultats
result_img_folder = "./result_img/complexity"
os.makedirs(result_img_folder, exist_ok=True)

# Graphe : Recherche et Suppression
plt.figure(figsize=(10, 6))
for method in ["Recherche", "Suppression"]:
    plt.plot(input_sizes, all_results[method], label=method, linewidth=2)
plt.title("Average Execution Time (Hybrid Trie): Recherche and Suppression")
plt.xlabel("Input Size (Number of Words)")
plt.ylabel("Average Execution Time (seconds)")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(os.path.join(result_img_folder, "complexity_Hybrid_recherche_suppression.png"))
plt.show()

# Graphe : Autres méthodes
plt.figure(figsize=(10, 6))
for method in ["ComptageMots", "ListeMots", "ComptageNil", "Hauteur", "ProfondeurMoyenne", "Prefixe"]:
    plt.plot(input_sizes, all_results[method], label=method, linewidth=2)
plt.title("Average Execution Time (Hybrid Trie): Other Methods")
plt.xlabel("Input Size (Number of Words)")
plt.ylabel("Average Execution Time (seconds)")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(os.path.join(result_img_folder, "complexity_Hybrid_other_methods.png"))
plt.show()

print("Hybrid Trie Average Execution analysis completed and plots saved.")
