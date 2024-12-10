import sys
import dataclasses
import tqdm


@dataclasses.dataclass
class Node:
    pos: int
    idx: int
    size: int
    prev: "Node" = None
    next: "Node" = None

    def end(self):
        return self.pos + self.size

    def insert_after(self, node):
        if self.next is not None:
            self.next.prev = node
            node.next = self.next
        self.next = node
        self.next.prev = self
        return self.next

    def insert_before(self, node):
        if self.prev is not None:
            self.prev.next = node
            node.prev = self.prev
        self.prev = node
        self.prev.next = self
        return self.prev

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.prev = self.next = None


class Disk:
    def __init__(self, data):
        self.gap_head = None
        self.blocks = None
        self.blocks_tail = None
        self.index = {}
        pos = 0
        for i in range(len(data)):
            if i % 2 == 0:
                bnode = Node(pos, i // 2, data[i])
                self.index[i // 2] = bnode
                if self.blocks is None:
                    self.gap_head = bnode
                    self.blocks = bnode
                    self.blocks_tail = bnode
                else:
                    self.blocks_tail = self.blocks_tail.insert_after(bnode)
                pos += data[i]
            else:
                pos += data[i]

    def leftmost_gap(self, size=1):
        if self.gap_head is None or self.gap_head.next is None:
            return self.gap_head
        while (
            self.gap_head.next is not None
            and self.gap_head.end() == self.gap_head.next.pos
        ):
            self.gap_head = self.gap_head.next

        res = self.gap_head
        while res.next.pos - res.end() < size:
            res = res.next
            if res.next is None:
                return None
        return res

    def move_left(self, idx, node, count=1):
        idx_n = self.index[idx]
        if node.pos >= idx_n.end():
            return
        idx_n.size -= count
        if node.idx == idx:
            node.size += count
        else:
            node.insert_after(Node(node.end(), idx, count))

    def rev_files(self):
        idxs = list(self.index.keys())
        idxs.sort(reverse=True)
        return [(idx, self.index[idx].size) for idx in idxs]

    def __repr__(self):
        return str(self)

    def __str__(self):
        res = []
        node = self.blocks
        pos = 0
        while node is not None:
            res.extend(["."] * (node.pos - pos))
            res.extend([str(node.idx)] * node.size)
            pos = node.end()
            node = node.next
        return "".join(res)

    def checksum(self):
        check = 0
        node = self.blocks
        while node is not None:
            check += (((2 * node.pos + node.size - 1) * node.size) // 2) * node.idx
            node = node.next
        return check


def sol1(data):
    D = Disk(data)
    for idx, size in D.rev_files():
        for _ in range(size):
            g = D.leftmost_gap()
            if g is None:
                continue
            D.move_left(idx, g)
    return D.checksum()


def sol2(data):
    D = Disk(data)
    for idx, size in D.rev_files():
        g = D.leftmost_gap(size)
        if g is None:
            continue
        D.move_left(idx, g, size)
    return D.checksum()


if __name__ == "__main__":
    data = [int(x) for x in sys.stdin.readline().strip()]
    print(sol1(data))
    print(sol2(data))
