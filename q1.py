import json


class PatriciaTrieNode:
    def __init__(self, label=""):
        self.label = label  # 当前节点的键
        self.children = {}  # 使用键值对存储子节点（字典）


class PatriciaTrie:
    end_marker = chr(0x00)  # 结束标记符

    def __init__(self):
        self.root = PatriciaTrieNode()

    def inserer(self, m):
        m += self.end_marker  # 在单词末尾添加结束标记
        node = self.root
        while m:
            found_child = False
            for key in node.children:
                child = node.children[key]
                prefix = find_mots_prefix(m, child.label)
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


    #辅助函数们
    def to_dict(self, node=None):
        """将 Patricia-Trie 转换为字典形式，正确处理结束标记存储在子节点或当前节点的情况"""
        if node is None:
            node = self.root

        # 初始化结果字典
        result = {
            "label": node.label.rstrip(self.end_marker),  # 去掉结束标记以显示真实单词
            "is_end_of_word": False
        }

        # 判断是否是单词结束
        if node.label.endswith(self.end_marker):  # 自己的 label 包含结束标记
            result["is_end_of_word"] = True
        elif self.end_marker in node.children:  # 子节点包含结束标记
            result["is_end_of_word"] = True

        # 构建子节点，排除显式的结束标记节点
        filtered_children = {
            key: self.to_dict(child)
            for key, child in sorted(node.children.items())
            if key != self.end_marker  # 跳过结束标记节点
        }
        if filtered_children:
            result["children"] = filtered_children
        else:
            result["children"] = {}

        return result

    def display_as_json(self):
        """打印 Patricia-Trie 为 JSON 格式"""
        trie_dict = self.to_dict()
        print(json.dumps(trie_dict, indent=4))

# 找出前缀.
def find_mots_prefix(str1, str2):
    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        if str1[i] != str2[i]:
            return str1[:i]
    return str1[:min_len]

#Question2
def recherche(arbre, m):
    """une fonction de recherche d’un mot dans un dictionnaire"""
    m += arbre.end_marker
    node = arbre.root
    while m:
        # 如果当前字符不在子节点中
        if m[0] not in node.children:
            return False

        child = node.children[m[0]]  # 找到对应的键
        if not m.startswith(child.label):  # 如果标签不匹配，直接返回 False
            return False

        node = child
        m = m[len(child.label):]

    # 如果匹配完成，检查是否包含结束标记
    return arbre.end_marker in node.label

def comptage_mots(arbre):
    """une fonction qui compte les mots présents dans le dictionnaire :"""
    def _nbmots(node):
        cpt = 0
        if node.label.endswith(arbre.end_marker):
            cpt+=1
        for child in node.children.values():
            cpt += _nbmots(child)
        return cpt
    return _nbmots(arbre.root)

def liste_mots(arbre):
    """从 Patricia-Trie 中获取所有单词并返回一个排序后的列表"""
    words = []

    def _aux(node, current_word):
        # 如果当前节点的标签包含结束标记，添加完整单词到结果中
        if node.label.endswith(arbre.end_marker):
            # 去掉结束标记后添加到结果列表
            words.append(current_word + node.label.rstrip(arbre.end_marker))

        # 递归访问子节点
        for key, child in sorted(node.children.items()):
            _aux(child, current_word + node.label)


    _aux(arbre.root, "")
    return words

def comptage_nil(arbre):
    def _count_nil(node):
        # 如果当前节点没有子节点，返回 1
        if not node.children:
            return 1
        return sum(_count_nil(child) for child in node.children.values())

    return _count_nil(arbre.root)

def comptage_nil_exclude_endmarker(arbre):
    """计算 Patricia-Trie 中非结束标记对应的 Nil 指针数量"""
    def _count_nil1(node):
        if not node.children:
            return 1

        return sum(_count_nil1(child) for key, child in node.children.items() if key != arbre.end_marker)
    return _count_nil1(arbre.root)


def hauteur(arbre):
    """计算 Patricia-Trie 的树高度"""

    def _height(node):
        # 如果当前节点没有子节点，返回 0
        if not node.children:
            return 0
        return 1 + max(_height(child) for child in node.children.values())

    # 从根节点开始计算
    return _height(arbre.root)


def profondeurMoyenne(arbre):
    """计算 Patricia-Trie 中叶节点的平均深度"""

    def _aux(node, depth):
        if not node.children:
            # 如果是叶节点，返回深度和计数1
            return depth, 1
        total_depth = 0
        total_leaves = 0
        for child in node.children.values():
            depth_sum, leaf_count = _aux(child, depth + 1)
            total_depth += depth_sum
            total_leaves += leaf_count
        return total_depth, total_leaves

    total_depth, total_leaves = _aux(arbre.root, 0)
    if total_leaves == 0:
        return 0  # 防止除以零
    return total_depth / total_leaves


def prefixe(arbre, mot):
    node = arbre.root
    while mot:
        if mot[0] not in node.children:
            return 0  # 如果前缀不在树中
        child = node.children[mot[0]]
        common_prefix = find_mots_prefix(mot, child.label)
        if common_prefix != child.label:  # 如果前缀部分不匹配
            return 0
        node = child
        mot = mot[len(common_prefix):]

    # 匹配成功，从当前节点开始统计单词数量
    new_arbre = PatriciaTrie()
    new_arbre.root = node
    return comptage_mots(new_arbre)


#
def suppression(arbre, mot):
    """une fonction qui prend un mot en argument et qui le supprime de l’arbre s’il y figure"""

    def _merge_if_needed(node):
        # 如果是根节点，直接返回，不做合并
        if node is arbre.root:
            return
        if len(node.children) == 1 and not node.label.endswith(arbre.end_marker):
            only_child_key, only_child = list(node.children.items())[0]
            # 在此合并
            node.label += only_child.label
            node.children = only_child.children

    def _delete(node, m):
        if not m:  # 如果 m 是空字符串
            if arbre.end_marker in node.children:
                del node.children[arbre.end_marker]
            if not node.children:  # 如果当前节点没有子节点，可以标记为删除
                return None
            _merge_if_needed(node)
            return node

        t = m[0]
        if t not in node.children:
            return node  # 如果子节点不存在，直接返回

        child = node.children[t]
        prefix = find_mots_prefix(child.label, m)

        if prefix == child.label and len(prefix) == len(m):  # 找到完整匹配的节点
            # 首先尝试从子节点中删除结束标记
            if arbre.end_marker in child.children:
                del child.children[arbre.end_marker]
            # 如果子节点中没有结束标记，但 label 中含有 end_marker，则从 label 中移除
            elif child.label.endswith(arbre.end_marker):
                child.label = child.label[:-1]

            # 如果删除结束后此节点没有子节点，且自身也不表示一个词（没有 end_marker 了）
            if not child.children and not child.label.endswith(arbre.end_marker):
                del node.children[t]
                if not node.children:
                    return None

            _merge_if_needed(child)
            return node

        if prefix:  # 如果有前缀，继续递归删除
            result = _delete(child, m[len(prefix):])
            if result is None:  # 如果子节点被标记为删除
                del node.children[t]
                if not node.children:  # 如果当前节点没有子节点，返回 None
                    return None

        _merge_if_needed(node)
        return node

    arbre.root = _delete(arbre.root, mot)or PatriciaTrieNode()
    return arbre

def fusion(a, b):
    """将两个 Patricia-Tries 合并"""
    def _aux(node_a, node_b):
        for key_b, child_b in node_b.children.items():
            if key_b in node_a.children:  # 如果 A 中存在相同的键
                child_a = node_a.children[key_b]
                prefix = find_mots_prefix(child_a.label, child_b.label)

                if prefix == child_a.label and prefix == child_b.label:
                    # 完全匹配，递归合并子节点
                    _aux(child_a, child_b)
                elif prefix:  # 部分匹配
                    # 提取 A 和 B 的剩余部分
                    rest_a = child_a.label[len(prefix):]
                    rest_b = child_b.label[len(prefix):]

                    # 将AB的剩余部分变成新的节点
                    new_a = PatriciaTrieNode(rest_a)
                    new_a.children = child_a.children

                    new_b = PatriciaTrieNode(rest_b)
                    new_b.children = child_b.children

                    # 更新a节点为prefix
                    node_a.children[key_b] = PatriciaTrieNode(prefix)
                    node_a.children[key_b].children = {}

                    # 递归合并 F 和 G 的子节点
                    merged_child = _aux(new_a, new_b)
                    if merged_child:
                        node_a.children[key_b].children[key_b] = merged_child
                else:
                    # 如果没有公共前缀，不应该出现这种情况
                    raise ValueError("Invalid state: overlapping keys with no common prefix")
            else:
                # 如果 A 中不存在对应的键，直接将 B 的子节点复制到 A 中
                node_a.children[key_b] = child_b

        return node_a

    # 从根节点开始合并
    _aux(a.root, b.root)
    return a

def json_to_patricia_trie(data):
    """从 JSON 数据构建 Patricia-Trie"""

    def _dict_to_node(node_data):
        """递归地将 JSON 数据转换为 Patricia-Trie 节点"""
        node = PatriciaTrieNode(node_data["label"])

        # 如果当前节点是单词结束，但仍有子节点，处理为既是结尾又有前缀的情况
        if node_data.get("is_end_of_word", False):
            # 不直接在 label 上添加结束标记符，而是增加一个子节点
            if PatriciaTrie.end_marker not in node.children:
                end_marker_node = PatriciaTrieNode(PatriciaTrie.end_marker)
                node.children[PatriciaTrie.end_marker] = end_marker_node

        # 递归处理子节点
        for key, child_data in node_data.get("children", {}).items():
            node.children[key] = _dict_to_node(child_data)

        return node

    # 创建 Patricia-Trie，并设置根节点
    trie = PatriciaTrie()
    trie.root = _dict_to_node(data)
    return trie
# 测试删除功能
if __name__ == "__main__":
    # 初始化 Patricia Trie
    trie = PatriciaTrie()

    # 测试数据
    words_to_insert = ["cat", "car", "bat", "cart", "dog", "dart"]
    words_to_delete = ["cat", "car", "cart", "dog", "dart", "bat"]
    #words_to_delete = ["dart", "dog"]
    # 插入单词
    for word in words_to_insert:
        trie.inserer(word)

    print("Trie after insertion:")
    trie.display_as_json()

    # 删除单词
    for word in words_to_delete:
        print(f"\nDeleting '{word}'...")
        suppression(trie, word)
        trie.display_as_json()

    # 最终检查是否为空
    print("\nFinal Trie:")
    trie.display_as_json()
    print(liste_mots(trie))


