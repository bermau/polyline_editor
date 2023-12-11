SIZE_X = 150
SIZE_Y = 200
__version__ = "0.1"
# Data are plotted from my polyline_editor tool.
data = {
    '0': [[(80, 9), (49, 13), (27, 35), (14, 60), (11, 98), (11, 137), (18, 168), (51, 185), (72, 191), (83, 190),
           (108, 178), (120, 153), (127, 111), (124, 78), (123, 51), (117, 39), (106, 22), (80, 9)]],
    '1': [[(23, 85), (86, 13), (85, 190)]],
    '2': [[(31, 64), (42, 41), (64, 26), (83, 23), (102, 36), (116, 56), (118, 90), (106, 108), (82, 134), (60, 148),
           (28, 176), (28, 183), (117, 182)]],
    '3': [[(8, 35), (48, 20), (72, 23), (92, 28), (106, 46), (115, 69), (113, 90), (94, 110), (45, 112)],
          [(45, 115), (109, 122), (112, 140), (113, 158), (106, 173), (70, 187), (34, 186), (10, 172)]],
    '4': [[(64, 12), (5, 102), (94, 101)],  [(64, 187)], [(67, 6), (69, 193)]],
    '5': [
        [(11, 18), (13, 99), (56, 93), (82, 100), (107, 118), (112, 138), (111, 171), (70, 191), (28, 189), (12, 179)],
        [(11, 12), (107, 16)]],
    '6': [[(132, 48), (116, 24), (90, 17), (60, 23), (40, 39), (38, 82), (44, 122), (45, 159), (73, 191), (116, 181),
           (130, 166), (137, 118), (116, 97), (70, 103), (46, 132)]],
    '7': [[(32, 26), (138, 24), (98, 178)], [(58, 96), (118, 97)]],
    '8': [[(32, 67), (43, 23), (97, 23), (124, 55), (107, 100), (61, 132), (53, 163), (75, 192), (126, 187), (140, 149),
           (82, 91), (52, 79), (32, 67)]],
    '9': [[(67, 8), (22, 18), (8, 50), (4, 82), (21, 109), (78, 106), (104, 102), (117, 55), (101, 18), (74, 11),
           (91, 17), (112, 38), (113, 88), (108, 124), (104, 156), (99, 182), (60, 194), (29, 183), (9, 154)]]
}


# LA grille initiale était de 150, 200.
# Les ccordonnées ci dessus sont façon pygame, je préfère le cartésien.
def pygame_to_cartersian(point):
    """
    :param point:
    :return:

    >>> pygame_to_cartersian((25, 30))
    (25, 170)
    """
    return (point[0], SIZE_Y - point[1])


data_cart = {}

for key in data:
    data_cart[key] = []
    for line in data[key]:
        AA = [pygame_to_cartersian(point) for point in line]
        data_cart[key].append(AA)


# Maintenant les données sont en mode cartésien, ce qui me semble plus simple à utiliser.
PEN_UP = "G0 Z1 ; pen up"
PEN_DOWN = "G0 Z-1 ; pen down"

class Tracer:
    def __init__(self):
        self.font_with = 2    # mm
        self.font_height = 2  # mm
        self.cur_x = 0
        self.cur_y = 0  # Suit la position en bas à gauche pour chaque lettre.

    def tracer_lettre(self, lettre):
        """
        :param lettre:
        :param start_x:
        :param start_y:
        :return:   gcode for a letter
        """
        if lettre not in data_cart:
            print("Erreur")
            raise ValueError(f"Error for letter '{lettre}'")
        else:
            gcode = [f"; letter {letter}"]

            for i, path in enumerate(data_cart[lettre]):
                gcode.append(f"; path {i} for letter {lettre}")
                # first point : move then down the pen
                point = path[0]
                x, y = self.correct_x(point), self.correct_y(point)
                gcode.append(f"G0 X{str(x)} Y{str(y)}")
                gcode.append(PEN_DOWN)
                if len(path) > 1:
                    for point in path[1:]:
                        x, y = self.correct_x(point), self.correct_y(point)
                        gcode.append(f"G0 X{str(x)} Y{str(y)}")
                    gcode.append(PEN_UP)
            self.cur_x += 2  # mm
            return gcode

    def correct_y(self, point) -> float:
        y = point[1] / SIZE_Y * self.font_height + self.cur_y
        return y

    def correct_x(self, point):
        x = point[0] / SIZE_X * self.font_with + self.cur_x
        return x


if __name__ == '__main__':
    t = Tracer()
    word = "234"
    retour_x, retour_y = (0, 0)
    code = [f"; version {__version__}"]
    code.append(PEN_UP)
    for letter in word:
        code += t.tracer_lettre(letter)
    for line in code:
        print(line)

    with open("./sortie.gc", "w") as f:
        for line in code:
            f.write(line+"\n")
