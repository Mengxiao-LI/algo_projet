import json
import os
import re



class HybridTrieNode:
    """
    Structure du nœud :
    - char : caractère actuel
    - is_end_of_word : est-ce la fin d'un mot (équivalent à end_marker)
    - left : nœud enfant gauche
    - middle : nœud enfant central
    - right : nœud enfant droit
    """
    def __init__(self, char=None, is_end_of_word=False):
        self.char = char
        self.is_end_of_word = is_end_of_word
        self.left = None
        self.middle = None
        self.right = None

    def to_dict(self):
        """Convertir récursivement le nœud en format dictionnaire"""
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
        Reconstruire un nœud à partir d'un dictionnaire
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
    Trie hybride, supporte les opérations d’insertion, suppression, recherche, statistiques de profondeur, etc.
    """
    def __init__(self):
        self.root = None
        self.operation_count = {
            "insert_comparisons": 0,
            "search_comparisons": 0,
            "delete_comparisons": 0
        }

    
    def insert(self, word):
        """Insérer un mot"""
        self.root = self._insert(self.root, word, 0)

    def _insert(self, node, word, index):
        char = word[index]
        if node is None:
            node = HybridTrieNode(char)

        if char < node.char:
            self.operation_count["insert_comparisons"] += 1  # Enregistrer le nombre de comparaisons
            node.left = self._insert(node.left, word, index)
        elif char > node.char:
            self.operation_count["insert_comparisons"] += 1
            node.right = self._insert(node.right, word, index)
        else:
            if index + 1 == len(word):
                node.is_end_of_word = True
            else:
                node.middle = self._insert(node.middle, word, index + 1)

        return node

 
    def suppression(self, word):
        """
        Supprimer un mot spécifique dans le Trie hybride.
        """
        def _suppression(node, word, index):
            if node is None:
                return None  # Le nœud est vide, retourner directement

            char = word[index]
            self.operation_count["delete_comparisons"] += 1  # 记录比较次数


            if char < node.char:
                # Supprimer de manière récursive dans le sous-arbre gauche
                node.left = _suppression(node.left, word, index)
            elif char > node.char:
                # Supprimer de manière récursive dans le sous-arbre droit
                node.right = _suppression(node.right, word, index)
            else:
                # Trouver le nœud correspondant au caractère
                if index + 1 == len(word):
                    # À la fin du mot, retirer le marqueur de fin
                    node.is_end_of_word = False
                else:
                    # Continuer à traiter le sous-arbre central
                    node.middle = _suppression(node.middle, word, index + 1)

                # Vérifier si le nœud actuel doit être supprimé
                if (
                    not node.is_end_of_word  # Le nœud actuel n'est plus la fin d'un mot
                    and node.left is None  # Le sous-arbre est vide
                    and node.middle is None  
                    and node.right is None  
                ):
                    return None  # Supprimer le nœud actuel

            # Élaguer le nœud parent si nécessaire
            if (
                not node.is_end_of_word
                and node.left is None
                and node.middle is None
                and node.right is None
            ):
                return None  # Retourner un nœud vide pour indiquer qu'il a été supprimé


            return node

        # Mettre à jour le nœud racine
        self.root = _suppression(self.root, word, 0)

        # Nettoyer la racine si elle est vide
        if self.root and not self.root.is_end_of_word and self.root.left is None and self.root.middle is None and self.root.right is None:
            self.root = None



    def is_empty(self):
        """
        Vérifier si le Trie est complètement vide.
        """
        return self.root is None




    def recherche(self, word):
        """Rechercher si un mot existe"""
        return self._recherche(self.root, word, 0)

    def _recherche(self, node, word, index):
        if node is None:
            return False
        char = word[index]
        self.operation_count["search_comparisons"] += 1  
        if char < node.char:
            return self._recherche(node.left, word, index)
        elif char > node.char:
            return self._recherche(node.right, word, index)
        else:
            if index + 1 == len(word):
                return node.is_end_of_word
            return self._recherche(node.middle, word, index + 1)
        
    def comptageMots(self, node):
        """Compter le nombre de mots dans le Trie"""
        if node is None:
            return 0
        count = 1 if node.is_end_of_word else 0
        count += self.comptageMots(node.left)
        count += self.comptageMots(node.middle)
        count += self.comptageMots(node.right)
        return count

    # 列出所有单词
    def liste_mots(self):
        """Lister tous les mots dans le Trie"""
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
        Compter le nombre de pointeurs NULL dans le Trie hybride
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
        """Calculer la hauteur de l'arbre"""
        return self._hauteur(self.root)

    def _hauteur(self, node):
        if node is None:
            return 0
        return 1 + max(self._hauteur(node.left), self._hauteur(node.middle), self._hauteur(node.right))

    # 平均深度
    def profondeur_moyenne(self):
        """Calculer la profondeur moyenne des feuilles dans l'arbre"""
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
        """Compter le nombre de mots commençant par un préfixe donné"""
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
                return self.comptageMots(node.middle)
            return self._prefixe(node.middle, prefix, index + 1)

    

    # 保存和加载功能
    def to_json(self, file_path):
        """Sauvegarder le Trie sous forme de fichier JSON"""
        with open(file_path, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    def to_dict(self):
        """Convertir le Trie en format dictionnaire"""
        return self.root.to_dict() if self.root else {}
    
    @classmethod
    def from_dict(cls, data):
        """
        Charger un Trie à partir d’un dictionnaire.
        Si le dictionnaire est vide ({}), retourner un Trie vide.
        """
        if not data or data == {}:  # 处理空字典
            return cls()
        trie = cls()
        trie.root = HybridTrieNode.from_dict(data)
        return trie


    @classmethod
    def from_json(cls, file_path):
        """Charger un Trie depuis un fichier JSON"""
        with open(file_path, "r") as f:
            data = json.load(f)
        trie = cls()
        trie.root = HybridTrieNode.from_dict(data)
        return trie
    
    def is_unbalanced(self, depth_threshold=3, balance_threshold=2):
        """Vérifier si l'arbre est déséquilibré"""
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
        """Rééquilibrer l'arbre"""
        words = self.liste_mots()
        words = sorted(set(words))  # 确保去重并排序
        self.root = self._build_balanced_tree(words, 0, len(words) - 1)

    def _build_balanced_tree(self, words, start, end):
        """Construire un arbre équilibré"""
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
        """Construire une sous-arbre en chaîne à partir d'un mot"""
        if not word:
            return None
        root = HybridTrieNode(word[0])
        root.is_end_of_word = len(word) == 1
        root.middle = self._build_tree_from_word(word[1:])
        return root

    def insert_with_balance(self, word, depth_threshold=3, balance_threshold=2):
        """Insérer un mot et vérifier si un rééquilibrage est nécessaire"""
        if word not in self.liste_mots():  # Éviter les insertions répétées
            self.insert(word)
        if self.is_unbalanced(depth_threshold, balance_threshold):
            self.rebalance()





if __name__ == "__main__":
    # Exemple de phrase
    sentence = """
    A quel genial professeur de dactylographie sommes nous redevables de la superbe phrase ci-dessous,
    un modele du genre, que toute dactylo connait par coeur puisque elle fait appel a chacune des touches
    du clavier de la machine a ecrire ?
    """

    # Nettoyer et normaliser les entrées
    words = re.findall(r'\b[a-z]+\b', sentence.lower())  # 提取 ASCII 范围内的单词

    # Construire le Trie hybride
    trie = HybridTrie()
    for word in words:
        trie.insert(word)

    # Créer le dossier de résultats
    result_folder = "result"
    os.makedirs(result_folder, exist_ok=True)

    # Sauvegarder sous forme de fichier JSON
    json_file_path = os.path.join(result_folder, "exemple_base.json")
    trie.to_json(json_file_path)
    print(f"Le Trie hybride a été sauvegardé avec succès sous '{json_file_path}'")




