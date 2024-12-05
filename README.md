# Trie Comparison Project

This project implements and compares the **Hybrid Trie** and **Patricia Trie** for encoding and managing word sets from Shakespearean texts.

```markdown
# Requirements

- **Python 3.9+**
- Required Modules:
  - `matplotlib`
  - Standard libraries (`os`, `json`, `time`, `sys`)

Install modules:
```bash
pip install matplotlib

# Directory Structure

```plaintext
project/
├── HybridTrie/           # Hybrid Trie implementation
├── PatriciaTrie/         # Placeholder for Patricia Trie
├── compare/              # Comparison scripts and input files
│   ├── Shakespeare/      # Input text files
│   ├── result/           # Output directory
│   └── compare.py        # Main comparison script
└── README.md


# How to Run

## Run Hybrid Trie Tests
```bash
python compare/compare.py


## Use Bash Script

./script.sh <command> <x> <file>

Commands:

inserer, suppression, fusion, listeMots, profondeurMoyenne, prefixe.

Example:
./script.sh inserer 1 compare/Shakespeare/hamlet.txt
./script.sh suppression 1 words_to_delete.txt
./script.sh fusion 1 trie1.json trie2.json
./script.sh listeMots 1 trie.json
./script.sh profondeurMoyenne 1 trie.json
./script.sh prefixe 1 trie.json pre



# Input/Output Format

- **Input**: Text files in `compare/Shakespeare/` with one word per line.
- **Output**: Results saved in `compare/result/` as JSON or PNG files.



