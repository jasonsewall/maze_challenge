# Copyright 2018 Jason Sewall (jasonsewall@gmai.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from numpy import ndarray
from collections import defaultdict
from random import randint

class rect_maze:
    """Represents a rectilinear maze. We use the labels 'n' 'e' 's' 'w' to identify cardinal directions."""
    def __init__(self, n, m):
        """Make a 2d n x m  'maze' with all walls in place"""
        self.n = n
        self.m = m
        self.wall_x = ndarray((self.n+1, self.m), dtype=int)
        self.wall_y = ndarray((self.n, self.m+1), dtype=int)
        self.wall_x[:,:] = 1
        self.wall_y[:,:] = 1
        self.start = None
        self.ends = []
    def dfs_maze(self, start_i, start_j):
        self.start = [start_i, start_j]
        """Starting at start_i, start_j, remove walls to create a maze"""
        visited = ndarray((self.n, self.m), dtype=int)
        visited[:,:] = 0
        visited[start_i, start_j] = 1
        visited_count = 1
        current_i, current_j = start_i, start_j
        trail = []
        trail.append((current_i, current_j))
        while visited_count < self.n*self.m:
            cand_neighbors = list(filter(lambda x: x[0] >= 0 and x[1] >= 0 and x[0] < self.n and x[1] < self.m and visited[x[0],x[1]] == 0,
                                    [(current_i+1, current_j), (current_i-1, current_j), (current_i, current_j+1), (current_i, current_j-1)]))
            if len(cand_neighbors) > 0:
                pick = cand_neighbors[randint(0, len(cand_neighbors)-1)]
                diff = (pick[0]-current_i, pick[1]-current_j)
                assert abs(diff[0]) + abs(diff[1]) == 1
                if diff[1] == 1: # south
                    self.wall_y[current_i, current_j+1] = 0
                elif diff[1] == -1: # north
                    self.wall_y[current_i, current_j] = 0
                elif diff[0] == 1: # east
                    self.wall_x[current_i+1, current_j] = 0
                elif diff[0] == -1: # west
                    self.wall_x[current_i, current_j] = 0
                trail.append(pick)
                visited[pick[0],pick[1]] = 1
                visited_count += 1
                (current_i, current_j) = pick
            else:
                if len(trail) > 0:
                    (current_i, current_j) = trail.pop()
    def wall_n(self, pos):
        """Returns exisitence of wall north of cell pos"""
        return self.wall_y[pos[0],pos[1]]
    def wall_s(self, pos):
        """Returns exisitence of wall south of cell pos"""
        return self.wall_y[pos[0],pos[1]+1]
    def wall_e(self, pos):
        """Returns exisitence of wall east of cell pos"""
        return self.wall_x[pos[0]+1,pos[1]]
    def wall_w(self, pos):
        """Returns exisitence of wall west of cell pos"""
        return self.wall_x[pos[0],pos[1]]
    def get_lines(self):
        """Produce vertices & indices to pass to batched rendering for OpenGL"""
        verts = []
        idx = 0
        lines = []
        for m in range(self.m+1):
            for n in range(self.n+1):
                verts += [n-0.5,m-0.5]
                if n > 0:
                    if self.wall_y[n-1,m]:
                        lines += [idx-1,idx]
                if m > 0:
                    if self.wall_x[n,m-1]:
                        lines += [idx-self.n-1,idx]
                idx += 1
        return (verts,lines)

class maze_walker:
    """A basic path-tracking class for traversing a maze"""
    def __init__(self, maze):
        """Set up reference to maze to be solved"""
        self.maze = maze
        self.pos = maze.start
        self.path = [self.pos]
    def solved(self):
        """Return true if we have reached one of the ends"""
        return self.pos in self.maze.ends
    def look(self, dr):
        """Check to see if there is a wall in this direction (one of 'n', 'e', 's', 'w')"""
        if dr in 'wnse':
            return getattr(self.maze, "wall_"+dr)(self.pos)
    def move(self, dr):
        """Try to move in specified direction, respecting walls."""
        if not self.look(dr):
            if dr == 'w':
                self.pos = [self.pos[0]-1, self.pos[1]]
            if dr == 'e':
                self.pos = [self.pos[0]+1, self.pos[1]]
            if dr == 'n':
                self.pos = [self.pos[0], self.pos[1]-1]
            if dr == 's':
                self.pos = [self.pos[0], self.pos[1]+1]
            self.path.append(self.pos)
        return self.pos
