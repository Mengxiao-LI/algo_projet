import sys
import json
from patricia import PatriciaTrie, json_to_patricia_trie, profondeurMoyenne

def main():
    # 检查参数是否正确
    if len(sys.argv) < 2:
        print("Usage: python patricia_profondeurMoyenne.py <json_file>")
        sys.exit(1)

    # 输入文件路径
    input_file = sys.argv[1]
    output_file = "Patricia-Tries/result/profondeur.txt"

    # 从 JSON 文件加载 Patricia-Trie
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
        average_depth = profondeurMoyenne(trie)
    except Exception as e:
        print(f"Error calculating average depth: {e}")
        sys.exit(1)


    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"{average_depth}")
        print(f"Average depth ({average_depth}) has been saved to {output_file}")
    except IOError as e:
        print(f"Error saving average depth to {output_file}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
