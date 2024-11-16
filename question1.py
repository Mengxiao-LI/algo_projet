import json


class PatriciaTrieNode:
    def __init__(self, label=""):
        self.label = label  # 节点的字符串内容
        self.children = []  # 使用列表存储子节点


def _common_prefix(str1, str2):
    """找到两个字符串的最长公共前缀"""
    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        if str1[i] != str2[i]:
            return str1[:i]
    return str1[:min_len]


def _insert_in_order(children, node):
    """按字母顺序将新节点插入到 children 列表中"""
    for i, child in enumerate(children):
        if node.label[0] < child.label[0]:
            # 在第一个比当前节点大的位置插入
            children.insert(i, node)
            return
    # 如果没有找到合适位置，则添加到末尾
    children.append(node)


class PatriciaTrie:
    end_marker = chr(0x00)  # 单词结束标记

    def __init__(self):
        self.root = PatriciaTrieNode()

    def insert(self, word):
        word += self.end_marker  # 在单词末尾添加结束标记
        node = self.root
        while word:
            # 查找共同前缀
            found_child = False
            for child in node.children:
                prefix = _common_prefix(word, child.label)
                if prefix:
                    found_child = True
                    if prefix == child.label:
                        # 完全匹配，进入下一个节点
                        node = child
                        word = word[len(prefix):]
                    else:
                        # 如果部分匹配，分裂子节点
                        rest = child.label[len(prefix):]  # 子节点剩余部分
                        new_node = PatriciaTrieNode(prefix)  # 创建新节点保存公共前缀
                        new_node.children.append(child)  # 原子节点挂到新节点下
                        child.label = rest  # 更新原子节点的标签
                        node.children.remove(child)  # 移除旧子节点
                        _insert_in_order(node.children, new_node)
                        node = new_node
                        word = word[len(prefix):]
                    break

            if not found_child:
                # 无共同前缀，直接插入新节点
                # 检查是否已存在重复节点
                for child in node.children:
                    if child.label == word:
                        return  # 如果已存在，不重复插入
                new_node = PatriciaTrieNode(word)
                _insert_in_order(node.children, new_node)
                return

    def to_dict(self, node=None):
        """将 Patricia-Trie 转换为字典形式"""
        if node is None:
            node = self.root

        # 检查 label 是否有结束标志
        is_end_of_word = node.label.endswith(self.end_marker)
        label = node.label.rstrip(self.end_marker) if is_end_of_word else node.label

        # 将 children 转换为字典格式
        children_dict = {
            child.label[0]: self.to_dict(child) for child in node.children
        }

        result = {
            "label": label,
        }

        # 如果是单词结束，添加 is_end_of_word 标志
        if is_end_of_word:
            result["is_end_of_word"] = True

        # 添加 children 信息
        result["children"] = children_dict

        return result

    def display_as_json(self):
        """打印 Patricia-Trie 为 JSON 格式"""
        trie_dict = self.to_dict()
        print(json.dumps(trie_dict, indent=4))


# 示例测试
trie = PatriciaTrie()
words = ["cat", "car", "cart", "bat", "dog"]
for word in words:
    trie.insert(word)

# 打印 Patricia-Trie 的结构
trie.display_as_json()