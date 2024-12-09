""" This solution is really slow! I wrote it without optimization, only 
thinking about correctness. Many things can be optimized like treating
the chunks of data and gaps as sorted ranges. The go version with this 
very same approach is much faster! """
import sys
import collections
import tqdm


class Disk:
    def __init__(self, data):
        self.blocks = [-1 for _ in range(sum(data))]
        self.file_blocks = collections.defaultdict(collections.deque)
        pos = 0
        for i in range(len(data)):
            if i % 2 == 0:
                self.insert_file(i // 2, pos, data[i])
                pos += data[i]
            else:
                pos += data[i]

    def insert_file(self, idx, pos, size):
        for i in range(size):
            self.blocks[pos + i] = idx
            self.file_blocks[idx].append(pos + i)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "".join(str(x) if x >= 0 else "." for x in self.blocks)

    def leftmost_gap(self, size=1):
        c = 0
        ci = None
        for i in range(len(self.blocks)):
            if self.blocks[i] == -1:
                if ci is None:
                    ci = i
                c += 1
                if c == size:
                    return ci
            else:
                c = 0
                ci = None
        return None

    def move_left(self, idx, pos, count=1):
        if pos > self.file_blocks[idx][-1]:
            return
        for i in range(count):
            oidx = self.file_blocks[idx].pop()
            self.blocks[oidx] = -1
            self.blocks[pos + i] = idx
            self.file_blocks[idx].appendleft(pos + i)

    def rev_files(self):
        idxs = list(self.file_blocks.keys())
        idxs.sort(reverse=True)
        return [(idx, len(self.file_blocks[idx])) for idx in idxs]

    def checksum(self):
        return sum([i * v for i, v in enumerate(self.blocks) if v >= 0])


def sol1(data):
    D = Disk(data)
    for idx, size in tqdm.tqdm(D.rev_files()):
        for _ in range(size):
            g = D.leftmost_gap()
            if g is None:
                continue
            D.move_left(idx, g)
    return D.checksum()


def sol2(data):
    D = Disk(data)
    for idx, size in tqdm.tqdm(D.rev_files()):
        g = D.leftmost_gap(size)
        if g is None:
            continue
        D.move_left(idx, g, size)
    return D.checksum()


if __name__ == "__main__":
    data = [int(x) for x in sys.stdin.readline().strip()]
    print(sol1(data))
    print(sol2(data))
