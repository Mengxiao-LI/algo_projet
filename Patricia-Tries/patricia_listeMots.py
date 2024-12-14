import sys
import json
from patricia import PatriciaTrie, json_to_patricia_trie, liste_mots

def main():
    # 检查参数是否正确
    if len(sys.argv) < 2:
        print("Usage: python patricia_listeMots.py <output_file>")
        sys.exit(1)

    # JSON 文件路径
    input_dir = sys.argv[1]
    output_dir = "Patricia-Tries/result/mot.txt"

    # 从 JSON 文件加载 Patricia Trie
    try:
        with open(input_dir, "r", encoding="utf-8") as f:
            trie_data = json.load(f)
            trie = json_to_patricia_trie(trie_data)
            words = liste_mots(trie)  # 获取 Patricia-Trie 中的所有单词
    except FileNotFoundError:
        print(f"Error: File {input_dir} not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {input_dir}: {e}")
        sys.exit(1)

    # 将单词列表保存到输出文件
    try:
        with open(output_dir, "w", encoding="utf-8") as f:
            for word in words:
                f.write(word + "\n")  # 每个单词写一行
        print(f"Word list has been saved to {output_dir}")
    except IOError as e:
        print(f"Error saving word list to {output_dir}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
