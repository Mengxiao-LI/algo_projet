import sys
import json
from patricia import PatriciaTrie, json_to_patricia_trie, fusion, liste_mots


def main():
    # 检查参数是否正确
    if len(sys.argv) < 3:
        print("Usage: python patricia_fusion.py <input_file1> <input_file2>")
        sys.exit(1)

    input_dir1 = sys.argv[1]  # 第一个 JSON 文件路径
    input_dir2 = sys.argv[2]  # 第二个 JSON 文件路径
    output_dir = "Patricia-Tries/result/pat.json"  # 输出文件路径

    # 从第一个 JSON 文件加载 Patricia Trie
    try:
        with open(input_dir1, "r", encoding="utf-8") as f:
            trie_data1 = json.load(f)
            trie1 = json_to_patricia_trie(trie_data1)
            list1=liste_mots(trie1)
            print(f"trie 1 is {list1} ")
    except FileNotFoundError:
        print(f"Error: File {input_dir1} not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {input_dir1}: {e}")
        sys.exit(1)

    # 从第二个 JSON 文件加载 Patricia Trie
    try:
        with open(input_dir2, "r", encoding="utf-8") as f:
            trie_data2 = json.load(f)
            trie2 = json_to_patricia_trie(trie_data2)
            list2 = liste_mots(trie2)
            print(f"trie 2 is {list2} ")
    except FileNotFoundError:
        print(f"Error: File {input_dir2} not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {input_dir2}: {e}")
        sys.exit(1)

    # 合并两个 Patricia-Tries
    try:
        print("Merging the Patricia-Tries...")
        merged_trie = fusion(trie1, trie2)
        list = liste_mots(merged_trie)
        print(f"Merged trie is {list} ")
    except Exception as e:
        print(f"Error during fusion: {e}")
        sys.exit(1)

    # 将合并后的 Patricia Trie 保存为 JSON 文件
    try:
        with open(output_dir, "w", encoding="utf-8") as f:
            json.dump(merged_trie.to_dict(), f, indent=4)
        print(f"Fused Patricia Trie has been saved to {output_dir}")
    except IOError as e:
        print(f"Error saving fused Patricia Trie to {output_dir}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
