import json

class HybridTrieNode:
    """
    节点结构：
    - char: 当前字符
    - is_end_of_word: 是否为单词结束（相当于 end_marker）
    - left: 左子节点
    - middle: 中间子节点
    - right: 右子节点
    """
    def __init__(self, char=None, is_end_of_word=False):
        self.char = char
        self.is_end_of_word = is_end_of_word
        self.left = None
        self.middle = None
        self.right = None

    def to_dict(self):
        """将节点递归转换为字典格式"""
        return {
            "char": self.char,
            "is_end_of_word": self.is_end_of_word,
            "left": self.left.to_dict() if self.left else None,
            "middle": self.middle.to_dict() if self.middle else None,
            "right": self.right.to_dict() if self.right else None,
        }


class HybridTrie:
    """
    混合 Trie 树，支持插入、搜索、删除操作
    """
    def __init__(self):
        self.root = None
       
    def insert(self, word):
        """插入单词"""
        self.root = self._insert(self.root, word, 0)
    

    def _insert(self, node, word, index):
        char = word[index]
        if node is None:
            node = HybridTrieNode(char)
        print(f"Inserting '{char}' at level {index} -> Current Node: {node.char if node else 'None'}")

        if char < node.char:
            node.left = self._insert(node.left, word, index)
        elif char > node.char:
            node.right = self._insert(node.right, word, index)
        else:
            if index + 1 == len(word):
                node.is_end_of_word = True
            else:
                node.middle = self._insert(node.middle, word, index + 1)

        return node
    
    def to_json(self):
        """将整个树转化为 JSON 格式"""
        if self.root is None:
            return json.dumps({})
        return json.dumps(self.root.to_dict(), ensure_ascii=False, indent=4)


    
    

    ########################################################
    #Question 2
    
    

def recherche(arbre, mot):
    """
    搜索一个单词是否存在于混合树中。

    参数:
        arbre: 混合树的根节点 (HybridTrie 对象)。
        mot: 要搜索的单词 (字符串)。

    返回值:
        布尔值 True 或 False,表示单词是否存在。
    """
    def _recherche(node, word, index):
        if node is None:  # 当前节点为空，返回 False
            return False
        char = word[index]  # 当前单词字符
        if char < node.char:  # 在左子树中查找
            return _recherche(node.left, word, index)
        elif char > node.char:  # 在右子树中查找
            return _recherche(node.right, word, index)
        else:  # 字符匹配
            if index + 1 == len(word):  # 到达单词末尾
                return node.is_end_of_word  # 检查是否是单词的结尾
            return _recherche(node.middle, word, index + 1)

    return _recherche(arbre.root, mot, 0)





def comptage_mots(arbre):
    """
    统计混合树中存储的单词数量。

    参数:
        arbre: 混合树的根节点 (HybridTrie 对象)。

    返回值:
        树中单词的总数量 (整数)。
    """
    def _comptage_mots(node):
        if node is None:  # 节点为空，返回 0
            return 0
        count = 1 if node.is_end_of_word else 0  # 如果节点是单词结尾，计数加 1
        count += _comptage_mots(node.left)  # 递归统计左子树
        count += _comptage_mots(node.middle)  # 递归统计中间子树
        count += _comptage_mots(node.right)  # 递归统计右子树
        return count

    return _comptage_mots(arbre.root)

def liste_mots(arbre):
    """
    列出混合树中存储的所有单词，按字母顺序排列。

    参数:
        arbre: 混合树的根节点 (HybridTrie 对象)。

    返回值:
        包含所有单词的列表 (列表形式)。
    """
    def _liste_mots(node, prefix, result):
        if node is None:  # 节点为空，直接返回
            return
        _liste_mots(node.left, prefix, result)  # 遍历左子树
        if node.is_end_of_word:  # 如果当前节点是单词结尾
            result.append(prefix + node.char)  # 将单词添加到结果列表
        _liste_mots(node.middle, prefix + node.char, result)  # 遍历中间子树
        _liste_mots(node.right, prefix, result)  # 遍历右子树

    result = []
    _liste_mots(arbre.root, "", result)
    return result





def comptage_nil(node):
    """
    统计混合树中指向 NULL 的指针数量。

    参数:
        node: 当前节点 (HybridTrieNode 对象)。

    返回值:
        NULL 指针的总数量 (整数)。
    """
    if node is None:
        return 0  # 当前节点为空，返回 3（因为它的左、中、右指针均为 NULL）

    # 当前节点存在，统计其子指针中的 NULL 数量
    count = 0
    if node.left is None:
        count += 1
    if node.middle is None:
        count += 1
    if node.right is None:
        count += 1

    # 递归处理左右中子树
    count += comptage_nil(node.left)
    count += comptage_nil(node.middle)
    count += comptage_nil(node.right)

    return count


def hauteur(arbre):
    """
    计算混合树的高度 (从根节点到叶子节点的最大深度)。

    参数:
        arbre: 混合树的根节点 (HybridTrie 对象)。

    返回值:
        树的高度 (整数)。
    """
    def _hauteur(node):
        if node is None:  # 节点为空，高度为 0
            return 0
        # 递归计算左、中、右子树的最大高度
        return 1 + max(_hauteur(node.left), _hauteur(node.middle), _hauteur(node.right))

    return _hauteur(arbre.root)



def profondeur_moyenne(arbre):
    """
    计算混合树中所有叶子节点的平均深度。

    参数:
        arbre: 混合树的根节点 (HybridTrie 对象)。

    返回值:
        平均深度 (浮点数)。
    """
    def _profondeur_moyenne(node, depth, result):
        if node is None:  # 节点为空，直接返回
            return
        if node.is_end_of_word:  # 如果节点是单词结尾
            result["total_depth"] += depth  # 累计深度
            result["leaf_count"] += 1  # 叶子节点计数
        _profondeur_moyenne(node.left, depth + 1, result)  # 遍历左子树
        _profondeur_moyenne(node.middle, depth + 1, result)  # 遍历中间子树
        _profondeur_moyenne(node.right, depth + 1, result)  # 遍历右子树

    result = {"total_depth": 0, "leaf_count": 0}
    _profondeur_moyenne(arbre.root, 0, result)
    if result["leaf_count"] == 0:  # 如果没有叶子节点，平均深度为 0
        return 0
    return result["total_depth"] / result["leaf_count"]


def prefixe(arbre, mot):
    """
    统计混合树中以指定前缀开头的单词数量。

    参数:
        arbre: 混合树的根节点 (HybridTrie 对象)。
        mot: 前缀字符串。

    返回值:
        以指定前缀开头的单词数量 (整数)。
    """
    def _prefixe(node, word, index):
        if node is None:  # 节点为空，返回 0
            return 0
        char = word[index] if index < len(word) else None
        if char is None:  # 前缀结束，统计子树中所有单词
            return comptage_mots_subtree(node)
        if char < node.char:  # 前缀字母小于当前节点，去左子树
            return _prefixe(node.left, word, index)
        elif char > node.char:  # 前缀字母大于当前节点，去右子树
            return _prefixe(node.right, word, index)
        else:  # 字母匹配
            if index + 1 == len(word):  # 前缀的最后一个字母
                return comptage_mots_subtree(node.middle)
            return _prefixe(node.middle, word, index + 1)

    def comptage_mots_subtree(node):
        if node is None:
            return 0
        count = 1 if node.is_end_of_word else 0
        count += comptage_mots_subtree(node.left)
        count += comptage_mots_subtree(node.middle)
        count += comptage_mots_subtree(node.right)
        return count

    return _prefixe(arbre.root, mot, 0)


def suppression(arbre, mot):
    """
    删除混合树中指定的单词。

    参数:
        arbre: 混合树的根节点 (HybridTrie 对象)。
        mot: 要删除的单词 (字符串)。

    返回值:
        无返回值，直接修改树的结构。
    """
    def _suppression(node, word, index):
        if node is None:
            return None
        
        char = word[index]
        
        if char < node.char:  # 去左子树
            node.left = _suppression(node.left, word, index)
        elif char > node.char:  # 去右子树
            node.right = _suppression(node.right, word, index)
        else:  # 字符匹配
            if index + 1 == len(word):  # 单词末尾
                node.is_end_of_word = False
            else:  # 继续检查中间子树
                node.middle = _suppression(node.middle, word, index + 1)
            
            # 检查是否需要删除当前节点
            if (
                not node.is_end_of_word  # 当前节点不再是单词的结束
                and node.left is None  # 左子树为空
                and node.middle is None  # 中间子树为空
                and node.right is None  # 右子树为空
            ):
                return None  # 删除当前节点
            
        return node

    arbre.root = _suppression(arbre.root, mot, 0)


    

# 测试
trie = HybridTrie()

# 插入单词
words = ["car", "cat", "cart", "dog", "bat"]
for word in words:
    trie.insert(word)


# 输出树的 JSON 表示
print(trie.to_json())


print("\n>>> 搜索单词:")
print(f"Search 'cat': {recherche(trie, 'cat')}")
print(f"Search 'rat': {recherche(trie, 'rat')}")


print("\n>>> 单词总数:", comptage_mots(trie))
print("\n>>> 所有单词:", liste_mots(trie))


print("\n>>> NULL 指针数量:", comptage_nil(trie.root))


print("\n>>> 树的高度:", hauteur(trie))


print("\n>>> 平均深度:", profondeur_moyenne(trie))


print("\n>>> 以 'ca' 开头的单词数量:", prefixe(trie, "ca"))


print("\n>>> 删除单词:")
for word in ["cat", "cart"]:
    suppression(trie, word)
    print(f"After deleting '{word}', words: {liste_mots(trie)}")











