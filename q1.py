import json


class PatriciaTrieNode:
    def __init__(self, label=""):
        self.label = label  # 当前节点的键
        self.children = {}  # 使用键值对存储子节点（字典）


class PatriciaTrie:
    end_marker = chr(0x00)  # 结束标记符

    def __init__(self):
        self.root = PatriciaTrieNode()

    def insert(self, m):
        m += self.end_marker  # 在单词末尾添加结束标记
        node = self.root
        while m:
            found_child = False
            for key in node.children:
                child = node.children[key]
                prefix = _prefix(m, child.label)
                if prefix:
                    found_child = True
                    if prefix == child.label:
                        # 完全匹配，进入下一个节点
                        node = child
                        m = m[len(prefix):]
                    else:
                        # 部分匹配，分裂节点
                        rest = child.label[len(prefix):]
                        new_node = PatriciaTrieNode(prefix)
                        new_node.children[rest[0]] = child
                        child.label = rest
                        node.children[prefix[0]] = new_node
                        node = new_node
                        m = m[len(prefix):]
                    break

            if not found_child:
                # 无共同前缀，直接插入
                new_node = PatriciaTrieNode(m)
                node.children[m[0]] = new_node
                return

    def delete(self, m):
        """删除 Patricia-Trie 中的单词 m"""

        def _merge_if_needed(node):
            """检查当前是否可以合并"""
            if len(node.children) == 1 :
                only_child_key, only_child = list(node.children.items())[0]
                # 合并当前节点和唯一子节点的标签
                node.label += only_child.label
                node.children = only_child.children
        def _delete(node, m):
            if not m:  # 如果 m 是空字符串
                if self.end_marker in node.children:
                    del node.children[self.end_marker]
                # 如果当前节点没有子节点，可以标记为删除
                if not node.children:
                    return None

                _merge_if_needed(node)

                return node

            t = m[0]
            if t not in node.children:
                return node  # 如果子节点不存在，直接返回

            child = node.children[t]
            prefix = _prefix(child.label, m)

            if prefix == child.label and len(prefix) == len(m):  # 找到完整单词
                if self.end_marker in child.children:
                    del child.children[self.end_marker]
                    # 如果子节点没有其他子节点，将其从父节点中删除
                    if not child.children:
                        del node.children[t]
                        return None if not node.children else node
                    _merge_if_needed(child)

                return node

            if prefix:  # 如果有前缀，继续递归删除
                result = _delete(child, m[len(prefix):])
                if result is None:  # 如果子节点被标记为删除
                    del node.children[t]

            _merge_if_needed(node)

            return node

        # 从根节点开始删除
        self.root = _delete(self.root, m)

    def search(self, m):
        """在 Patricia-Trie 中查找单词 m"""
        m += self.end_marker
        node = self.root
        while m:
            # 如果当前字符不在子节点中/
            if m[0] not in node.children:
                return False

            child = node.children[m[0]]  # 找到对应的键


            if not m.startswith(child.label):  # 如果标签不匹配，直接返回 False
                return False

            node = child
            m = m[len(child.label):]

        # 如果匹配完成，检查是否包含结束标记
        return self.end_marker in node.label

    #辅助函数们
    def to_dict(self, node=None):
        """将 Patricia-Trie 转换为字典形式"""
        if node is None:
            node = self.root

        is_end_of_word = node.label.endswith(self.end_marker)
        # label = node.label.rstrip(self.end_marker) if is_end_of_word else node.label
        label=node.label

        result = {"label": label}
        if is_end_of_word:
            result["is_end_of_word"] = True

        # 按需对 children 的键排序
        result["children"] = {key: self.to_dict(child) for key, child in sorted(node.children.items())}

        return result

    def display_as_json(self):
        """打印 Patricia-Trie 为 JSON 格式"""
        trie_dict = self.to_dict()
        print(json.dumps(trie_dict, indent=4))


# 找出前缀
def _prefix(str1, str2):
    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        if str1[i] != str2[i]:
            return str1[:i]
    return str1[:min_len]


# 示例测试
trie = PatriciaTrie()
words = ["cat", "car", "carrrr", "bat","batt", "dog"]
for word in words:
    trie.insert(word)


# 打印 Patricia-Trie 的结构
trie.display_as_json()
print(trie.search("car"))
trie.delete("car")
print("\nAfter deleting 'car':")
trie.display_as_json()
print(trie.search("car"))
print(trie.search("ca"))

