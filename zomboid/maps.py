#!/usr/bin/env python
import os
from main import *
from vendor.pytmx import tmxloader
from progressbar import *


class Maps(object):

    def __init__(self, filename):
        self.tmxMap = tmxloader.load_pygame(os.path.join("media/Maps", filename), pixelalpha=True)
        self.num_tile_x = self.tmxMap.width
        self.tileWidth = self.tmxMap.tilewidth
        self.dW = self.tileWidth/2
        self.num_tile_y = self.tmxMap.height
        self.tileHeight = self.tmxMap.tileheight
        self.dH = self.tileHeight/2
        self.posList = {}
        self.tile_properties = {}

    def load(self):
        inc = 0
        progress = ProgressBar(maxval=self.num_tile_x*self.num_tile_y, widgets=[Percentage(), ' ', Bar(), ' ', ETA()])
        progress.start()
        for layer_index in range(len(self.tmxMap.layernames.keys())):
            self.posList[layer_index] = {}
            for x in range(self.num_tile_x):
                self.posList[layer_index][x] = {}
                self.tile_properties[layer_index][x] = {}
                for y in range(self.num_tile_y):
                    image = self.tmxMap.getTileImage(x, y, int(layer_index))
                    if image:
                        self.posList[layer_index][x][y] = (((x-y)*self.dW)+(WIDTH/2), ((x+y)*self.dH), image)
                    self.tile_properties[layer_index][x][y] = self.tmxMap.getTileProperties((x, y, int(layer_index)))
                    inc = inc + 1 if inc + 1 <= self.num_tile_x*self.num_tile_y else inc
                    progress.update(inc)
        progress.finish()

    def get_pos(self, x, y, layer):
        return self.posList[layer][x][y][0], self.posList[layer][x][y][1]

    def get_properties(self, x, y, layer):
        if layer in self.posList:
            return self.posList[layer][x][y]
