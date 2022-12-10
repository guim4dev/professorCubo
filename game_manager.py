import numpy as np
from rubik_solver import utils


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

class Game_manager:
    def __init__(self):
        self.cube_faces = np.empty(shape=(6,9), dtype=np.unicode_)
        self.last_captured_face = np.empty(shape=9, dtype=np.unicode_)
        self.stable_capture_count = 0
        self.solution = None
        self.expected_cube = None
        self.last_instruction = ""

    def from_squares_to_face(self, squares):
        try:
            result = np.empty(shape=(3,3), dtype=np.unicode_)
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
                result[y_lane, x_lane] = s.color
            
            return result
        except Exception as e:
            print(e)
            return[]

    def getNextMove(self,squares):
        face = self.from_squares_to_face(squares)
        if(len(face) == 0): return ""
        if(np.any(''== face)): return ""
        flat_face = face.flatten()

        if(not np.array_equal(flat_face, self.last_captured_face)):
            self.stable_capture_count = 0
            self.last_captured_face = flat_face
            return ""
        
        if(self.stable_capture_count != 1):
            self.stable_capture_count+= 1
            return ""
        
        face_ix = color_to_face[flat_face[4]]

        if(np.any(self.cube_faces[face_ix] == '')):
            if(face_ix == 0):
                face = np.flip(face)
            if(face_ix == 3):
                face = np.rot90(face)

            self.cube_faces[face_ix] = face.flatten()
            if(np.any(self.cube_faces == '')): return self.nextFaceToShow(face_ix)
        
        
        if(np.any(self.cube_faces == '')):
            return ""

        if self.solution == None:
            print("".join(self.cube_faces.flatten()))
            self.solution = utils.solve("".join(self.cube_faces.flatten()), 'Kociemba')
            print(self.solution)

        
    
    def nextFaceToShow(self, face_ix):
        if(face_ix == 0):
            return "MOVE LEFT"
        if(face_ix == 1):
            return "MOVE LEFT"
        if(face_ix == 2):
            return "MOVE LEFT"
        if(face_ix == 3):
            return "MOVE LEFT"
        if(face_ix == 4):
            return "MOVE UP"
        if(face_ix == 5):
            return "MOVE UP"

