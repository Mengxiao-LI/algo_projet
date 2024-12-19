import json


class PatriciaTrieNode:
    def __init__(self, label=""):
        self.label = label
        self.children = {} #dictionnaire


class PatriciaTrie:
    end_marker = chr(0x00)  # 结束标记符

    def __init__(self):
        self.root = PatriciaTrieNode()
        #les cpt
        self.operation_count = {
            "insert_comparisons": 0,
            "search_comparisons": 0,
            "delete_comparisons": 0
        }

    def inserer(self, mot):
        mot += self.end_marker
        node = self.root

        while mot:

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
                #self.operation_count["insert_comparisons"] += len(prefix)

                if prefix == child.label:
                    # Correspondance parfaite, passer au nœud suivant.
                    node = child
                    mot = mot[len(prefix):]
                else:
                    # Correspondance partielle, diviser le nœud.
                    rest = child.label[len(prefix):]
                    new_node = PatriciaTrieNode(prefix)
                    new_node.children[rest[0]] = child
                    child.label = rest
                    node.children[prefix[0]] = new_node
                    node = new_node
                    mot = mot[len(prefix):]
            else:
                # Aucun préfixe commun, insérer directement.
                new_node = PatriciaTrieNode(mot)
                node.children[mot[0]] = new_node
                return

    #les fonctions auxiliaires
    def to_dict(self, node=None):
        """Convertir le Patricia-Trie en forme de dictionnaire"""
        if node is None:
            node = self.root


        result = {
            "label": node.label.rstrip(self.end_marker),
            "is_end_of_word": False
        }
        if node.label.endswith(self.end_marker):
            result["is_end_of_word"] = True
        elif self.end_marker in node.children:
            result["is_end_of_word"] = True


        filtered_children = {
            key: self.to_dict(child)
            for key, child in sorted(node.children.items())
            if key != self.end_marker
        }
        if filtered_children:
            result["children"] = filtered_children
        else:
            result["children"] = {}

        return result

    def display_as_json(self):
        """print trie en json """
        trie_dict = self.to_dict()
        print(json.dumps(trie_dict, indent=4))


# def find_mots_prefix(str1, str2):
#     min_len = min(len(str1), len(str2))
#     for i in range(min_len):
#         if str1[i] != str2[i]:
#             return str1[:i]
#     return str1[:min_len]
def find_mots_prefix(str1, str2, counter_dict=None, counter_key=None):
    """Trouver le préfixe de deux mots"""
    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        # si il y a cpt
        if counter_dict is not None and counter_key is not None:
            counter_dict[counter_key] += 1

        if str1[i] != str2[i]:
            return str1[:i]

    return str1[:min_len]

def json_to_patricia_trie(data):
    """Construire un Patricia-Trie à partir de données JSON"""

    def _dict_to_node(node_data):
        """Convertir récursivement les données JSON en nœuds de Patricia-Trie"""
        node = PatriciaTrieNode(node_data["label"])

        for key, child_data in node_data.get("children", {}).items():
            node.children[key] = _dict_to_node(child_data)

        if node_data.get("is_end_of_word", False):
            if node.children:
                # Si le nœud actuel a d'autres sous-nœuds, stocker le marqueur de fin sous forme de sous-nœuds
                if PatriciaTrie.end_marker not in node.children:
                    end_marker_node = PatriciaTrieNode(PatriciaTrie.end_marker)
                    node.children[PatriciaTrie.end_marker] = end_marker_node
            else:
                # S'il n'y a pas de sous-nœuds, ajouter directement le marqueur de fin dans le label
                node.label += PatriciaTrie.end_marker

        return node

    trie = PatriciaTrie()
    trie.root = _dict_to_node(data)
    return trie

#Question2
def recherche(arbre, m):
    """une fonction de recherche d’un mot dans un dictionnaire"""
    m += arbre.end_marker
    node = arbre.root
    while m:

        arbre.operation_count["search_comparisons"] += 1
        if m[0] not in node.children:
            return False

        child = node.children[m[0]]
        prefix = find_mots_prefix(
            m,
            child.label,
            counter_dict=arbre.operation_count,
            counter_key="search_comparisons"
        )

        if len(prefix) != len(child.label):
            return False

        node = child
        m = m[len(child.label):]

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
    """Extraire tous les mots du Patricia-Trie et retourner une liste triée"""
    words = []

    def _aux(node, current_word):
        if node.label.endswith(arbre.end_marker):
            words.append(current_word + node.label.rstrip(arbre.end_marker))

        for key, child in sorted(node.children.items()):
            _aux(child, current_word + node.label)


    _aux(arbre.root, "")
    return words

def comptage_nil(arbre):
    def _count_nil(node):
        if not node.children:
            return 1
        return sum(_count_nil(child) for child in node.children.values())

    return _count_nil(arbre.root)

def comptage_nil_exclude_endmarker(arbre):
    """Calculer le nombre de pointeurs nuls correspondant aux marqueurs non finaux dans le Patricia-Trie"""
    def _count_nil1(node):
        if not node.children:
            return 1

        return sum(_count_nil1(child) for key, child in node.children.items() if key != arbre.end_marker)
    return _count_nil1(arbre.root)


def hauteur(arbre):
    """Calculer la hauteur de l'arbre du Patricia-Trie"""

    def _height(node):
        if not node.children:
            return 0
        return 1 + max(_height(child) for child in node.children.values())

    return _height(arbre.root)


def profondeurMoyenne(arbre):
    """Calculer la profondeur moyenne """

    def _aux(node, depth):
        if not node.children:
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
        return 0
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
        """Fusionner les nœuds"""
        if node is arbre.root:
            return
        if len(node.children) == 1 and not node.label.endswith(arbre.end_marker):
            only_child_key, only_child = list(node.children.items())[0]
            node.label += only_child.label
            node.children = only_child.children

    def _delete(node, m):
        if not m:
            if arbre.end_marker in node.children:
                del node.children[arbre.end_marker]
            if not node.children:
                return None
            _merge_if_needed(node)
            return node

        t = m[0]
        arbre.operation_count["delete_comparisons"] += 1
        if t not in node.children:
            return node

        child = node.children[t]
        #prefix = find_mots_prefix(child.label, m)
        prefix = find_mots_prefix(
            child.label,
            m,
            counter_dict=arbre.operation_count,
            counter_key="delete_comparisons"
        )

        if prefix == child.label and len(prefix) == len(m):  # le nœud correspondant complete
            # D'abord, essayer de supprimer le marqueur de fin des sous-nœuds
            if arbre.end_marker in child.children:
                del child.children[arbre.end_marker]
            # Si les sous-nœuds ne contiennent pas de marqueur de fin, mais que le label contient le marqueur de fin, alors le retirer du label
            elif child.label.endswith(arbre.end_marker):
                child.label = child.label[:-1]

            # Si, après suppression, ce nœud ne possède plus de sous-nœuds et ne représente pas un mot (n'a plus de marqueur de fin)
            if not child.children and not child.label.endswith(arbre.end_marker):
                del node.children[t]
                if not node.children:
                    return None

            _merge_if_needed(child)
            return node

        if prefix:
            result = _delete(child, m[len(prefix):])
            if result is None:
                del node.children[t]
                if not node.children:
                    return None

        _merge_if_needed(node)
        return node

    arbre.root = _delete(arbre.root, mot)or PatriciaTrieNode()
    return arbre

def fusion(a, b):
    """fusion deux Patricia-Tries """
    def _aux(node_a, node_b):
        for key_b, child_b in node_b.children.items():
            if key_b in node_a.children:  # si a meme cle
                child_a = node_a.children[key_b]
                prefix = find_mots_prefix(child_a.label, child_b.label)

                if prefix == child_a.label and prefix == child_b.label:
                    _aux(child_a, child_b)
                elif prefix:
                    rest_a = child_a.label[len(prefix):]
                    rest_b = child_b.label[len(prefix):]

                    new_a = PatriciaTrieNode(rest_a)
                    new_a.children = child_a.children
                    new_b = PatriciaTrieNode(rest_b)
                    new_b.children = child_b.children

                    # mise a jour de A
                    node_a.children[key_b] = PatriciaTrieNode(prefix)
                    node_a.children[key_b].children = {}

                    # fusion newA et B
                    merged_child = _aux(new_a, new_b)
                    if merged_child:
                        node_a.children[key_b].children[key_b] = merged_child
                else:
                    # impossible
                    raise ValueError("Invalid state: overlapping keys with no common prefix")
            else:
                node_a.children[key_b] = child_b

        return node_a

    _aux(a.root, b.root)
    return a


if __name__ == "__main__":
    # test
    trie = PatriciaTrie()
    words = ["cat", "car", "cart", "bat","batt", "dog"]
    for word in words:
        trie.inserer(word)

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
    # Découper une phrase en mots
    import re
    words = re.findall(r'\b\w+\b|[^\w\s]', sentence)

    print(words)  # ['A', 'quel', 'genial', 'professeur', 'de', 'dactylographie', ',', 'sommes', '-', 'nous', ...]

    trie1 = PatriciaTrie()
    for word in words:
        trie1.inserer(word)

    print("phrase")
    print(liste_mots(trie1))
    print("there is "+str(comptage_mots(trie1))+" mots in the arbre1")
    print("nb Nil in trie " + str(comptage_nil(trie1)))
    print("nb Nil in trie no endmarker "+str(comptage_nil_exclude_endmarker(trie1)))


    def mots_with_end_marker_as_key(trie):
        """Les nœuds dans l'arbre où la clé est le marqueur de fin (end_marker)"""

        result = []

        def _dfs(node, path):
            current_word = "".join(path + [node.label.rstrip(trie.end_marker)])

            if trie.end_marker in node.children:
                child = node.children[trie.end_marker]
                if not child.children:
                    result.append(current_word)

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

    # test fusion
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
