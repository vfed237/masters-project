
#	AUTHOR:  vfed237

import copy
import random
from CvPythonExtensions import *
import CvUtil
import CvMapGeneratorUtil
from CvMapGeneratorUtil import TerrainGenerator
from CvMapGeneratorUtil import FeatureGenerator

def blank_map(map_height, map_width, value_to_set):
    blank_map = []
    i = 0
    while i < map_height:
        j = 0
        map_row = []
        while j < map_width:
            map_row.append(value_to_set)
            j += 1
        blank_map.append(map_row)
        i += 1
    return blank_map
    
def random_walk(rmap, max_iterations, border_cross, value_to_set):
    x_pos = int(len(rmap[0])/2)
    y_pos = int(len(rmap)/2)
    i = 0
    while i < max_iterations:
        rmap[y_pos][x_pos] = value_to_set
        rand_int = random.randint(0,3)
        if rand_int == 0:
            y_pos += 1
            if y_pos > (len(rmap) - 1):
                if border_cross:
                    y_pos = 0
                else:
                    y_pos -= 2
        elif rand_int == 1:
            y_pos -=1
            if y_pos < 0:
                if border_cross:
                    y_pos = len(rmap) - 1
                else:
                    y_pos = 1
        elif rand_int == 2:
            x_pos += 1
            if x_pos > (len(rmap[0]) - 1):
                if border_cross:
                    x_pos = 0
                else:
                    x_pos -= 2
        else:
            x_pos -= 1
            if x_pos < 0:
                if border_cross:
                    x_pos = len(rmap[0]) - 1
                else:
                    x_pos = 1
        i += 1
    return rmap

def cellular_automata(rmap, adjacent_cell_req, value_to_set):
    new_map = copy.deepcopy(rmap)
    i = 1
    while i < (len(rmap) - 1):
        j = 1
        while j < (len(rmap[0]) - 1):
            adjacent_cells_active = 0
            adjacent_cells_active += rmap[i - 1][j]
            adjacent_cells_active += rmap[i + 1][j]
            adjacent_cells_active += rmap[i][j - 1]
            adjacent_cells_active += rmap[i][j + 1]
            if adjacent_cells_active >= adjacent_cell_req and new_map[i][j] < value_to_set:
                new_map[i][j] = value_to_set
            else:
                new_map[i][j] = rmap[i][j]
            j += 1
        i += 1
    return new_map

def cellular_automata_any_adjacent(rmap, adjacent_cell_req, base_cell_req, value_to_set):
    new_map = copy.deepcopy(rmap)
    i = 1
    while i < (len(rmap) - 1):
        j = 1
        while j < (len(rmap[0]) - 1):
            adjacent_cells_active = 0
            if rmap[i - 1][j] == adjacent_cell_req:
                adjacent_cells_active = 1
            elif rmap[i + 1][j] == adjacent_cell_req:
                adjacent_cells_active = 1
            elif rmap[i][j - 1] == adjacent_cell_req:
                adjacent_cells_active = 1
            elif rmap[i][j + 1] == adjacent_cell_req:
                adjacent_cells_active = 1
            if adjacent_cells_active == 1 and new_map[i][j] == base_cell_req:
                new_map[i][j] = value_to_set
            else:
                new_map[i][j] = rmap[i][j]
            j += 1
        i += 1
    return new_map

def mutate_map(rmap, base_value, mutated_value, mutate_chance):
    new_map = []
    for i in rmap:
        map_row = []
        for j in i:
            if j == base_value and random.random() < mutate_chance:
                map_row.append(mutated_value)
            else:
                map_row.append(j)
        new_map.append(map_row)
    return new_map

def fix_ca_borders(rmap):
    last_index_y = len(rmap) - 1
    last_index_x = len(rmap[0]) - 1
    i = 0
    while i < len(rmap[0]):
        if rmap[0][i] == 1 and rmap[last_index_y][i] == 1:
            rmap[0][i] = 2
            rmap[last_index_y][i] = 2
        i += 1
    i = 1
    while i < (len(rmap) - 1):
        if rmap[i][0] == 1 and rmap[i][last_index_x] == 1:
            rmap[i][0] = 2
            rmap [i][last_index_x] = 2
        i += 1
    return rmap

def getDescription():
	return "A map that generates using a Random Walk algorithm."

def getNumCustomMapOptions():
	return 0

def isAdvancedMap():
	return 0
    
def isClimateMap():
	return 0

def isSeaLevelMap():
	return 0

def getWrapX():
	return True
    
def getWrapY():
	return True
        
def generatePlotTypes():
    gc = CyGlobalContext()
    civmap = gc.getMap()
    iNumPlotsX = civmap.getGridWidth()
    iNumPlotsY = civmap.getGridHeight()
    plotTypes = [PlotTypes.PLOT_OCEAN] * (iNumPlotsX*iNumPlotsY)
    space_count = iNumPlotsX*iNumPlotsY
    random_walk_count = space_count // 10
    global generated_map_to_use
    generated_map_to_use = blank_map(iNumPlotsY,iNumPlotsX,1)
    generated_map_to_use = random_walk(generated_map_to_use,space_count,True, 0)
    generated_map_to_use = cellular_automata(generated_map_to_use, 4, 2)
    generated_map_to_use = cellular_automata(generated_map_to_use, 4, 1)
    generated_map_to_use = fix_ca_borders(generated_map_to_use)
    generated_map_to_use = cellular_automata(generated_map_to_use, 12, 4)
    generated_map_to_use = mutate_map(generated_map_to_use, 2, 5, 0.01)
    generated_map_to_use = mutate_map(generated_map_to_use, 2, 6, 0.02)
    generated_map_to_use = mutate_map(generated_map_to_use, 2, 7, 0.01)
    generated_map_to_use = mutate_map(generated_map_to_use, 2, 4, 0.02)
    generated_map_to_use = mutate_map(generated_map_to_use, 2, 3, 0.02)
    generated_map_to_use = mutate_map(generated_map_to_use, 2, 8, 0.03)
    generated_map_to_use = cellular_automata_any_adjacent(generated_map_to_use, 6, 2, 6)
    generated_map_to_use = cellular_automata_any_adjacent(generated_map_to_use, 6, 2, 6)
    generated_map_to_use = cellular_automata_any_adjacent(generated_map_to_use, 5, 2, 5)
    generated_map_to_use = cellular_automata_any_adjacent(generated_map_to_use, 5, 2, 5)
    generated_map_to_use = cellular_automata_any_adjacent(generated_map_to_use, 7, 2, 7)
    generated_map_to_use = cellular_automata_any_adjacent(generated_map_to_use, 7, 2, 7)
    generated_map_to_use = cellular_automata_any_adjacent(generated_map_to_use, 8, 2, 8)
    generated_map_to_use = cellular_automata_any_adjacent(generated_map_to_use, 8, 2, 8)
    generated_map_to_use = cellular_automata_any_adjacent(generated_map_to_use, 4, 2, 3)
    generated_map_to_use = mutate_map(generated_map_to_use, 5, 2, 0.05)
    generated_map_to_use = mutate_map(generated_map_to_use, 6, 2, 0.05)
    generated_map_to_use = mutate_map(generated_map_to_use, 7, 2, 0.05)
    generated_map_to_use = mutate_map(generated_map_to_use, 4, 2, 0.05)
    generated_map_to_use = mutate_map(generated_map_to_use, 8, 2, 0.05)
    for i in range(iNumPlotsX*iNumPlotsY):
        yc = i//iNumPlotsX
        xc = i - yc * iNumPlotsX
        if generated_map_to_use[yc][xc] >= 5:
            plotTypes[i] = PlotTypes.PLOT_LAND
        elif generated_map_to_use[yc][xc] == 4:
            plotTypes[i] = PlotTypes.PLOT_PEAK
        elif generated_map_to_use[yc][xc] == 3:
            plotTypes[i] = PlotTypes.PLOT_HILLS
        elif generated_map_to_use[yc][xc] >= 1:
            plotTypes[i] = PlotTypes.PLOT_LAND
        else:
            plotTypes[i] = PlotTypes.PLOT_OCEAN     
    return plotTypes
	
def generateTerrainTypes():
    gc = CyGlobalContext()
    civmap = gc.getMap()
    iNumPlotsX = civmap.getGridWidth()
    iNumPlotsY = civmap.getGridHeight()
    terrainDesert = gc.getInfoTypeForString("TERRAIN_DESERT")
    terrainPlains = gc.getInfoTypeForString("TERRAIN_PLAINS")
    terrainIce = gc.getInfoTypeForString("TERRAIN_SNOW")
    terrainTundra = gc.getInfoTypeForString("TERRAIN_TUNDRA")
    terrainGrass = gc.getInfoTypeForString("TERRAIN_GRASS")
    terrainHill = gc.getInfoTypeForString("TERRAIN_HILL")
    terrainCoast = gc.getInfoTypeForString("TERRAIN_COAST")
    terrainOcean = gc.getInfoTypeForString("TERRAIN_OCEAN")
    terrainPeak = gc.getInfoTypeForString("TERRAIN_PEAK")

    terrainTypes = [0]*(iNumPlotsX*iNumPlotsY)
    for i in range(iNumPlotsX*iNumPlotsY):
        yc = i//iNumPlotsX
        xc = i - yc * iNumPlotsX
        if generated_map_to_use[yc][xc] == 8:
            terrainTypes[i] = terrainPlains
        elif generated_map_to_use[yc][xc] == 7:
            terrainTypes[i] = terrainIce
        elif generated_map_to_use[yc][xc] == 6:
            terrainTypes[i] = terrainTundra
        elif generated_map_to_use[yc][xc] == 5:
            terrainTypes[i] = terrainDesert
        elif generated_map_to_use[yc][xc] == 4:
            terrainTypes[i] = terrainGrass
        elif generated_map_to_use[yc][xc] >= 2:
            terrainTypes[i] = terrainGrass
        elif generated_map_to_use[yc][xc] == 1:
            terrainTypes[i] = terrainCoast
        else:
            terrainTypes[i] = terrainOcean
    return terrainTypes