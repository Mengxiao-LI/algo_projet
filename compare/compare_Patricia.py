import time
import os
import json
import sys
import matplotlib.pyplot as plt


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "../Patricia-Tries")
sys.path.append(parent_dir) #Ajouter le chemin du module

from patricia import PatriciaTrie, hauteur,recherche, profondeurMoyenne,suppression  # 从 patricia.py 导入所需函数


input_folder = "./Shakespeare"
output_folder = "./result_Patricia"
test_file = "./test/word.txt"  # test insert new word
os.makedirs(output_folder, exist_ok=True)

print("Constructing Patricia Trie...")
overall_patricia = PatriciaTrie()
start_time_total = time.time()

overall_patricia_total_time = 0  # all construe


file_results = {}

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        print(f"Processing {filename}...")
        file_path = os.path.join(input_folder, filename)
        single_patricia = PatriciaTrie()  # single
        single_patricia_total_time = 0

        single_patricia.operation_count = {
            "insert_comparisons": 0,
            "search_comparisons": 0,
            "delete_comparisons": 0,
        }
        file_start_time = time.time()
        word_count = 0
#test construire
        with open(file_path, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word:

                    start_time = time.time()
                    single_patricia.inserer(word)
                    end_time = time.time()
                    single_patricia_total_time += (end_time - start_time)

                    start_time = time.time()
                    overall_patricia.inserer(word)
                    end_time = time.time()
                    overall_patricia_total_time += (end_time - start_time)

                    word_count += 1
        operation_count= single_patricia.operation_count

        # test recherche
        with open(file_path, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    recherche(single_patricia,word)


        # test insert new word
        with open(test_file, "r") as f:
            test_words = [line.strip().lower() for line in f if line.strip()]

        for word in test_words:
            start_time = time.time()
            single_patricia.inserer(word)
            end_time = time.time()
            insertion_times=end_time - start_time

        sup_cpt=single_patricia.operation_count["delete_comparisons"]
        with open(test_file, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    suppression(single_patricia,word)
        # test suppression
        single_patricia.operation_count["delete_comparisons"]=sup_cpt
        delete_times = []
        with open(test_file, "r") as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    start_time = time.time()
                    suppression(single_patricia, word)
                    end_time = time.time()
                    delete_times.append(end_time - start_time)

        # time of suppression
        total_delete_time = sum(delete_times)


        # result
        file_results[filename] = {
            "Word Count": word_count,
            "Single Construction Time (seconds)": single_patricia_total_time,
            "Overall Construction Time (seconds)": overall_patricia_total_time,
            "Height": hauteur(single_patricia),
            "Average Depth": profondeurMoyenne(single_patricia),
            "Insert Comparisons": operation_count["insert_comparisons"],
            "Search Comparisons": single_patricia.operation_count["search_comparisons"],
            "Delete Comparisons": single_patricia.operation_count["delete_comparisons"],
            "Insertion NEW LIST WORD Times (milliseconds)": insertion_times* 1000000,
            "Total Deletion Time (seconds)": total_delete_time,  # 添加删除时间
        }


with open(os.path.join(output_folder, "file_results_patricia.json"), "w") as file_result_file:
    json.dump(file_results, file_result_file, indent=4)
total_end_time = time.time()

overall_results = {
    "Total Word Count": sum([result["Word Count"] for result in file_results.values()]),
    "Total Construction Time (seconds)": sum([result["Single Construction Time (seconds)"] for result in file_results.values()]),
    "Overall Height": hauteur(overall_patricia),
    "Overall Average Depth": profondeurMoyenne(overall_patricia),
}


with open(os.path.join(output_folder, "overall_results_patricia.json"), "w") as overall_result_file:
    json.dump(overall_results, overall_result_file, indent=4)

print("Patricia Trie results saved to result folder.")

