import json


class PatriciaTrieNode:
    def __init__(self, label=""):
        self.label = label  # 内容
        self.children = {}  # 键值对[key,node]


def _common_prefix(str1, str2):
    # 找到两个字符串的最长公共前缀
    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        if str1[i] != str2[i]:
            return str1[:i]
    return str1[:min_len]


def _insert_in_order(children, key, node):
    # 按字母顺序将新节点插入到 children 中
    items = list(children.items())
    for i, (k, v) in enumerate(items):
        if key < k:
            # 插入到i的位置
            items.insert(i, (key, node))
            break
    else:
        # 如果 key 比所有现有键都大，则将其添加到末尾
        items.append((key, node))

    # 清空原字典并重新按顺序插入
    children.clear()
    for k, v in items:
        children[k] = v


class PatriciaTrie:
    end_marker = chr(0x00)  # 结束标记

    def __init__(self):
        self.root = PatriciaTrieNode()

    def insert(self, word):
        word += self.end_marker  # 在单词末尾添加结束标记
        node = self.root
        while word:
            # 查找共同前缀
            found_child = False
            for key in node.children:
                child = node.children[key]
                prefix = _common_prefix(word, child.label)
                if prefix:
                    found_child = True
                    if prefix == child.label:
                        # 完全匹配，进入下一个节点
                        node = child
                        word = word[len(prefix):]
                    else:
                        # 部分匹配，分裂节点
                        rest = child.label[len(prefix):]
                        new_node = PatriciaTrieNode(prefix)
                        new_node.children[rest[0]] = child
                        child.label = rest
                        _insert_in_order(node.children, prefix[0], new_node)
                        node = new_node
                        word = word[len(prefix):]
                    break

            if not found_child:
                # 无共同前缀，直接插（字母顺序）
                new_node = PatriciaTrieNode(word)
                _insert_in_order(node.children, word[0], new_node)
                return

    #将 Patricia-Trie 转换为字典形式
    def to_dict(self, node=None):
        if node is None:
            node = self.root

        # 检查 label 是否有结束标志
        is_end_of_word = node.label.endswith(self.end_marker)
        label = node.label.rstrip(self.end_marker) if is_end_of_word else node.label

        result = {
            "label": label,
        }

        # 如果是单词结束，添加 is_end_of_word 标志
        if is_end_of_word:
            result["is_end_of_word"] = True

        # 添加 children 信息
        result["children"] = {key: self.to_dict(child) for key, child in node.children.items()}

        return result

    #打印 Patricia-Trie 为 JSON 格式
    def display_as_json(self):
        trie_dict = self.to_dict()
        print(json.dumps(trie_dict, indent=4))


# 示例测试
trie = PatriciaTrie()
words = ["cat", "car", "cart", "bat", "dog"]
for word in words:
    trie.insert(word)

# 打印 Patricia-Trie 的结构
trie.display_as_json()
