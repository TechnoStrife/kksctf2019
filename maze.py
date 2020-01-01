import socket
from math import inf
from typing import List, Optional, Set

from vector import Vector


def split_by_length(array, size):
    return [array[z:z + size] for z in range(0, len(array), size)]


class Vertex:
    def __init__(self, position, type_=None):
        self.pos = Vector(position)
        self.type = type_
        self.distance = inf
        self.neighbours: List[Vertex] = []
        self.shortest_path_from: Optional[Vertex] = None

    def __str__(self):
        return f'{self.pos} <{self.type}>'

    __repr__ = __str__


class Maze:
    def __init__(self, maze: List[List[str]]):
        assert all(len(x) == len(maze[0]) for x in maze)
        self.size = Vector(len(maze[0]), len(maze))
        self.start = None

        self.maze: List[List[Optional[Vertex]]] = [[None] * self.size.x for _ in range(self.size.y)]
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == '##':
                    continue
                self.maze[y][x] = Vertex(Vector(x, y), cell)

        for row in self.maze:
            for vertex in row:
                if vertex is None:
                    continue
                for neighbour in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    neighbour: Vector = vertex.pos + neighbour
                    neighbour: Optional[Vertex] = self.maze[neighbour.y][neighbour.x]
                    if neighbour is not None:
                        vertex.neighbours.append(neighbour)

    def vertices(self):
        return (vertex for row in self.maze for vertex in row if vertex is not None)

    def solve(self):
        start = self.maze[1][1]
        plans = self.paths_to_exit([start])
        paths = [self.calculate_plan_path(plan) for plan in plans]
        the_path = min(paths, key=lambda x: len(x))
        ans = ''
        for z in range(len(the_path) - 1):
            direction = the_path[z + 1].pos - the_path[z].pos
            if direction.x == 0:
                ans += 'd' if direction.y == 1 else 'u'
            else:
                ans += 'r' if direction.x == 1 else 'l'
        return ans

    def paths_to_exit(self, path: List[Vertex], keys=0) -> List[List[Vertex]]:
        routes = []
        # find all checkpoints available from the end of the path
        available = self.available_from(path[-1])
        # remove those we already visited
        available.difference_update(path)
        for node in available:
            new_keys = keys
            if node.type == 'Om':
                new_keys += 1
            elif node.type == '{}':
                new_keys -= 1
            if new_keys < 0:
                continue  # this route has more doors than keys

            new_path = path + [node]
            if node.type == '<>':
                routes.append(new_path)
            else:
                subroutes = self.paths_to_exit(new_path, new_keys)
                routes.extend(subroutes)
        return routes

    def available_from(self, start: Vertex) -> Set[Vertex]:
        for vertex in self.vertices():
            vertex.distance = inf

        available = set()
        queue: List[Vertex] = [start]
        start.distance = 0

        while queue:
            current = queue.pop(0)
            if current.type in ['<>', 'Om', '{}']:
                available.add(current)
            if current.type == '{}' and current is not start:
                continue
            for neighbour in current.neighbours:
                if neighbour.distance == inf:
                    neighbour.distance = 0
                    queue.append(neighbour)
        available.discard(start)
        return available

    def calculate_plan_path(self, plan) -> List[Vertex]:
        paths = []
        for z in range(len(plan) - 1):
            paths.append(self.bfs(plan[z], plan[z + 1]))
        for path in paths[1:]:
            path.pop(0)
        return sum(paths, [])

    def bfs(self, source: Vertex, dest: Vertex) -> List[Vertex]:
        vertices = [source]
        for vertex in self.vertices():
            vertex.distance = inf
            vertex.shortest_path_from = None
        source.distance = 0

        while vertices:
            vertex = vertices.pop(0)
            if vertex is dest:
                break

            for neighbour in vertex.neighbours:
                if neighbour.type == '{}' and neighbour is not dest:
                    continue
                if neighbour.distance == inf:
                    neighbour.distance = vertex.distance + 1
                    neighbour.shortest_path_from = vertex
                    vertices.append(neighbour)

        path = []
        current_vertex = dest
        while current_vertex.shortest_path_from is not None:
            path.append(current_vertex)
            current_vertex = current_vertex.shortest_path_from
        if path:
            path.append(current_vertex)
        return path[::-1]


sock = socket.socket()
sock.connect(('tasks.open.kksctf.ru', 31397))
sock.recv(100000)  # skip initial '\n\n'

while True:
    s = sock.recv(100000).decode()
    if s == '':
        break
    print(s)
    if s.startswith('Gratz'):
        break

    maze = s.split('\n')
    maze = [split_by_length(x, 2) for x in maze]
    maze = Maze(maze)
    ans = maze.solve() + '\r\n'
    print(ans)
    sock.send(ans.encode())

sock.close()
