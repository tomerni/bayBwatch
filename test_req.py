import matplotlib.path as mplPath
import numpy as np

def test(coords_string):
    f = open("testfile", "w")
    for coord in coords_string.split(","):
        f.write(coord + "\n")
    f.close()
    f = open("coords", "r")
    lines = f.readlines()
    hz = []
    for line in lines:
        hz.append(line[:-1]) # TODO: Check if removing \n is really needed
    poly = [190, 50, 500, 310]
    bbPath = mplPath.Path(np.array([[poly[0], poly[1]],
                     [poly[1], poly[2]],
                     [poly[2], poly[3]],
                     [poly[3], poly[0]]]))

bbPath.contains_point((200, 100))
        
test("1,1,1,1,1,1,1,1")