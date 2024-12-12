import sys
import json
from patricia import PatriciaTrie

def main():
    # 检查参数是否正确
    if len(sys.argv) < 3:
        print("Usage: python patricia_inserer.py <x> <word_file>")
        sys.exit(1)

    input_dir = sys.argv[2]  # 第三个参数是输入的单词文件
    output_dir = "Patricia-Tries/result/pat.json"  # 输出 JSON 文件位置

    # 创建 Patricia Trie
    trie = PatriciaTrie()

    # 读取单词文件并插入
    try:
        with open(input_dir, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:  # 忽略空行
                    trie.inserer(word)
    except FileNotFoundError:
        print(f"Error: File {input_dir} not found.")
        sys.exit(1)

    # 将 Patricia Trie 保存为 JSON 文件
    try:
        with open(output_dir, "w", encoding="utf-8") as f:
            json.dump(trie.to_dict(), f, indent=4)
        print(f"Patricia Trie has been saved to {output_dir}")
    except IOError as e:
        print(f"Error saving Patricia Trie to {output_dir}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
