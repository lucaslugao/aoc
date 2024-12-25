import sys
from collections import deque


def read_map():
    grid = [list(line.strip("\n")) for line in sys.stdin]
    return grid


def neighbors(x, y, n, m):
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < m:
            yield nx, ny


def bfs_no_cheat(grid, start, end):
    n, m = len(grid), len(grid[0])
    dist = [[-1] * m for _ in range(n)]
    sx, sy = start
    dist[sx][sy] = 0
    q = deque([(sx, sy)])
    while q:
        x, y = q.popleft()
        if (x, y) == end:
            return dist
        for nx, ny in neighbors(x, y, n, m):
            if dist[nx][ny] == -1 and grid[nx][ny] != "#":
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    return dist


def bfs_from_end(grid, end):
    n, m = len(grid), len(grid[0])
    dist = [[-1] * m for _ in range(n)]
    ex, ey = end
    dist[ex][ey] = 0
    q = deque([(ex, ey)])
    while q:
        x, y = q.popleft()
        for nx, ny in neighbors(x, y, n, m):
            if dist[nx][ny] == -1 and grid[nx][ny] != "#":
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    return dist


def find_positions(grid, char):
    n, m = len(grid), len(grid[0])
    for i in range(n):
        for j in range(m):
            if grid[i][j] == char:
                return (i, j)
    return None


def is_free_cell(c):
    return c in (".", "S", "E")


def compute_cheats(
    grid, dist_start, dist_end, base_time, max_cheat_length, save_threshold=100
):
    n, m = len(grid), len(grid[0])
    free_cells = [
        (i, j) for i in range(n) for j in range(m) if is_free_cell(grid[i][j])
    ]

    cheat_map = {}

    for sx, sy in free_cells:
        start_dist = dist_start[sx][sy]
        if start_dist == -1:
            continue

        dist_cheat_phase = [[-1] * m for _ in range(n)]
        dist_cheat_phase[sx][sy] = 0
        q = deque([(sx, sy)])

        reachable_ends = {}
        while q:
            x, y = q.popleft()
            d = dist_cheat_phase[x][y]
            if d < max_cheat_length:
                for nx, ny in neighbors(x, y, n, m):
                    if dist_cheat_phase[nx][ny] == -1:
                        dist_cheat_phase[nx][ny] = d + 1
                        q.append((nx, ny))
                        if is_free_cell(grid[nx][ny]) and (nx, ny) != (sx, sy):
                            old = reachable_ends.get((nx, ny), max_cheat_length + 1)
                            if d + 1 < old:
                                reachable_ends[(nx, ny)] = d + 1

        for (ex, ey), c_cost in reachable_ends.items():
            if dist_end[ex][ey] != -1:
                total_time_with_cheat = dist_start[sx][sy] + c_cost + dist_end[ex][ey]
                saving = base_time - total_time_with_cheat
                if saving >= save_threshold:
                    cheat_map.setdefault((sx, sy), {})[(ex, ey)] = c_cost

    count = 0
    for s_pos, ends in cheat_map.items():
        for e_pos, c_cost in ends.items():
            ex, ey = e_pos
            saving = base_time - (
                dist_start[s_pos[0]][s_pos[1]] + c_cost + dist_end[ex][ey]
            )
            if saving >= save_threshold:
                count += 1

    return count


if __name__ == "__main__":
    grid = read_map()

    start = find_positions(grid, "S")
    end = find_positions(grid, "E")

    dist_start = bfs_no_cheat(grid, start, end)
    base_time = dist_start[end[0]][end[1]]
    dist_end = bfs_from_end(grid, end)

    res1 = compute_cheats(
        grid, dist_start, dist_end, base_time, max_cheat_length=2, save_threshold=100
    )
    res2 = compute_cheats(
        grid, dist_start, dist_end, base_time, max_cheat_length=20, save_threshold=100
    )

    print(res1)
    print(res2)
