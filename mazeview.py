import pyglet
from pyglet.gl import *
from maze import rect_maze, maze_walker

size_x = 5
size_y = 5

mz = rect_maze(size_x, size_y)
mz.dfs_maze(0,0)

mz.ends.append([size_x-1,size_y-1])

config = pyglet.gl.Config(alpha_size=8)
window = pyglet.window.Window(config=config,resizable=True,visible=False,caption="The Maze!")

(verts,lines) = mz.get_lines()

vl = pyglet.graphics.vertex_list_indexed(int(len(verts)/2), lines, ('v2f', tuple(verts)))

start = pyglet.image.load("start.png")
start.anchor_x = start.width//2
start.anchor_y = start.height//2

stop = pyglet.image.load("stop.png")
stop.anchor_x = stop.width//2
stop.anchor_y = stop.height//2

LA = pyglet.image.load("LA.png")
LA.anchor_x = LA.width//2
LA.anchor_y = LA.height//2

walker = maze_walker(mz)

@window.event
def on_key_release(symbol, modifiers):
    if walker.solved():
        return
    if symbol == pyglet.window.key.LEFT:
        walker.move('w')
    if symbol == pyglet.window.key.RIGHT:
        walker.move('e')
    if symbol == pyglet.window.key.UP:
        walker.move('s')
    if symbol == pyglet.window.key.DOWN:
        walker.move('n')

@window.event
def on_resize(width, height):
    pyglet.gl.glViewport(0,width,0,height)

def lerp(t, s, e):
    return t*(e-s) + s

@window.event
def on_draw():
    window.clear()
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, size_x, -1, size_y, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()
    glDisable(GL_TEXTURE_2D)
    glColor4f(0.0, 0.0, 0.0, 1.0)
    vl.draw(GL_LINES)

    if len(walker.path) > 1:
        cstart = [1.0, 1.0, 1.0]
        cend = [0.0, 0.0, 1.0]
        z = [walker.path[0][0],walker.path[1][0]]
        c = []
        c += cstart
        num = 0
        for i,p in enumerate(walker.path):
            z += [p[0],p[1]]
            t = i/(len(walker.path)-1)
            c += [ lerp(t, s, e) for (s,e) in zip(cstart,cend) ]
            num += 1
        z += walker.path[-1]
        c += cend
        wp = pyglet.graphics.vertex_list(int(len(z)/2), ('v2f', tuple(z)), ('c3f', tuple(c)))
        glColor4f(0.2, 0.2, 0.7, 1.0)
        wp.draw(GL_LINE_STRIP)

    glPushMatrix()
    glTranslatef(mz.start[0],mz.start[1],0.0)
    glScalef(1.0/start.width, 1.0/start.height, 1.0)
    glColor3f(1.0, 1.0, 1.0)
    start.blit(0,0,0)
    glPopMatrix()

    for e in mz.ends:
        glPushMatrix()
        glTranslatef(e[0],e[1], 0.0)
        glScalef(1.0/stop.width, 1.0/stop.height, 1.0)
        glColor3f(1.0, 1.0, 1.0)
        stop.blit(0,0,0)
        glPopMatrix()

    glPushMatrix()
    glTranslatef(walker.pos[0],walker.pos[1],0)
    glScalef(1.0/LA.width, 1.0/LA.height, 1.0)
    if not walker.solved():
        glRotatef(0.0,0.0,0.0,1.0)
    else:
        glRotatef(180,0.0,0.0,1.0)
    LA.blit(0,0,0)
    glPopMatrix()

window.set_visible()
window.activate()

pyglet.app.run()
