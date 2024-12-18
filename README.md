# Trie Comparison Project

This project implements and compares **Patricia Trie** and **Hybrid Trie** structures to manage and analyze word sets from Shakespearean texts.
Our git：https://github.com/Mengxiao-LI/projet_algo.git
# Requirements

- **Python 3.9+**
- Required Modules:
  - `matplotlib`
  - Standard libraries (`os`, `json`, `time`, `sys`)

- Install modules:
pip install matplotlib


## Directory Structure

```plaintext
project/
├── compare/                     # Scripts and results for comparing Patricia and Hybrid Tries
│   ├── Shakespeare/             # Input files for testing (Shakespeare's texts)
│   ├── result/                  # Test output results for Hybrid Trie (JSON)
│   ├── result_Patricia/         # Test output results for Patricia Trie (JSON)
│   ├── result_img/              # Visualized comparison results (PNG files)
│   ├── test/                    # Input files for insertion tests
│   │   └── word.txt             # Test file for inserting shuffled words
│   ├── compare_Hybrid.py        # Runs Hybrid Trie methods and saves results in JSON format
│   ├── compare_Patricia.py      # Runs Patricia Trie methods and saves results in JSON format
│   ├── compare_img.py           # Generates comparison charts for Patricia and Hybrid Tries
│   ├── complexite_hybrid.py     # Validates Hybrid Trie complexity and generates visual charts
│   └── complexite_patricia.py   # Validates Patricia Trie complexity and generates visual charts
│
├── Patricia-Tries/              # Patricia Trie implementation and tests
│   ├── result/                  # Folder for output test results
│   ├── test/                    # Folder containing input files for testing
│   ├── patricia.py              # Implementation of Patricia Trie
│   ├── patricia_fusion.py       # Test script for merging two Patricia Tries
│   ├── patricia_inserer.py      # Test script for insertion operations in Patricia Trie
│   ├── patricia_listeMots.py    # Test script for listing all words in Patricia Trie
│   ├── patricia_prefixe.py      # Test script for prefix matching in Patricia Trie
│   ├── patricia_profondeurMoyenne.py  # Test script for calculating average depth in Patricia Trie
│   └── patricia_suppression.py  # Test script for word deletion in Patricia Trie
│
├── Hybrid_trie/                 # Hybrid Trie implementation and tests
│   ├── result/                  # Folder for output test results
│   ├── hybrid_trie.py           # Implementation of Hybrid Trie
│   ├── trie_fusion.py           # Test script for merging two Hybrid Tries
│   ├── trie_inserer.py          # Test script for insertion operations in Hybrid Trie
│   ├── trie_listeMots.py        # Test script for listing all words in Hybrid Trie
│   ├── trie_prefixe.py          # Test script for prefix matching in Hybrid Trie
│   ├── trie_profondeurMoyenne.py  # Test script for calculating average depth in Hybrid Trie
│   └── trie_suppression.py      # Test script for word deletion in Hybrid Trie
│
├── script.sh                    # Bash script to run all tests for Patricia and Hybrid Tries

└── README.md                    # Project documentation
```


## Use Bash Script

./script.sh <command> <x> <file>

- **Commands**:

- `inserer`, `suppression`, `fusion`, `listeMots`, `profondeurMoyenne`, `prefixe`.

- **Example**:
```bash
./script.sh inserer 0 Patricia-Tries/test/word.txt
 ./script.sh suppression 0 Patricia-Tries/test/words_to_delete.txt
 ./script.sh fusionPat Patricia-Tries/test/tree1.json Patricia-Tries/test/tree2.json
./script.sh listeMots 0 Patricia-Tries/result/pat.json
 ./script.sh profondeurMoyenne 0 Patricia-Tries/result/pat.json
 ./script.sh prefixe 0 Patricia-Tries/result/pat.json c

./script.sh inserer 1 Hybrid_trie/words.txt
./script.sh suppression 1 Hybrid_trie/result/words_to_delete.txt
./script.sh listeMots 1 Hybrid_trie/result/trie.json
./script.sh profondeurMoyenne 1 Hybrid_trie/result/annexes.json
./script.sh prefixe 1 Hybrid_trie/result/annexes.json ca
  ```




