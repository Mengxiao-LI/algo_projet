import json
import re

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

    @staticmethod
    def from_dict(data):
        """
        从字典数据重建节点
        """
        if data is None:
            return None
        node = HybridTrieNode(data["char"], data["is_end_of_word"])
        node.left = HybridTrieNode.from_dict(data["left"])
        node.middle = HybridTrieNode.from_dict(data["middle"])
        node.right = HybridTrieNode.from_dict(data["right"])
        return node



class HybridTrie:
    """
    混合 Trie 树，支持插入、删除、搜索、深度统计等操作。
    """
    def __init__(self):
        self.root = None

    # 插入功能
    def insert(self, word):
        """插入单词"""
        self.root = self._insert(self.root, word, 0)

    def _insert(self, node, word, index):
        char = word[index]
        if node is None:
            node = HybridTrieNode(char)

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

    # 删除功能
    def suppression(self, word):
        """
        删除混合树中指定的单词。
        """
        def _suppression(node, word, index):
            if node is None:
                return None  # 节点为空，直接返回

            char = word[index]

            if char < node.char:
                # 在左子树中递归删除
                node.left = _suppression(node.left, word, index)
            elif char > node.char:
                # 在右子树中递归删除
                node.right = _suppression(node.right, word, index)
            else:
                # 找到匹配的字符节点
                if index + 1 == len(word):
                    # 到达单词末尾，移除结束标记
                    node.is_end_of_word = False
                else:
                    # 继续处理中间子树
                    node.middle = _suppression(node.middle, word, index + 1)

                # 检查当前节点是否需要删除
                if (
                    not node.is_end_of_word  # 当前节点不再是单词结尾
                    and node.left is None  # 左子树为空
                    and node.middle is None  # 中间子树为空
                    and node.right is None  # 右子树为空
                ):
                    return None  # 删除当前节点

            # 修剪父节点：如果当前节点没有子节点且不是单词结尾，递归删除父节点
            if (
                not node.is_end_of_word
                and node.left is None
                and node.middle is None
                and node.right is None
            ):
                return None  # 返回空节点，表示该节点也被删除

            return node

        # 更新根节点
        self.root = _suppression(self.root, word, 0)

        # 清理根节点：如果根节点已经没有有效内容，清空根节点
        if self.root and not self.root.is_end_of_word and self.root.left is None and self.root.middle is None and self.root.right is None:
            self.root = None



    def is_empty(self):
        """
        检查 Trie 是否完全为空。
        """
        return self.root is None



    # 搜索功能
    def recherche(self, word):
        """搜索单词是否存在"""
        return self._recherche(self.root, word, 0)

    def _recherche(self, node, word, index):
        if node is None:
            return False
        char = word[index]
        if char < node.char:
            return self._recherche(node.left, word, index)
        elif char > node.char:
            return self._recherche(node.right, word, index)
        else:
            if index + 1 == len(word):
                return node.is_end_of_word
            return self._recherche(node.middle, word, index + 1)

    # 列出所有单词
    def liste_mots(self):
        """列出树中的所有单词"""
        result = []
        self._liste_mots(self.root, "", result)
        return result

    def _liste_mots(self, node, prefix, result):
        if node is None:
            return
        self._liste_mots(node.left, prefix, result)
        if node.is_end_of_word:
            result.append(prefix + node.char)
        self._liste_mots(node.middle, prefix + node.char, result)
        self._liste_mots(node.right, prefix, result)


    def comptage_nil(self):
        """
        统计混合树中指向 NULL 的指针数量
        """
        def _comptage_nil(node):
            if node is None:
                return 0

            count = 0
            if node.left is None:
                count += 1
            if node.middle is None:
                count += 1
            if node.right is None:
                count += 1

            count += _comptage_nil(node.left)
            count += _comptage_nil(node.middle)
            count += _comptage_nil(node.right)

            return count

        return _comptage_nil(self.root)

    # 树的高度
    def hauteur(self):
        """计算树的高度"""
        return self._hauteur(self.root)

    def _hauteur(self, node):
        if node is None:
            return 0
        return 1 + max(self._hauteur(node.left), self._hauteur(node.middle), self._hauteur(node.right))

    # 平均深度
    def profondeur_moyenne(self):
        """计算树中叶子的平均深度"""
        result = {"total_depth": 0, "leaf_count": 0}
        self._profondeur_moyenne(self.root, 0, result)
        if result["leaf_count"] == 0:
            return 0
        return result["total_depth"] / result["leaf_count"]

    def _profondeur_moyenne(self, node, depth, result):
        if node is None:
            return
        if node.is_end_of_word:
            result["total_depth"] += depth
            result["leaf_count"] += 1
        self._profondeur_moyenne(node.left, depth + 1, result)
        self._profondeur_moyenne(node.middle, depth + 1, result)
        self._profondeur_moyenne(node.right, depth + 1, result)

    # 以指定前缀开头的单词数量
    def prefixe(self, prefix):
        """统计以指定前缀开头的单词数量"""
        return self._prefixe(self.root, prefix, 0)

    def _prefixe(self, node, prefix, index):
        if node is None:
            return 0
        if index >= len(prefix):
            return self._count_subtree_words(node)
        char = prefix[index]
        if char < node.char:
            return self._prefixe(node.left, prefix, index)
        elif char > node.char:
            return self._prefixe(node.right, prefix, index)
        else:
            if index + 1 == len(prefix):
                return self._count_subtree_words(node.middle)
            return self._prefixe(node.middle, prefix, index + 1)

    def _count_subtree_words(self, node):
        if node is None:
            return 0
        count = 1 if node.is_end_of_word else 0
        count += self._count_subtree_words(node.left)
        count += self._count_subtree_words(node.middle)
        count += self._count_subtree_words(node.right)
        return count

    # 保存和加载功能
    def to_json(self, file_path):
        """将树保存为 JSON 文件"""
        with open(file_path, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    def to_dict(self):
        """将树转换为字典格式"""
        return self.root.to_dict() if self.root else {}
    
    @classmethod
    def from_dict(cls, data):
        """
        从字典加载树。
        如果字典为空（即 {}），返回一个新的空树。
        """
        if not data or data == {}:  # 处理空字典
            return cls()
        trie = cls()
        trie.root = HybridTrieNode.from_dict(data)
        return trie


    @classmethod
    def from_json(cls, file_path):
        """从 JSON 文件加载树"""
        with open(file_path, "r") as f:
            data = json.load(f)
        trie = cls()
        trie.root = HybridTrieNode.from_dict(data)
        return trie
    
    def is_unbalanced(self, depth_threshold=3, balance_threshold=2):
        """判断树是否失衡"""
        max_depth = self.hauteur()
        avg_depth = self.profondeur_moyenne()
        if avg_depth == 0:
            return False

        def max_depth_difference(node):
            if node is None:
                return 0
            left_depth = _hauteur(node.left)
            right_depth = _hauteur(node.right)
            return abs(left_depth - right_depth)

        def _hauteur(node):
            if node is None:
                return 0
            return 1 + max(_hauteur(node.left), _hauteur(node.middle), _hauteur(node.right))

        depth_difference = max_depth_difference(self.root)
        return max_depth / avg_depth > balance_threshold or depth_difference > depth_threshold

    def rebalance(self):
        """重新平衡树"""
        words = self.liste_mots()
        words = sorted(set(words))  # 确保去重并排序
        self.root = self._build_balanced_tree(words, 0, len(words) - 1)

    def _build_balanced_tree(self, words, start, end):
        """构建平衡树"""
        if start > end:
            return None

        mid = (start + end) // 2
        root = HybridTrieNode(words[mid][0])
        root.is_end_of_word = len(words[mid]) == 1
        if len(words[mid]) > 1:
            root.middle = self._build_tree_from_word(words[mid][1:])
        root.left = self._build_balanced_tree(words, start, mid - 1)
        root.right = self._build_balanced_tree(words, mid + 1, end)

        return root

    def _build_tree_from_word(self, word):
        """从单个单词构建一条链式子树"""
        if not word:
            return None
        root = HybridTrieNode(word[0])
        root.is_end_of_word = len(word) == 1
        root.middle = self._build_tree_from_word(word[1:])
        return root

    def insert_with_balance(self, word, depth_threshold=3, balance_threshold=2):
        """插入单词并检测是否需要重新平衡"""
        if word not in self.liste_mots():  # 避免重复插入
            self.insert(word)
        if self.is_unbalanced(depth_threshold, balance_threshold):
            self.rebalance()