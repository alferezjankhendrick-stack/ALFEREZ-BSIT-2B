import sys
from collections import deque

LAST_NAME = "Alferez"   # <-- CHANGE THIS to your last name



class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def build_tree(name):

    letters = [c.upper() for c in name if c.isalpha()]
    root = None
    for ch in letters:
        if root is None:
            root = Node(ch)
            continue
        cur = root
        while True:
            if ch == cur.key:
                break  # duplicate letter, skip
            side = "left" if ch < cur.key else "right"
            nxt = getattr(cur, side)
            if nxt is None:
                setattr(cur, side, Node(ch))
                break
            cur = nxt
    return root


def print_tree(node, prefix="", is_left=None):

    if node is None:
        return
    label = "ROOT" if is_left is None else ("L" if is_left else "R")
    print(f"{prefix}[{label}] {node.key}")
    print_tree(node.left, prefix + "    ", True)
    print_tree(node.right, prefix + "    ", False)



def tree_bfs(root):
    result, queue = [], deque([root] if root else [])
    while queue:
        node = queue.popleft()
        result.append(node.key)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result



def preorder(node, out):    # Root, Left, Right
    if node:
        out.append(node.key)
        preorder(node.left, out)
        preorder(node.right, out)
    return out


def inorder(node, out):     # Left, Root, Right
    if node:
        inorder(node.left, out)
        out.append(node.key)
        inorder(node.right, out)
    return out


def postorder(node, out):   # Left, Right, Root
    if node:
        postorder(node.left, out)
        postorder(node.right, out)
        out.append(node.key)
    return out



def build_graph(name):

    letters = [c.upper() for c in name if c.isalpha()]
    adj, edges = {}, []
    for ch in letters:
        adj.setdefault(ch, set())
    for a, b in zip(letters, letters[1:]):
        if a != b and b not in adj[a]:
            adj[a].add(b)
            adj[b].add(a)
            edges.append((a, b))
    return {k: sorted(v) for k, v in adj.items()}, letters[0], edges



def graph_bfs(adj, start):
    visited, order, queue = {start}, [], deque([start])
    while queue:
        v = queue.popleft()
        order.append(v)
        for n in adj[v]:
            if n not in visited:
                visited.add(n)
                queue.append(n)
    return order



def graph_dfs(adj, v, visited=None, order=None):
    if visited is None:
        visited, order = set(), []
    visited.add(v)
    order.append(v)
    for n in adj[v]:
        if n not in visited:
            graph_dfs(adj, n, visited, order)
    return order


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else LAST_NAME
    if not any(c.isalpha() for c in name):
        sys.exit("Please enter a name with letters.")

    print(f"\nLast name: {name.upper()}")


    root = build_tree(name)
    print("\n===== BINARY TREE =====")
    print_tree(root)
    print("\nBFS (level-order):   ", " -> ".join(tree_bfs(root)))
    print("DFS Preorder  (N L R):", " -> ".join(preorder(root, [])))
    print("DFS Inorder   (L N R):", " -> ".join(inorder(root, [])))
    print("DFS Postorder (L R N):", " -> ".join(postorder(root, [])))


    adj, start, edges = build_graph(name)
    print("\n===== GRAPH =====")
    print("Vertices:", ", ".join(adj))
    print("Edges:   ", ", ".join(f"{a}-{b}" for a, b in edges) or "(none)")
    print("Adjacency list:")
    for v, ns in adj.items():
        print(f"  {v}: {', '.join(ns) or '-'}")
    print(f"\nStart vertex: {start}")
    print("BFS:", " -> ".join(graph_bfs(adj, start)))
    print("DFS:", " -> ".join(graph_dfs(adj, start)))


if __name__ == "__main__":
    main()