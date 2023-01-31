from collections import deque
from math import inf

# Очень большое число, которым является расстояние
# до каждой точки из стартовой точки по умолчанию
INF = inf

# Двумерный кортеж, в котором в каждом отдельном кортеже
# хранятся координаты клеток-соседей текущей клетки
# относительно самой текущей клетки
DELTA = ((0, -1), (0, 1), (1, 0), (-1, 0),
         (1, 1), (1, -1), (-1, 1), (-1, -1))


# Алгоритм для нахождения кратчайшего пути
# Алгоритм ищет путь до каждой точки вокруг стартовой точки
# до того момента пока не найдет конечную точку
# После того, как алгоритм находит конечную точку он
# превращает проложенный до нее путь в план движения и
# возвращает его обратно Программе
def Wave_algorythm(field, s, f):
    weight = len(field)
    height = len(field[0])
    distance = [[INF] * height for _ in range(weight)]
    path = [[None] * height for _ in range(weight)]
    used = [[False] * height for _ in range(weight)]
    queue = deque()

    distance[s[0]][s[1]] = 0
    used[s[0]][s[1]] = True
    queue.append(s)
    while len(queue):
        x, y = queue.popleft()
        for dx, dy in DELTA:
            nx, ny = x + dx, y + dy
            if 0 < nx < weight and 0 < ny < height \
                    and not used[nx][ny] and field[nx][ny]:
                distance[nx][ny] = distance[x][y] + 1
                path[nx][ny] = (x, y)
                used[nx][ny] = True
                queue.append((nx, ny))
        if used[f[0]][f[1]]:
            break
    cur = f
    way = []
    while 1:
        next = path[cur[0]][cur[1]]
        if next == None:
            break
        way.append((cur[0] - next[0], cur[1] - next[1]))
        cur = next
    way.reverse()

    return way
