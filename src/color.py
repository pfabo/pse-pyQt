import six

if six.PY2:
    from PyQt4.QtGui import QColor
else:
    from PyQt5.QtGui import QColor

def convertColor(value):
    '''
    Converts value between 0 and 1 to cold-hot color scale
    '''

    if (0 <= value and value <= 1 / 8):
        R = 0
        G = 0
        B = 4 * value + .5    # .5 - 1 // b = 1/2

    elif (1 / 8 < value and value <= 3 / 8):
        R = 0
        G = 4 * value - .5     # 0 - 1 // b = - 1/2
        B = 1                  # small fix

    elif (3 / 8 < value and value <= 5 / 8):
        R = 4 * value - 1.5    # 0 - 1 // b = - 3/2
        G = 1
        B = -4 * value + 2.5   # 1 - 0 // b = 5/2

    elif (5 / 8 < value and value <= 7 / 8):
        R = 1
        G = -4 * value + 3.5    # 1 - 0 // b = 7/2
        B = 0

    elif (7 / 8 < value and value <= 1):
        R = -4 * value + 4.5   # 1 - .5 // b = 9/2
        G = 0
        B = 0

    else:                    # should never happen - value > 1
        R = .5
        G = 0
        B = 0

    # scale for hex conversion
    R = int(R * 255)
    G = int(G * 255)
    B = int(B * 255)

    return R, G, B


class Color(object):
    aquamarine = QColor(112, 219, 147)
    black = QColor(0, 0, 0)
    blue = QColor(0, 0, 255)
    blueViolet = QColor(159, 95, 159)
    brown = QColor(165, 42, 42)
    cadetBlue = QColor(95, 159, 159)
    coral = QColor(255, 127, 0)
    cornflowerBlue = QColor(66, 66, 111)
    cyan = QColor(0, 255, 255)
    darkGrey = QColor(47, 47, 47)
    darkGreen = QColor(47, 79, 47)
    darkOliveGreen = QColor(79, 79, 47)
    darkOrchid = QColor(153, 50, 204)
    darkSlateBlue = QColor(107, 35, 142)
    darkSlateGrey = QColor(47, 79, 79)
    darkTurquoise = QColor(112, 147, 219)
    dimGrey = QColor(84, 84, 84)
    firebrick = QColor(142, 35, 35)
    forestGreen = QColor(35, 142, 35)
    gold = QColor(204, 127, 50)
    goldenrod = QColor(219, 219, 112)
    grey = QColor(128, 128, 128)
    green = QColor(0, 255, 0)
    greenYellow = QColor(147, 219, 112)
    indianRed = QColor(79, 47, 47)
    khaki = QColor(159, 159, 95)
    lightBlue = QColor(191, 216, 216)
    lightGrey = QColor(192, 192, 192)
    lightSteelBlue = QColor(143, 143, 188)
    limeGreen = QColor(50, 204, 50)
    lightMagenta = QColor(255, 0, 255)
    magenta = QColor(255, 0, 255)
    maroon = QColor(142, 35, 107)
    mediumAquamarine = QColor(50, 204, 153)
    mediumGrey = QColor(100, 100, 100)
    mediumBlue = QColor(50, 50, 204)
    mediumForestGreen = QColor(107, 142, 35)
    mediumGoldenrod = QColor(234, 234, 173)
    mediumOrchid = QColor(147, 112, 219)
    mediumSeaGreen = QColor(66, 111, 66)
    mediumSlateBlue = QColor(127, 0, 255)
    mediumSpringGreen = QColor(127, 255, 0)
    mediumTurquoise = QColor(112, 219, 219)
    mediumVioletRed = QColor(219, 112, 147)
    midnightBlue = QColor(47, 47, 79)
    navy = QColor(35, 35, 142)
    orange = QColor(204, 50, 50)
    orangeRed = QColor(255, 0, 127)
    orchid = QColor(219, 112, 219)
    paleGreen = QColor(143, 188, 143)
    pink = QColor(188, 143, 234)
    plum = QColor(234, 173, 234)
    purple = QColor(176, 0, 255)
    red = QColor(255, 0, 0)
    salmon = QColor(111, 66, 66)
    seaGreen = QColor(35, 142, 107)
    sienna = QColor(142, 107, 35)
    skyBlue = QColor(50, 153, 204)
    slateBlue = QColor(0, 127, 255)
    springGreen = QColor(0, 255, 127)
    steelBlue = QColor(35, 107, 142)
    tan = QColor(219, 147, 112)
    thistle = QColor(216, 191, 216)
    turquoise = QColor(173, 234, 234)
    violet = QColor(79, 47, 79)
    violetRed = QColor(204, 50, 153)
    wheat = QColor(216, 216, 191)
    white = QColor(255, 255, 255)
    yellow = QColor(255, 255, 0)
    yellowGreen = QColor(153, 204, 50)
    mediumGoldenrod = QColor(234, 234, 173)
    mediumForestGreen = QColor(107, 142, 35)
    lightMagenta = QColor(255, 0, 255)
    mediumGrey = QColor(100, 100, 100)

Color = Color()
