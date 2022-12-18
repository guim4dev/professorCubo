from tracemalloc import start
import numpy as np
from rubik.cube import Cube
from rubik_solver import utils
from rubik.optimize import *

#     Y
#   B R G O
#     W

color_to_face ={
    'Y':0,
    'B':1,
    'R':2,
    'G':3,
    'O':4,
    'W':5, 
}

class Arrow:
    def __init__(self, start, end):
        self.start = (int(start[0]), int(start[1]))
        self.end = (int(end[0]), int(end[1]))
    def inverse(self):
        return Arrow (self.end, self.start)

class Game_manager:
    def __init__(self):
        self.cube_faces = np.empty(shape=(6,9), dtype=np.unicode_)
        self.last_captured_face = np.empty(shape=9, dtype=np.unicode_)
        self.solution = None
        self.cube = None
        self.current_step = None
        self.initial_setup_done = False
        self.expected_face = None

    def squaresToFace(self, squares):
        grid = self.squaresToGrid(squares)
        if(len(grid) == 0): return []
        if(np.any(None == grid)): return []
        
        for row in range(len(grid)):
            for column in range(len(grid[row])):
                grid[row,column] = grid[row,column].color
        return grid

    def getNextMove(self,squares):
        face = self.squaresToFace(squares)
        if(len(face) == 0): return ""
        if(np.any(''== face)): return ""

        if(not self.initial_setup_done):
            return self.stepToArrows(squares, self.initialSetup(face))
            
        face_ix = color_to_face[face[1,1]]

        if self.current_step[0] != 'B' and self.current_step[0] != 'F' and face_ix != 2:
            print("MOVE LEFT")
            return self.stepToArrows(squares, "MOVE LEFT")
        
        if (self.current_step[0] == 'B' or self.current_step[0] == 'F') and face_ix != 3:
            print("MOVE RIGHT")
            return self.stepToArrows(squares, "MOVE RIGHT")

        if np.any(face.flatten() != self.expected_face):
            print(self.current_step)
            return self.stepToArrows(squares, self.current_step)
        else:
            self.doOneStepInternalCube()
            print("MANDOU BEM!")
        
    def nextFaceToSetup(self, face_ix):
        if(face_ix == 0):
            print("MOVE LEFT")
            return "MOVE LEFT"
        if(face_ix == 1):
            print("MOVE LEFT")
            return "MOVE LEFT"
        if(face_ix == 2):
            print("MOVE LEFT")
            return "MOVE LEFT"
        if(face_ix == 3):
            print("MOVE LEFT")
            return "MOVE LEFT"
        if(face_ix == 4):
            print("MOVE UP")
            return "MOVE UP"
        if(face_ix == 5):
            print("MOVE UP")
            return "MOVE UP"

    def initialSetup(self, face):
        face_ix = color_to_face[face[1,1]]

        if(np.any(self.cube_faces == '') or face_ix != 2):
            if(face_ix == 0):
                face = np.flip(face)
            if(face_ix == 3):
                face = np.rot90(face)
            flat_face = face.flatten()

            self.cube_faces[face_ix] = flat_face    

            return self.nextFaceToSetup(face_ix)

        self.initial_setup_done = True
        self.cube = Cube(self.toDumbFormat((self.cube_faces.flatten())))
        self.solution = utils.solve("".join(self.cube_faces.flatten()), 'Kociemba')
        self.solution = [s.raw for s in self.solution]
        print(self.solution)
        self.doOneStepInternalCube()
        return ""

    def stepToArrows(self, squares, step):
        arrows = []
        #cv2.arrowedLine(im, (biggest_x, lowest_y), (biggest_x,biggest_y), (150, 150, 150), 10)
        grid = self.squaresToGrid(squares)
        if(len(grid) == 0): return []
        if(np.any(None == grid)): return []

        top_right = grid[0,2]
        top_mid = grid[0,1]
        top_left = grid[0,0]
        mid_right = grid[1,2]
        mid_left = grid[1,0]
        bottom_right = grid[2,2]
        bottom_mid = grid[2,1]
        bottom_left = grid[2,0]

        if step == 'MOVE RIGHT':
            arrows.append(Arrow((top_right.x + top_right.w, top_right.y + top_right.w/2), (top_left.x, top_left.y + top_left.w/2)))
            arrows.append(Arrow((mid_right.x + mid_right.w, mid_right.y + mid_right.w/2), (mid_left.x, mid_left.y + mid_left.w/2)))
            arrows.append(Arrow((bottom_right.x + bottom_right.w, bottom_right.y + bottom_right.w/2), (bottom_left.x, bottom_left.y + bottom_left.w/2)))

        elif step == 'MOVE LEFT':
            arrows.append(Arrow((top_left.x, top_left.y + top_left.w/2), (top_right.x + top_right.w, top_right.y + top_right.w/2)))
            arrows.append(Arrow((mid_left.x, mid_left.y + mid_left.w/2), (mid_right.x + mid_right.w, mid_right.y + mid_right.w/2)))
            arrows.append(Arrow((bottom_left.x, bottom_left.y + bottom_left.w/2), (bottom_right.x + bottom_right.w, bottom_right.y + bottom_right.w/2)))

        elif step == 'MOVE UP':
            arrows.append(Arrow((top_right.x + top_right.w/2, top_right.y), (bottom_right.x + bottom_right.w/2, bottom_right.y + bottom_right.w)))
            arrows.append(Arrow((top_mid.x + top_mid.w/2, top_mid.y), (bottom_mid.x + bottom_mid.w/2, bottom_mid.y + bottom_mid.w)))
            arrows.append(Arrow((top_left.x + top_left.w/2, top_left.y), (bottom_left.x + bottom_left.w/2, bottom_left.y + bottom_left.w)))

        elif step == 'U':
            arrows.append(Arrow((top_right.x + top_right.w, top_right.y + top_right.w/2), (top_left.x, top_left.y + top_left.w/2)))
        
        elif step == 'L':
            arrows.append(Arrow((top_left.x + top_left.w/2, top_left.y), (bottom_left.x + bottom_left.w/2, bottom_left.y + bottom_left.w)))   

        elif step == 'F':
            arrows.append(Arrow((top_left.x + top_left.w/2, top_left.y), (bottom_left.x + bottom_left.w/2, bottom_left.y + bottom_left.w)))

        elif step == 'R':
            arrows.append(Arrow((bottom_right.x + bottom_right.w/2, bottom_right.y + bottom_right.w), (top_right.x + top_right.w/2, top_right.y))) 

        elif step == 'B':
            arrows.append(Arrow((bottom_right.x + bottom_right.w/2, bottom_right.y + bottom_right.w), (top_right.x + top_right.w/2, top_right.y)))     

        elif step == 'D':
            arrows.append(Arrow((bottom_left.x, bottom_left.y + bottom_left.w/2), (bottom_right.x + bottom_right.w, bottom_right.y + bottom_right.w/2)))    

        elif step == "U'":
            arrows.append(arrows.append(Arrow((top_right.x + top_right.w, top_right.y + top_right.w/2), (top_left.x, top_left.y + top_left.w/2))).inverse())        
        
        elif step == "L'":
            arrows.append(Arrow((top_left.x + top_left.w/2, top_left.y), (bottom_left.x + bottom_left.w/2, bottom_left.y + bottom_left.w)).inverse()) 

        elif step == "F'":
            arrows.append(Arrow((top_left.x + top_left.w/2, top_left.y), (bottom_left.x + bottom_left.w/2, bottom_left.y + bottom_left.w)).inverse())
        
        elif step == "R'":
            arrows.append(Arrow((bottom_right.x + bottom_right.w/2, bottom_right.y + bottom_right.w), (top_right.x + top_right.w/2, top_right.y)).inverse()) 

        elif step == "B'":
            arrows.append(Arrow((bottom_right.x + bottom_right.w/2, bottom_right.y + bottom_right.w), (top_right.x + top_right.w/2, top_right.y)).inverse())     
    
        elif step == "D'":
            arrows.append(Arrow((bottom_left.x, bottom_left.y + bottom_left.w/2), (bottom_right.x + bottom_right.w, bottom_right.y + bottom_right.w/2)).inverse())    

        return arrows

    def squaresToGrid(self, squares):
        try:
            result = np.empty(shape=(3,3), dtype=object)
            if len(squares) != 9: return []

            biggest_x = max([s.x for s in squares])
            smallest_x = min([s.x for s in squares])
            biggest_y = max([s.y for s in squares])
            smallest_y = min([s.y for s in squares])

            x_lane_size = (biggest_x - smallest_x)/3
            y_lane_size = (biggest_y - smallest_y)/3

            x_lanes = [smallest_x + x_lane_size/2 + i*x_lane_size for i in range(3)]
            y_lanes = [smallest_y + y_lane_size/2 + i*y_lane_size for i in range(3)]

            for s in squares:
                x_distances_to_lanes = [abs(s.x- l) for l in x_lanes]
                y_distances_to_lanes = [abs(s.y- l) for l in y_lanes]
                x_lane = x_distances_to_lanes.index(min(x_distances_to_lanes))
                y_lane = y_distances_to_lanes.index(min(y_distances_to_lanes))
                result[y_lane, x_lane] = s
            
            return result
        except Exception as e:
            print(e)
            return[]

    def doOneStepInternalCube(self):
        if len(self.solution) == 0:
            print("BRABOOO!")
            return

        nextStep = self.solution[0]
        if nextStep[-1] == '2':
            self.solution[0] = nextStep[:-1]
            self.solution.insert(0,nextStep[:-1])
            nextStep = nextStep[:-1]
        self.current_step = nextStep

        if nextStep == 'U':
            self.cube.U()
        if nextStep == 'L':
            self.cube.L()
        if nextStep == 'F':
            self.cube.F()
        if nextStep == 'R':
            self.cube.R()
        if nextStep == 'B':
            self.cube.B()
        if nextStep == 'D':
            self.cube.D()    
        if nextStep == "U'":
            self.cube.Ui()
        if nextStep == "L'":
            self.cube.Li()
        if nextStep == "F'":
            self.cube.Fi()
        if nextStep == "R'":
            self.cube.Ri()
        if nextStep == "B'":
            self.cube.Bi()
        if nextStep == "D'":
            self.cube.Di()       

        self.solution = self.solution[1:]
        expected_cube = self.toSmartFormat(self.cube._color_list())
        if self.current_step[0] == 'B' or self.current_step[0] == 'F':
            self.expected_face = expected_cube[27:36]
        else:
            self.expected_face = expected_cube[18:27]

    def toDumbFormat(self, cube):
        new_cube_str = np.empty(shape=6*9, dtype=np.unicode_)
        new_cube_str[0:12] = cube[0:12]

        new_cube_str[12:15] = cube[18:21]
        new_cube_str[15:18] = cube[27:30]
        new_cube_str[18:21] = cube[36:39]

        new_cube_str[21:24] = cube[12:15]
        new_cube_str[24:27] = cube[21:24]
        new_cube_str[27:30] = cube[30:33]
        new_cube_str[30:33] = cube[39:42]

        new_cube_str[33:36] = cube[15:18]
        new_cube_str[36:39] = cube[24:27]
        new_cube_str[39:42] = cube[33:36]
        new_cube_str[42:45] = cube[42:45]

        new_cube_str[45:54] = cube[45:54]
        return "".join(new_cube_str)
    
    def toSmartFormat(self, cube):
        new_cube_str = np.empty(shape=6*9, dtype=np.unicode_)
        new_cube_str[0:12] = cube[0:12]  

        new_cube_str[18:21]= cube[12:15]
        new_cube_str[27:30]= cube[15:18]
        new_cube_str[36:39]= cube[18:21]

        new_cube_str[12:15]= cube[21:24]
        new_cube_str[21:24]= cube[24:27]
        new_cube_str[30:33]= cube[27:30]
        new_cube_str[39:42]= cube[30:33]

        new_cube_str[15:18]= cube[33:36]
        new_cube_str[24:27]= cube[36:39]
        new_cube_str[33:36]= cube[39:42]
        new_cube_str[42:45]= cube[42:45]

        new_cube_str[45:54]= cube[45:54]
        return new_cube_str        