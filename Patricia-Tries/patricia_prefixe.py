import sys
import json
from patricia import PatriciaTrie, json_to_patricia_trie, prefixe

def main():

    if len(sys.argv) < 3:
        print("Usage: python patricia_prefixe.py <x> <arbre.json> <prefix>")
        sys.exit(1)


    input_file = sys.argv[1]
    prefix = sys.argv[2]
    output_file = "Patricia-Tries/result/prefixe.txt"


    try:
        with open(input_file, "r", encoding="utf-8") as f:
            trie_data = json.load(f)
            trie = json_to_patricia_trie(trie_data)
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {input_file}: {e}")
        sys.exit(1)

    try:
        prefix_count = prefixe(trie, prefix)
    except Exception as e:
        print(f"Error calculating prefix count: {e}")
        sys.exit(1)

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"{prefix_count}")
        print(f"Prefix count ({prefix_count}) has been saved to {output_file}")
    except IOError as e:
        print(f"Error saving prefix count to {output_file}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
