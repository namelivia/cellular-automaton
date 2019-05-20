#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
from random import randint
import sdl2.ext

class AutomatonGenerator(object):
    """Cellullar automaton generation tool"""
    @classmethod
    def run(cls):
        """Configuration, initialization and running the automaton in an endless loop"""
        parser = argparse.ArgumentParser()
        parser.add_argument('width', help='the width in tiles of the world', type=int)
        parser.add_argument('height', help='the height in tiles of the world', type=int)
        parser.add_argument('tile', help='the size of the tiles in pixels', type=int)
        parser.add_argument('outer', help='the status of the outer cells', type=int)
        args = parser.parse_args()
        sdl2.ext.init()
				#TODO: Screen resoultion will be dynamic
        window = sdl2.ext.Window('Cellullar Automaton', size=(800, 600))
        running = True
        window.show()
        while running:
            Automaton(window, args.width, args.height, args.tile, args.outer).run()
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    running = False
            window.refresh()

class Automaton(object):
    """Unidimensional square cellullar automaton"""
    def __init__(self, window, width, height, tile, outer):
        self.surface = window.get_surface()
        self.world = World(self.surface, width, tile, outer)
        self.height = height
        self.tile = tile
    def run(self):
        """Runs the automaton calculating and drawing it on the screen"""
        sdl2.ext.fill(self.surface, 0)
        for idx in range(0, self.height):
            self.world.step(idx)
            self.world.draw()

class World(object):
    """The world (row of squares) on the cellullar automaton"""
    INITIAL_STATUS = 0
    def __init__(self, surface, width, tile, outer):
        self.outer = outer
        self.cells = []
        self.surface = surface
        self.tile = tile
        for idx in range(0, width):
            self.cells.append(Cell(self.surface, self.INITIAL_STATUS, idx, 0, self.tile))
        #TODO: Initial configuration will be dynamic
        self.cells[width / 2] = Cell(self.surface, 1, width / 2, 0, self.tile)

    def step(self, index):
        """Executes a simulation step on the world"""
        new_cells = []
        for idx, val in enumerate(self.cells):
            left_status = self.cells[idx - 1].status if idx > 0 else self.outer
            right_status = self.cells[idx + 1].status if idx < len(self.cells) - 1 else self.outer
            new_cells.append(
                Cell(self.surface, val.step(left_status, right_status), idx, index, self.tile)
            )
        self.cells = new_cells

    def draw(self):
        """Draws the world on the window"""
        for _, val in enumerate(self.cells):
            val.draw()

class Cell(object):
    """A cell (square) on the cellullar automaton"""
    def __init__(self, surface, initial_status, index, y, tile):
        self.tile = tile
        self.surface = surface
        self.status = initial_status
        self.x_coord = index * self.tile
        self.y_coord = y * self.tile

    def step(self, left_status, right_status):
        """Executes a simulation step on the cell"""
        return self.get_new_status(str(left_status) + str(self.status) + str(right_status))

    def draw(self):
        """Draws a cell on the window"""
        white = sdl2.ext.Color(randint(0, 255), randint(0, 255), randint(0, 255))
        black = sdl2.ext.Color(0, 0, 0)
        color = white if self.status else black
        sdl2.ext.fill(self.surface, color, (self.x_coord, self.y_coord, self.tile, self.tile))

    @classmethod
    def get_new_status(cls, code):
        """Gets the new status for a cell"""
        #TODO: Rules will be dynamic
        my_dict = {
            '000' : 0,
            '001' : 1,
            '010' : 1,
            '011' : 1,
            '100' : 1,
            '101' : 0,
            '110' : 0,
            '111' : 0,
        }
        return my_dict[code]

if __name__ == '__main__':
    AutomatonGenerator().run()
