import sys
import json
from patricia import PatriciaTrie, json_to_patricia_trie, prefixe

def main():
    # 检查参数数量是否正确
    if len(sys.argv) < 3:
        print("Usage: python patricia_prefixe.py <x> <arbre.json> <prefix>")
        sys.exit(1)

    # 参数解析

    input_file = sys.argv[1]  # 输入 JSON 文件
    prefix = sys.argv[2]  # 前缀
    output_file = "Patricia-Tries/result/prefixe.txt"  # 结果保存文件


    # 加载 JSON 文件
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            trie_data = json.load(f)
            trie = json_to_patricia_trie(trie_data)  # 转换为 Patricia Trie 对象
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {input_file}: {e}")
        sys.exit(1)

    # 计算前缀的匹配单词数
    try:
        prefix_count = prefixe(trie, prefix)
    except Exception as e:
        print(f"Error calculating prefix count: {e}")
        sys.exit(1)

    # 将结果写入文件
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"{prefix_count}")  # 写入整数，不换行
        print(f"Prefix count ({prefix_count}) has been saved to {output_file}")
    except IOError as e:
        print(f"Error saving prefix count to {output_file}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
