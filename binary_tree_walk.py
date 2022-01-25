"""
Прогрмма востонавливающая бинарное дерево ввиде класса из лог-файла walk_log.txt
"""
import itertools
import logging
import random
import re
from collections import deque
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)

    node_right = get_tree(max_depth - 1, level=level + 1)

    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    with open(path_to_log_file, 'r', encoding='utf-8') as file:
        for line in file:
            root = BinaryTreeNode(val=int(re.search(r'\d+', line).group()))
            break

    container = {}
    container[root.val] = root
    with open(path_to_log_file, 'r', encoding='utf-8') as file:
        for line in file:
            if 'INFO' in line:
                value = int(re.search(r'\d+', line).group())
                parent = container.pop(value)

            elif 'DEBUG' in line:
                value = int(re.findall(r'\d+', line)[1])
                nod = BinaryTreeNode(val=value)
                container[value] = nod
                if 'left' in line:
                    parent.left = nod
                elif 'right' in line:
                    parent.right = nod
    return root


if __name__ == "__main__":
    root = restore_tree('walk_log.txt')
    print(root)
