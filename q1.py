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


def profondeur_moyenne(arbre):
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


def suppression(arbre, mot):
    """une fonction qui prend un mot en argument et qui le supprime de l’arbre s’il y figure"""

    def _merge_if_needed(node):
        """检查当前是否可以合并"""
        if len(node.children) == 1 :
            only_child_key, only_child = list(node.children.items())[0]
            # 合并当前节点和唯一子节点的标签
            node.label += only_child.label
            node.children = only_child.children
    def _delete(node, m):
        if not m:  # 如果 m 是空字符串
            if arbre.end_marker in node.children:
                del node.children[arbre.end_marker]
            # 如果当前节点没有子节点，可以标记为删除
            if not node.children:
                return None
            _merge_if_needed(node)
            return node

        t = m[0]
        if t not in node.children:
            return node  # 如果子节点不存在，直接返回

        child = node.children[t]
        prefix = find_mots_prefix(child.label, m)
        if prefix == child.label and len(prefix) == len(m):  # 找到完整单词
            if arbre.end_marker in child.children:
                del child.children[arbre.end_marker]
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

    arbre.root = _delete(arbre.root, mot)
    return arbre


# test
trie = PatriciaTrie()
words = ["cat", "car", "carrrr", "bat","batt", "dog"]
for word in words:
    trie.insert(word)


# 打印 Patricia-Trie 的结构
print("there is "+str(comptage_mots(trie))+" mots in the arbre")
print("nb Nil in trie "+str(comptage_nil(trie)))
print("nb Nil in trie no endmarker "+str(comptage_nil_exclude_endmarker(trie)))

print("hauter: "+str(hauteur(trie)))
average_depth = profondeur_moyenne(trie)
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
    trie1.insert(word)

# 打印 Patricia-Trie 结构
trie1.display_as_json()
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

