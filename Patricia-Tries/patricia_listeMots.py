import sys
import json
from patricia import PatriciaTrie, json_to_patricia_trie, liste_mots

def main():
    if len(sys.argv) < 2:
        print("Usage: python patricia_listeMots.py <output_file>")
        sys.exit(1)


    input_dir = sys.argv[1]
    output_dir = "Patricia-Tries/result/mot.txt"
#list mots
    try:
        with open(input_dir, "r", encoding="utf-8") as f:
            trie_data = json.load(f)
            trie = json_to_patricia_trie(trie_data)
            words = liste_mots(trie)
    except FileNotFoundError:
        print(f"Error: File {input_dir} not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {input_dir}: {e}")
        sys.exit(1)

    try:
        with open(output_dir, "w", encoding="utf-8") as f:
            for word in words:
                f.write(word + "\n")  # chaque mot accupe une ligne
        print(f"Word list has been saved to {output_dir}")
    except IOError as e:
        print(f"Error saving word list to {output_dir}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
