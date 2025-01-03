import sys
import json
from patricia import PatriciaTrie, json_to_patricia_trie, suppression


def main():
    if len(sys.argv) < 3:
        print("Usage: python patricia_suppression.py <x> <word_file>")
        sys.exit(1)


    input_dir = sys.argv[2]
    output_dir = "Patricia-Tries/result/pat.json"

    try:
        with open(output_dir, "r", encoding="utf-8") as f:
            trie_data = json.load(f)
            trie = json_to_patricia_trie(trie_data)
    except FileNotFoundError:
        print(f"Error: File {output_dir} not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {output_dir}: {e}")
        sys.exit(1)

    try:
        with open(input_dir, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:
                    trie = suppression(trie, word)
    except FileNotFoundError:
        print(f"Error: File {input_dir} not found.")
        sys.exit(1)

    try:
        with open(output_dir, "w", encoding="utf-8") as f:
            json.dump(trie.to_dict(), f, indent=4)
        print(f"Updated Patricia Trie has been saved to {output_dir}")
    except IOError as e:
        print(f"Error saving Patricia Trie to {output_dir}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
