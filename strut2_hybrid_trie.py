class HybridTrieNode:
    """ 
    Signature = (character: str, is_end_of_word: bool) -> HybridTrieNode
    Description = Représente un noeud dans le Trie hybride, avec des enfants pour les sous-arbres gauche, milieu et droit.
    """
    def __init__(self, character=None, is_end_of_word=False):
        self.character = character  # 节点字符
        self.is_end_of_word = is_end_of_word  # 是否为单词结束
        self.left = None  # 左子树
        self.middle = None  # 中间子树
        self.right = None  # 右子树


class HybridTrie:
    """ 
    Signature = () -> HybridTrie
    Description = Implémente un Trie hybride pour insérer, rechercher, afficher et supprimer les mots dans une structure équilibrée.
    """
    def __init__(self):
        self.root = None

    def insert(self, word):
        """ 
        Signature = (HybridTrie, str) -> None
        Description = Insère un mot dans le Trie hybride, caractère par caractère.
        """
        self.root = self._insert(self.root, word, 0)

    def _insert(self, node, word, index):
        """ 
        Signature = (HybridTrieNode, str, int) -> HybridTrieNode
        Description = Insère un mot de manière récursive dans le Trie hybride en créant ou en accédant aux noeuds appropriés.
        """
        char = word[index]
        if node is None:
            node = HybridTrieNode(char)

        if char < node.character:
            node.left = self._insert(node.left, word, index)
        elif char > node.character:
            node.right = self._insert(node.right, word, index)
        else:
            if index + 1 == len(word):
                node.is_end_of_word = True
            else:
                node.middle = self._insert(node.middle, word, index + 1)
        return node

    def search(self, word):
        """ 
        Signature = (HybridTrie, str) -> bool
        Description = Recherche un mot dans le Trie hybride et retourne True si le mot est trouvé, sinon False.
        """
        return self._search(self.root, word, 0)

    def _search(self, node, word, index):
        """ 
        Signature = (HybridTrieNode, str, int) -> bool
        Description = Recherche récursive d'un mot dans le Trie hybride, caractère par caractère.
        """
        if node is None:
            return False

        char = word[index]
        if char < node.character:
            return self._search(node.left, word, index)
        elif char > node.character:
            return self._search(node.right, word, index)
        else:
            if index + 1 == len(word):
                return node.is_end_of_word
            return self._search(node.middle, word, index + 1)

    def delete(self, word):
        """ 
        Signature = (HybridTrie, str) -> None
        Description = Supprime un mot du Trie hybride s'il existe.
        """
        self.root = self._delete(self.root, word, 0)

    def _delete(self, node, word, index):
        """ 
        Signature = (HybridTrieNode, str, int) -> HybridTrieNode
        Description = Supprime récursivement un mot dans le Trie hybride.
        """
        if node is None:
            return None

        char = word[index]
        if char < node.character:
            node.left = self._delete(node.left, word, index)
        elif char > node.character:
            node.right = self._delete(node.right, word, index)
        else:
            if index + 1 == len(word):
                node.is_end_of_word = False
            else:
                node.middle = self._delete(node.middle, word, index + 1)

            # 如果当前节点不再是单词结尾，且没有子节点，则删除节点
            if not node.is_end_of_word and node.left is None and node.middle is None and node.right is None:
                return None

        return node

    def print_trie(self):
        """ 
        Signature = (HybridTrie) -> None
        Description = Affiche le contenu du Trie hybride en listant tous les mots stockés.
        """
        self._print_trie(self.root, "")

    def _print_trie(self, node, word):
        """ 
        Signature = (HybridTrieNode, str) -> None
        Description = Parcourt récursivement le Trie et imprime les mots lorsqu'un noeud terminal est atteint.
        """
        if node is not None:
            self._print_trie(node.left, word)
            if node.is_end_of_word:
                print(word + node.character)
            self._print_trie(node.middle, word + node.character)
            self._print_trie(node.right, word)


# Test du Trie hybride avec suppression
"""
Signature = () -> None
Description = Insère une série de mots dans le Trie hybride, imprime la structure du Trie, supprime certains mots, et vérifie la recherche des mots restants.
"""
trie = HybridTrie()
sentence = "A quel genial professeur de dactylographie sommes nous redevables de la superbe phrase ci dessous un modele du genre que toute dactylo connait par coeur puisque elle fait appel a chacune des touches du clavier de la machine a ecrire"
words = sentence.split()

# Insérer les mots dans le Trie
for word in words:
    trie.insert(word)

# Afficher la structure du Trie avant suppression
print("Trie contents before deletion:")
trie.print_trie()

# Supprimer des mots
trie.delete("dactylographie")
trie.delete("genial")

# Afficher la structure du Trie après suppression
print("\nTrie contents after deletion:")
trie.print_trie()

# Tester la recherche de mots
print("\nSearch 'dactylographie':", trie.search("dactylographie"))
print("Search 'genial':", trie.search("genial"))
print("Search 'professeur':", trie.search("professeur"))
