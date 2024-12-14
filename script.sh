#!/bin/bash

#./script.sh inserer 0 Patricia-Tries/test/word.txt
# ./script.sh suppression 0 Patricia-Tries/test/words_to_delete.txt
# ./script.sh fusionPat Patricia-Tries/test/tree1.json Patricia-Tries/test/tree2.json
#./script.sh listeMots 0 Patricia-Tries/result/pat.json
# ./script.sh profondeurMoyenne 0 Patricia-Tries/result/pat.json
# ./script.sh prefixe 0 Patricia-Tries/result/pat.json c


#./script.sh inserer 1 Hybrid_trie/words.txt
#./script.sh suppression 1 Hybrid_trie/result/words_to_delete.txt

#./script.sh fusion 1 tree1.json tree2.json
#./script.sh listeMots 1 trie.json
#./script.sh profondeurMoyenne 1 trie.json
#./script.sh prefixe 1 trie.json prefixe


# 检查参数数量是否正确
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <command> <x> <file> [additional_args...]"
    echo "Commands: inserer, suppression, fusion, listeMots, profondeurMoyenne, prefixe"
    exit 1
fi
command=$1  # 动作名称（如 inserer, suppression, fusion）
if [ "$command" != "fusionPat" ]; then

    # 读取参数

    x=$2        # 0 = Patricia 树，1 = 混合 Trie 树
    file=$3     # 输入文件或 JSON 文件
    shift 3     # 剩余参数作为附加参数传递给 Python 脚本

    # 检查 x 是否为 0 或 1
    if [ "$x" -ne 0 ] && [ "$x" -ne 1 ]; then
        echo "Error: x must be 0 or 1"
        exit 1
    fi

    # 确定 Python 脚本前缀
    if [ "$x" -eq 0 ]; then
        script_prefix="Patricia-Tries/patricia"
    else
        script_prefix="Hybrid_trie/trie"
    fi
else
    file1=$2  # 第一个 JSON 文件
    file2=$3  # 第二个 JSON 文件
    script_prefix="Patricia-Tries/patricia"  # fusion 默认针对 Patricia 树
fi

# 根据命令选择对应的 Python 脚本
case $command in
    inserer)
        echo "Running: python3 ${script_prefix}_inserer.py $x $file $@"
        python3 "${script_prefix}_inserer.py" "$x" "$file" "$@"
        ;;

    suppression)
        echo "Running: python3 ${script_prefix}_suppression.py $file $@"
        python3 "${script_prefix}_suppression.py" "$x" "$file" "$@"
        ;;
    fusionPat)
        echo "Running: python3 ${script_prefix}_fusion.py $file1 $file2"
        python3 "${script_prefix}_fusion.py" "$file1" "$file2"
        ;;
    listeMots)
        echo "Running: python3 ${script_prefix}_listeMots.py $file $@"
        python3 "${script_prefix}_listeMots.py" "$file" "$@"
        ;;
    profondeurMoyenne)
        echo "Running: python3 ${script_prefix}_profondeurMoyenne.py $file $@"
        python3 "${script_prefix}_profondeurMoyenne.py" "$file" "$@"
        ;;
    prefixe)
        if [ "$#" -lt 1 ]; then
            echo "Usage: $0 prefixe <x> <file.json> <prefix>"
            exit 1
        fi
        prefix=$1
        shift 1
        echo "Running: python3 ${script_prefix}_prefixe.py $file $prefix $@"
        python3 "${script_prefix}_prefixe.py" "$file" "$prefix" "$@"
        ;;
    *)
        echo "Error: Unknown command $command"
        echo "Commands: inserer, suppression, fusion, listeMots, profondeurMoyenne, prefixe"
        exit 1
        ;;
esac
