from collections import deque


def bfs(field, s, t):
    n = len(field)
    m = len(field[0])
    INF = 10 ** 9
    delta = ((0, -1), (0, 1), (1, 0), (-1, 0))
    d = [[INF] * m for _ in range(n)]
    p = [[None] * m for _ in range(n)]
    used = [[False] * m for _ in range(n)]
    queue = deque()

    d[s[0]][s[1]] = 0
    used[s[0]][s[1]] = True
    queue.append(s)
    while len(queue) != 0:
        x, y = queue.popleft()
        for dx, dy in delta:
            nx, ny = x + dx, y + dy
            if 0 < nx < n and 0 < ny < m \
                    and not used[nx][ny] and field[nx][ny] != '#':
                d[nx][ny] = d[x][y] + 1
                p[nx][ny] = (x, y)
                used[nx][ny] = True
                queue.append((nx, ny))
    print(d[t[0]][t[1]])
    cur = t
    path = []
    way = []
    while cur is not None:
        path.append(cur)
        cur = p[cur[0]][cur[1]]
    path.reverse()

    # Эта хуйня блять не работает
    # Тут короче должена получиться карта с путём а не эта хуйня
    # res = [[" "] * m for _ in range(n)]
    # for i in range(n):
    #     for j in range(m):
    #         pij = p[i - 1][j - 1]
    #         if pij != None:
    #             res[pij[0]][pij[1]] = "O"
    #         else:
    #             res[i - 1][j - 1] = field[i - 1][j - 1]
    # st = ''
    # for i in range(n):
    #     for j in range(m):
    #         st += res[i - 1][j - 1]
    # print(st)


if __name__ == "__main__":
    file = open("path.txt")
    filelines = file.readlines()
    n = len(filelines)
    m = len(filelines[0]) - 1
    s = None
    t = None

    for i in range(n):
        line = filelines[i]
        line = line.strip()
        sf = line.find('S')
        if sf != -1:
            s = (i, sf)
        tf = line.find('T')
        if tf != -1:
            t = (i, tf)

    st = ''
    for i in filelines:
        st += i
    print(st)
    print(s, t)
    bfs(filelines, s, t)
