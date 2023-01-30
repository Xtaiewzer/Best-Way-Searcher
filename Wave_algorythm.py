from collections import deque
from math import inf

# Невозможно большая длина пути по умолчанию
INF = inf
# Разница в координатах текущей клетки и клетки-соседа
DELTA = ((0, -1), (0, 1), (1, 0), (-1, 0),
         (1, 1), (1, -1), (-1, 1), (-1, -1))

# Алгоритм для нахождения кратчайшего пути
# Алгоритм ищет путь до каждой точки вокруг стартовой точки
# до того момента пока не найдет конечную точку
# После того, как алгоритм находит конечную точку он
# превращает проложенный до нее путь в план движения и
# возвращает его обратно Программе
def Wave_algorythm(field, s, f):
    w = len(field)
    h = len(field[0])
    d = [[INF] * h for _ in range(w)]
    p = [[None] * h for _ in range(w)]
    used = [[False] * h for _ in range(w)]
    queue = deque()

    d[s[0]][s[1]] = 0
    used[s[0]][s[1]] = True
    queue.append(s)
    while len(queue):
        x, y = queue.popleft()
        for dx, dy in DELTA:
            nx, ny = x + dx, y + dy
            if 0 < nx < w and 0 < ny < h \
                    and not used[nx][ny] and field[nx][ny]:
                d[nx][ny] = d[x][y] + 1
                p[nx][ny] = (x, y)
                used[nx][ny] = True
                queue.append((nx, ny))
        if used[f[0]][f[1]]:
            break
    cur = f
    way = []
    while 1:

        next = p[cur[0]][cur[1]]
        if next == None:
            break
        way.append((cur[0] - next[0], cur[1] - next[1]))

        cur = next
    way.reverse()

    return way
