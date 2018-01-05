from maze import rect_maze, maze_walker
from random import randint
import sys
import pyglet
from mazeview import mazeview

class bozo_walker(maze_walker):
    def __init__(self, maze):
        super(bozo_walker, self).__init__(maze)
    def solve(self):
        while not self.solved():
            dr = 'nesw'[randint(0, 3)]
            self.move(dr)
            if len(self.path) > 0 and len(self.path) % 10000 == 0:
                print("%d path steps so far..." % len(self.path))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Need 2 arguments!")
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    if len(sys.argv) == 4:
        seed = int(sys.argv[3])
        random.seed(seed)
    mz = rect_maze(n, m)
    mz.dfs_maze(0,0)
    mz.ends.append([n-1,m-1])

    walker = bozo_walker(mz)
    walker.solve()
    print("Took %d steps" % len(walker.path))
    mazeviewer = mazeview(mz)
    mazeviewer.walker = walker

    pyglet.app.run()
