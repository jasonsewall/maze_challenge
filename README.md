Maze Solver
===========
Jason Sewall
jasonsewall@gmail.com
January 2018

## Quick start

    $ python maze_viewer.py <n> <m> [seed]

(You may need to specify `python3` in some systems)

Create and view a n x m maze, optionally randomly seeded with [seed]. Use arrow keys to move icon.

    $ python bozo_walker.py <n> <m> [seed]

Create and view a n x m maze, optionally randomly seeded with [seed]. bozo walker will work very hard to find a (long, long) path to the solution. Not guaranteed to terminate! (But probably will).

n x m should probbly be < 200 each. It gets very hard to see things currently for large values, and the bozo walker is unlikely to terminate in a reasonable amount of time for n, m > 40

## Introduction

This is simple maze creation, viewing, and solving testbed written in Python 3. The only external dependency is on Pyglet.

### License

This is licensed with the permissive Apache License 2.0. See the LICENSE-2.0 file in the root of the distrubtion for details.

## Installation

In Windows, I recommend [Anaconda][https://www.anaconda.com/download/#windows].

Now, for Anaconda in Windows or in Linux assuming you have Python 3 properly installed:

    $ pip3 install pyglet

## Overview

There are 3 source files in this distribution:

- `maze.py` provides code to build and represent a rectilinar maze with one start and muliple ends, as well as basic `maze_walker` code.
- `mazeview.py` provides code to view mazes and to interatively nagivate them with the default walker. (see quick start, above)
- `bozo_walker.py` provides a subclass of the `maze_walker` that randomly walks until it has solved the maze.

## Challenge

Can you write a new `walker` subclass following the `bozo_walker` example that can solve the maze more reliably and quickly? Try it out! You'll certainly need to use more storage to do so, but it should be worth it.

## Other projects

- Make other types of mazes
  - Implement other maze generation techniques
  - Make mazes that have unreachable parts
  - Support non-rectilinear mazes
- Change from 'mazes' to 'general' navigation
  - Find shortest paths, rather than find solution quickly
- Improve maze viewer
  - Change the textures
  - Make the 'win condition' more visually interesting
  - Support 'camera movement' to allow for larger mazes to be displayed well.
  - 3D maze viewers!
