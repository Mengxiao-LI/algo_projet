import sys
import json
from patricia import PatriciaTrie

def main():

    if len(sys.argv) < 3:
        print("Usage: python patricia_inserer.py <x> <word_file>")
        sys.exit(1)

    input_dir = sys.argv[2]  # input
    output_dir = "Patricia-Tries/result/pat.json"  # output

    trie = PatriciaTrie()

    # insert les mots
    try:
        with open(input_dir, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:
                    trie.inserer(word)
    except FileNotFoundError:
        print(f"Error: File {input_dir} not found.")
        sys.exit(1)

    #  Patricia Trie to JSON
    try:
        with open(output_dir, "w", encoding="utf-8") as f:
            json.dump(trie.to_dict(), f, indent=4)
        print(f"Patricia Trie has been saved to {output_dir}")
    except IOError as e:
        print(f"Error saving Patricia Trie to {output_dir}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
