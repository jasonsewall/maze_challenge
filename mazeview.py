import pyglet
from pyglet.gl import *
import random
from maze import rect_maze, maze_walker
import sys

def lerp(t, s, e):
    return t*(e-s) + s

class mazeview(pyglet.window.Window):
    def __init__(self, maze):
        config = pyglet.gl.Config(alpha_size=8)
        super(mazeview, self).__init__(resizable=True,caption="The Maze! (%dx%d)" % (maze.n, maze.m))
        self.maze = maze
        (verts,lines) = maze.get_lines()
        self.vl = pyglet.graphics.vertex_list_indexed(int(len(verts)/2), lines, ('v2f', tuple(verts)))

        self.start = pyglet.image.load("start.png")
        self.start.anchor_x = self.start.width//2
        self.start.anchor_y = self.start.height//2
        self.stop = pyglet.image.load("stop.png")
        self.stop.anchor_x = self.stop.width//2
        self.stop.anchor_y = self.stop.height//2
        self.LA = pyglet.image.load("LA.png")
        self.LA.anchor_x = self.LA.width//2
        self.LA.anchor_y = self.LA.height//2

        self.walker = None
        self.label = pyglet.text.Label('Hello, world!')

    def on_key_release(self, symbol, modifiers):
        if self.walker == None or self.walker.solved():
            return
        if symbol == pyglet.window.key.LEFT:
            self.walker.move('w')
        if symbol == pyglet.window.key.RIGHT:
            self.walker.move('e')
        if symbol == pyglet.window.key.UP:
            self.walker.move('s')
        if symbol == pyglet.window.key.DOWN:
            self.walker.move('n')

    def on_draw(self):
        self.clear()
        self.label.draw()
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, self.maze.n, -1, self.maze.m, -1, 1)
        glMatrixMode(GL_MODELVIEW)

        glLoadIdentity()
        glDisable(GL_TEXTURE_2D)
        glColor4f(0.0, 0.0, 0.0, 1.0)
        self.vl.draw(GL_LINES)

        if self.walker != None and len(self.walker.path) > 1:
            cstart = [1.0, 1.0, 1.0]
            cend = [0.0, 0.0, 1.0]
            z = [self.walker.path[0][0],self.walker.path[1][0]]
            c = []
            c += cstart
            num = 0
            for i,p in enumerate(self.walker.path):
                z += [p[0],p[1]]
                t = i/(len(self.walker.path)-1)
                c += [ lerp(t, s, e) for (s,e) in zip(cstart,cend) ]
                num += 1
            z += self.walker.path[-1]
            c += cend
            wp = pyglet.graphics.vertex_list(int(len(z)/2), ('v2f', tuple(z)), ('c3f', tuple(c)))
            glColor4f(0.2, 0.2, 0.7, 1.0)
            wp.draw(GL_LINE_STRIP)

        glPushMatrix()
        glTranslatef(self.maze.start[0],self.maze.start[1],0.0)
        glScalef(1.0/self.start.width, 1.0/self.start.height, 1.0)
        glColor3f(1.0, 1.0, 1.0)
        self.start.blit(0,0,0)
        glPopMatrix()

        for e in self.maze.ends:
            glPushMatrix()
            glTranslatef(e[0],e[1], 0.0)
            glScalef(1.0/self.stop.width, 1.0/self.stop.height, 1.0)
            glColor3f(1.0, 1.0, 1.0)
            self.stop.blit(0,0,0)
            glPopMatrix()

        if self.walker != None:
            glPushMatrix()
            glTranslatef(self.walker.pos[0],self.walker.pos[1],0)
            glScalef(1.0/self.LA.width, 1.0/self.LA.height, 1.0)
            if not self.walker.solved():
                glRotatef(0.0,0.0,0.0,1.0)
            else:
                glRotatef(180,0.0,0.0,1.0)
            self.LA.blit(0,0,0)
            glPopMatrix()
        glFlush()

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

    mazeviewer = mazeview(mz)
    mazeviewer.walker = maze_walker(mz)

    pyglet.app.run()
