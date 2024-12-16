import json


class PatriciaTrieNode:
    def __init__(self, label=""):
        self.label = label
        self.children = {}


class PatriciaTrie:
    end_marker = chr(0x00)  # 结束标记符

    def __init__(self):
        self.root = PatriciaTrieNode()
        self.operation_count = {
            "insert_comparisons": 0,
            "search_comparisons": 0,
            "delete_comparisons": 0
        }

    def inserer(self, mot):
        mot += self.end_marker  # 在单词末尾添加结束标记
        node = self.root

        while mot:
            # 直接按首字符查找是否存在匹配的子节点
            self.operation_count["insert_comparisons"] += 1 #查找mot【0】
            if mot[0] in node.children:
                child = node.children[mot[0]]
                # prefix = find_mots_prefix(mot, child.label)
                prefix = find_mots_prefix(
                    mot,
                    child.label,
                    counter_dict=self.operation_count,
                    counter_key="insert_comparisons"
                )
                self.operation_count["insert_comparisons"] += len(prefix)  # 字符逐个比较

                if prefix == child.label:
                    # 完全匹配，进入下一个节点
                    node = child
                    mot = mot[len(prefix):]
                else:
                    # 部分匹配，分裂节点
                    rest = child.label[len(prefix):]
                    new_node = PatriciaTrieNode(prefix)
                    new_node.children[rest[0]] = child
                    child.label = rest
                    node.children[prefix[0]] = new_node
                    node = new_node
                    mot = mot[len(prefix):]
            else:
                # 无共同前缀，直接插入
                new_node = PatriciaTrieNode(mot)
                node.children[mot[0]] = new_node
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

# # 找出前缀.
# def find_mots_prefix(str1, str2):
#     min_len = min(len(str1), len(str2))
#     for i in range(min_len):
#         if str1[i] != str2[i]:
#             return str1[:i]
#     return str1[:min_len]
def find_mots_prefix(str1, str2, counter_dict=None, counter_key=None):
    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        # 如果有计数器传入，则对比较次数自增
        if counter_dict is not None and counter_key is not None:
            counter_dict[counter_key] += 1

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
        arbre.operation_count["search_comparisons"] += 1
        if m[0] not in node.children:
            return False

        child = node.children[m[0]]  # 找到对应的键
        # 使用find_mots_prefix计算公共前缀，从而统计字符比较次数
        prefix = find_mots_prefix(
            m,
            child.label,
            counter_dict=arbre.operation_count,
            counter_key="search_comparisons"
        )

        # 如果公共前缀长度与child.label长度不一致，说明m不以child.label为前缀
        if len(prefix) != len(child.label):
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
        if not common_prefix:
            # 没有公共前缀，直接失败
            return 0
        if len(common_prefix) == len(child.label):
            # 完全匹配子节点的 label
            node = child
            mot = mot[len(common_prefix):]
        else:
            if len(common_prefix) == len(mot):
                new_arbre = PatriciaTrie()
                new_arbre.root = child
                return comptage_mots(new_arbre)
            else:
                return 0



    # 匹配成功，从当前节点开始统计单词数量
    new_arbre = PatriciaTrie()
    new_arbre.root = node
    return comptage_mots(new_arbre)

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
        arbre.operation_count["delete_comparisons"] += 1
        if t not in node.children:
            return node  # 如果子节点不存在，直接返回

        child = node.children[t]
        #prefix = find_mots_prefix(child.label, m)
        prefix = find_mots_prefix(
            child.label,
            m,
            counter_dict=arbre.operation_count,
            counter_key="delete_comparisons"
        )

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

        # 递归处理子节点
        for key, child_data in node_data.get("children", {}).items():
            node.children[key] = _dict_to_node(child_data)

        # 如果当前节点是单词结束
        if node_data.get("is_end_of_word", False):
            if node.children:
                # 如果当前节点有其他子节点，则用子节点方式存放 end_marker
                if PatriciaTrie.end_marker not in node.children:
                    end_marker_node = PatriciaTrieNode(PatriciaTrie.end_marker)
                    node.children[PatriciaTrie.end_marker] = end_marker_node
            else:
                # 没有子节点，直接在 label 中加上结束标记
                node.label += PatriciaTrie.end_marker

        return node

    # 创建 Patricia-Trie，并设置根节点
    trie = PatriciaTrie()
    trie.root = _dict_to_node(data)
    return trie

if __name__ == "__main__":
    # test
    trie = PatriciaTrie()
    words = ["cat", "car", "cart", "bat","batt", "dog"]
    for word in words:
        trie.inserer(word)


    # 打印 Patricia-Trie 的结构
    print("there is "+str(comptage_mots(trie))+" mots in the arbre")
    print("nb Nil in trie "+str(comptage_nil(trie)))
    print("nb Nil in trie no endmarker "+str(comptage_nil_exclude_endmarker(trie)))

    print("hauter: "+str(hauteur(trie)))
    average_depth = profondeurMoyenne(trie)
    print("Average depth of leaves:", average_depth)
    print("nb prefix  'ca' = "+str(prefixe(trie,"ca")))



    trie.display_as_json()
    print("Is car in the tree: "+ str(recherche(trie,"car")))
    suppression(trie,"car")
    print("\nAfter deleting 'car':")
    print("there is "+str(comptage_mots(trie))+" mots in the arbre")
    trie.display_as_json()
    print("Is car in the tree: "+str(recherche(trie,"car")))
    print("Is dfdfdf in the tree: "+str(recherche(trie,"ca")))
    print(liste_mots(trie))

    # 1.3
    sentence = """A quel genial professeur de dactylographie sommes nous redevables de la superbe phrase ci dessous, un
    modele du genre, que toute dactylo connait par coeur puisque elle fait appel a chacune des touches du
    clavier de la machine a ecrire ?"""
    # 将句子拆分成单词（包括标点符号）
    import re
    words = re.findall(r'\b\w+\b|[^\w\s]', sentence)

    # 输出分词结果
    print(words)  # ['A', 'quel', 'genial', 'professeur', 'de', 'dactylographie', ',', 'sommes', '-', 'nous', ...]

    # 将分词结果插入 Patricia-Trie
    trie1 = PatriciaTrie()
    for word in words:
        trie1.inserer(word)

    # 打印 Patricia-Trie 结构
    #trie1.display_as_json()
    print("phrase")
    print(liste_mots(trie1))
    print("there is "+str(comptage_mots(trie1))+" mots in the arbre1")
    print("nb Nil in trie no endmarker "+str(comptage_nil_exclude_endmarker(trie1)))


    def mots_with_end_marker_as_key(trie):
        """arbre 中  key 为 end_marker 的节点"""

        result = []

        def _dfs(node, path):
            # 当前路径上的单词
            current_word = "".join(path + [node.label.rstrip(trie.end_marker)])

            # 如果 children 中有一个 key 是 end_marker 并且对应的子节点是叶子节点
            if trie.end_marker in node.children:
                child = node.children[trie.end_marker]
                if not child.children:  # 确保是叶子节点
                    result.append(current_word)

            # 递归遍历子节点
            for key, child in sorted(node.children.items()):
                _dfs(child, path + [node.label])


        _dfs(trie.root, [])
        return result
    nodes_with_end_marker_as_key = mots_with_end_marker_as_key(trie1)
    print("Nodes with end marker as key:", nodes_with_end_marker_as_key)
    print("nb prefix 'dactylo' = "+str(prefixe(trie1,"dactylo")))


    trie1 = PatriciaTrie()
    trie2 = PatriciaTrie()

    words1 = ["cat", "car", "cart"]
    words2 = ["car", "cattt", "dog", "dart"]

    for word in words1:
        trie1.inserer(word)

    for word in words2:
        trie2.inserer(word)

    # 合并两棵树
    print("Trie 1:")
    trie1.display_as_json()

    print("\nTrie 2:")
    trie2.display_as_json()
    fusion = fusion(trie1, trie2)
    print("\nfusion 3:")
    fusion.display_as_json()
#q5
    json_data = '''

        {
            "label": "",
            "is_end_of_word": false,
            "children": {
                "b": {
                    "label": "bat",
                    "is_end_of_word": true,
                    "children": {}
                },
                "c": {
                    "label": "ca",
                    "is_end_of_word": false,
                    "children": {
                        "r": {
                            "label": "r",
                            "is_end_of_word": true,
                            "children": {
                                "t": {
                                    "label": "t",
                                    "is_end_of_word": true,
                                    "children": {}
                                }
                            }
                        },
                        "t": {
                            "label": "t",
                            "is_end_of_word": true,
                            "children": {}
                        }
                    }
                },
                "d": {
                    "label": "d",
                    "is_end_of_word": false,
                    "children": {
                        "a": {
                            "label": "art",
                            "is_end_of_word": true,
                            "children": {}
                        },
                        "o": {
                            "label": "og",
                            "is_end_of_word": true,
                            "children": {}
                        }
                    }
                }
            }
        }'''

    python_data = json.loads(json_data)

    trie = json_to_patricia_trie(python_data)
    if trie:
        trie.display_as_json()

    print("Is car in the tree: "+str(recherche(trie,"car")))
    print("Is cart in the tree: "+str(recherche(trie,"cart")))
    print(liste_mots(trie))
    print(prefixe(trie, "c"))
