class PatriciaTrieNode:
    def __init__(self, label=""):
        self.label = label  # 节点的字符串内容
        self.children = {}  # 使用普通字典来存储子节点
        self.is_end_of_word = False  # 是否为单词结尾


def _common_prefix(str1, str2):
    #找到两个字符串的共同前缀
    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        if str1[i] != str2[i]:
            return str1[:i]
    return str1[:min_len]


def _insert_in_order(children, key, node):
    #按字母顺序将新节点插入到 children 中
    items = list(children.items())
    for i, (k, v) in enumerate(items):
        if key < k:
            # 在第一个比 key 大的位置插入
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
    def __init__(self):
        self.root = PatriciaTrieNode()

    def insert(self, word):
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
                new_node.is_end_of_word = True
                return
        node.is_end_of_word = True
    




trie = PatriciaTrie()
sentence = "A quel genial professeur de dactylographie sommes nous redevables de la superbe phrase ci dessous un modele du genre que toute dactylo connait par coeur puisque elle fait appel a chacune des touches du clavier de la machine a ecrire"
words = sentence.split()#分开每个字符

for word in words:
    trie.insert(word)


