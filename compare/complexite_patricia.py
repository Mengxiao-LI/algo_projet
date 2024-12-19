import time
import os
import matplotlib.pyplot as plt
import sys
import signal

# Ajouter le chemin du module
sys.path.append("../Patricia-Tries")
from patricia import PatriciaTrie, recherche, hauteur, profondeurMoyenne, comptage_mots, liste_mots, comptage_nil, prefixe, suppression


class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Timed out!")

signal.signal(signal.SIGALRM, timeout_handler)

def safe_execution(func, *args, timeout=10):
    try:
        signal.alarm(timeout)
        result = func(*args)
        signal.alarm(0)
        return result
    except TimeoutException:
        return float('inf')

def load_words_from_file(file_path, limit):
    """Lire des mots à partir d'un seul fichier, avec une limite sur le nombre maximal de mots"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().split()
        return content[:limit]

def test_methods(words):
    """test tous les methodes"""
    patricia_trie = PatriciaTrie()
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

    for word in words:
        patricia_trie.inserer(word)


    start_time = time.time()
    for word in words:
        safe_execution(recherche, patricia_trie, word, timeout=5)
    results["Recherche"] = time.time() - start_time

    start_time = time.time()
    safe_execution(comptage_mots, patricia_trie, timeout=5)
    results["ComptageMots"] = time.time() - start_time

    start_time = time.time()
    safe_execution(liste_mots, patricia_trie, timeout=5)
    results["ListeMots"] = time.time() - start_time

    start_time = time.time()
    safe_execution(comptage_nil, patricia_trie, timeout=5)
    results["ComptageNil"] = time.time() - start_time

    start_time = time.time()
    safe_execution(hauteur, patricia_trie, timeout=5)
    results["Hauteur"] = time.time() - start_time

    start_time = time.time()
    safe_execution(profondeurMoyenne, patricia_trie, timeout=5)
    results["ProfondeurMoyenne"] = time.time() - start_time

    start_time = time.time()
    safe_execution(prefixe, patricia_trie, "a", timeout=5)
    results["Prefixe"] = time.time() - start_time

    start_time = time.time()
    for word in words:
        safe_execution(suppression, patricia_trie, word, timeout=5)
    results["Suppression"] = time.time() - start_time

    return results

input_sizes = [1000,2000, 4000, 6000, 8000, 10000]
shakespeare_folder = "../compare/Shakespeare"
all_results = {method: [0] * len(input_sizes) for method in ["Recherche", "ComptageMots", "ListeMots", "ComptageNil", "Hauteur", "ProfondeurMoyenne", "Prefixe", "Suppression"]}
file_count = 0  # for average


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


            for method in all_results.keys():
                all_results[method][idx] += results[method]

# Average
for method in all_results.keys():
    all_results[method] = [time / file_count for time in all_results[method]]


result_img_folder = "./result_img/complexity"
os.makedirs(result_img_folder, exist_ok=True)

# dessine les graphe
# graphe 1: Recherche et Suppression
plt.figure(figsize=(10, 6))
for method in ["Recherche", "Suppression"]:
    plt.plot(input_sizes, all_results[method], label=method, linewidth=2)

plt.title("Average Execution Time (Patricia-Trie): Recherche and Suppression", fontsize=14)
plt.xlabel("Input Size (Number of Words)", fontsize=12)
plt.ylabel("Average Execution Time (seconds)", fontsize=12)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(os.path.join(result_img_folder, "complexity_Patricia_recherche_suppression.png"))
plt.show()

# 2: autre methode
plt.figure(figsize=(10, 6))
for method in ["ComptageMots", "ListeMots", "ComptageNil", "Hauteur", "ProfondeurMoyenne", "Prefixe"]:
    plt.plot(input_sizes, all_results[method], label=method, linewidth=2)

plt.title("Average Execution Time (Patricia-Trie): Other Methods", fontsize=14)
plt.xlabel("Input Size (Number of Words)", fontsize=12)
plt.ylabel("Average Execution Time (seconds)", fontsize=12)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(os.path.join(result_img_folder, "complexity_Patricia_other_methods.png"))
plt.show()

print("Patricia-Trie Average Execution analysis completed and plots saved.")
