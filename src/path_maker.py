#!/usr/bin/python

"""
Pedro Melgueira - m11153
------------------------

This program parses a file containing one rect and one path SVG
elements. After the parsing the information is processed to output a
data structure convenient to test the first part of the SCAD course,
which deals with the use of HMMs.
"""

import sys
import ply.lex as lex
import ply.yacc as yacc
import math
import numpy as np

""" Parsed Information Will Go Here """

res_path = {}
res_rect = {}

""" Tokens """

tokens = (
    'TAG_OPEN', 'TAG_CLOSE',
    'PATH', 'RECT',
    'D', 'M', 'L', 'Z',
    'HEIGHT', 'WIDTH', 'X', 'Y',
    'OTHERARG',
    'COMMA',
    'QUOTES',
    'NUMBER'
)

# Define the tokens regex. Note that the use of the simpler form
# t_TOKENNAME = r'regex', was not used due to some bug in ply.
def t_TAG_OPEN(t):
    r'<'
    return t

def t_TAG_CLOSE(t):
    r'/>'
    return t

def t_PATH(t):
    r'path'
    return t

def t_RECT(t):
    r'rect'
    return t

def t_D(t):
    r'd='
    return t

def t_HEIGHT(t):
    r'height='
    return t

def t_WIDTH(t):
    r'width='
    return t

def t_X(t):
    r'x='
    return t

def t_Y(t):
    r'y='
    return t

def t_OTHERARG(t):
    # r'[a-z\-]+=".*"'
    r'[a-z\-]+="[a-zA-Z0-9 \-\.\,]*"'
    return t

def t_M(t):
    r'm'
    return t

def t_L(t):
    r'L'
    return t

def t_Z(t):
    r'z'
    return t

def t_COMMA(t):
    r','
    return t

def t_QUOTES(t):
    r'"'
    return t

def t_NUMBER(t):
    r'-?([0-9]*\.[0-9]+|[0-9]+)'
    try:
        t.value = float(t.value)
    except ValueError:
        t.value = 0
    return t

def t_newline(t):
    r'\n+'
    return ""

t_ignore = ' \t'

def t_error(t):
    print "ERROR!!", t
    t.lexer.skip(1)

lex.lex()

""" Rules """

# Tags
def p_line(t):
    '''line : tag
            | '''
    pass

def p_path_tag(t):
    'tag : TAG_OPEN PATH path_tag_content TAG_CLOSE'

def p_rect_tag(t):
    'tag : TAG_OPEN RECT rect_tag_content TAG_CLOSE'

# Path tag content
def p_path_tag_content(t):
    '''path_tag_content : D QUOTES path_def QUOTES
                        | D QUOTES path_def QUOTES path_tag_content'''
    pass

def p_path_tag_content_other(t):
    '''path_tag_content : OTHERARG
                        | OTHERARG path_tag_content'''
    pass

def p_path_def_m0(t):
    'path_def : M NUMBER COMMA NUMBER'
    res_path["path"] = [(t[2], t[4])]

def p_path_def_m1(t):
    'path_def : M NUMBER COMMA NUMBER path_def'''
    res_path["path"] = [(t[2], t[4])] + t[5]

def p_path_def_l0(t):
    'path_def : L NUMBER COMMA NUMBER'
    t[0] = [(t[2], t[4])]

def p_path_def_l1(t):
    'path_def : L NUMBER COMMA NUMBER path_def'
    t[0] = [(t[2], t[4])] + t[5]

def p_path_def_z(t):
    'path_def : Z'
    pass

# Rect tag content
def p_rect_tag_content_x(t):
    '''rect_tag_content : X QUOTES NUMBER QUOTES
                        | X QUOTES NUMBER QUOTES rect_tag_content'''
    res_rect["x"] = t[3]

def p_rect_tag_content_y(t):
    '''rect_tag_content : Y QUOTES NUMBER QUOTES
                        | Y QUOTES NUMBER QUOTES rect_tag_content'''
    res_rect["y"] = t[3]

def p_rect_tag_content_width(t):
    '''rect_tag_content : WIDTH QUOTES NUMBER QUOTES
                        | WIDTH QUOTES NUMBER QUOTES rect_tag_content'''
    res_rect["width"] = t[3]

def p_rect_tag_content_height(t):
    '''rect_tag_content : HEIGHT QUOTES NUMBER QUOTES
                        | HEIGHT QUOTES NUMBER QUOTES rect_tag_content'''
    res_rect["height"] = t[3]

def p_rect_tag_content_other(t):
    '''rect_tag_content : OTHERARG
                        | OTHERARG rect_tag_content'''
    pass

def p_error(t):
    print "Parssing error:", t

yacc.yacc()

""" Create Markov Chain """

def createMarkovChain(path, trans_prob):
    res = []

    for i in range(len(path)):
        l = [0.0] * len(path)
        l[i] = 1 - trans_prob
        l[(i-1) % len(path)] = trans_prob
        res.append(l)

    return np.array(res)

""" Create Observations Matrix """

def createObsMatrix(path, rect, variance):
    init_point = path[0]
    loop_list = path[1:] + [init_point]

    lp = init_point

    res = []

    def dist(x1, x2, y1, y2):
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)

    for i in loop_list:
        # Get bot orientation
        d = dist(lp[0], i[0], lp[1], i[1])
        a_cos = math.acos((i[0]-lp[0]) / d)
        a_sin = math.asin((i[1]-lp[1]) / d)
        orientation = a_cos if a_sin >= 0 else 2*math.pi - a_cos

        # Get Intersections
        if i[0]-lp[0] == 0:
            x_up = x_dn = None
            y_up = (i[0], rect["height"])
            y_dn = (i[0], rect["x"])

        elif i[1]-lp[1] == 0:
            x_up = (rect["width"], i[1])
            x_dn = (rect["x"], i[1])
            y_up = y_dn = None

        else:
            m = (i[1]-lp[1]) / (i[0]-lp[0])
            b = i[1] - m * i[0]

            x_up = (rect["width"],          rect["width"] * m + b)
            x_dn = (rect["x"],              rect["x"] * m + b)
            y_up = ((rect["height"]-b) / m, rect["height"])
            y_dn = ((rect["y"]-b) / m,      rect["y"])

        # half of section
        sec_half = ((i[0] + lp[0]) / 2.0, (i[1] + lp[1]) / 2.0)

        # Calc distance from half of section to walls
        x_dist = y_dist = -1
        if orientation >= 0.0 and orientation < math.pi / 2.0:
            if x_up != None: x_dist = dist(sec_half[0], x_up[0], sec_half[1], x_up[1])
            if y_up != None: y_dist = dist(sec_half[0], y_up[0], sec_half[1], y_up[1])

        elif orientation < math.pi:
            if x_dn != None: x_dist = dist(sec_half[0], x_dn[0], sec_half[1], x_dn[1])
            if y_up != None: y_dist = dist(sec_half[0], y_up[0], sec_half[1], y_up[1])

        elif orientation < math.pi * (3.0 / 2.0):
            if x_dn != None: x_dist = dist(sec_half[0], x_dn[0], sec_half[1], x_dn[1])
            if y_dn != None: y_dist = dist(sec_half[0], y_dn[0], sec_half[1], y_dn[1])

        else:
            if x_up != None: x_dist = dist(sec_half[0], x_up[0], sec_half[1], x_up[1])
            if y_dn != None: y_dist = dist(sec_half[0], y_dn[0], sec_half[1], y_dn[1])

        if x_dist == -1:
            last_dist = y_dist
        elif y_dist == -1:
            last_dist = x_dist
        else:
            last_dist = x_dist if x_dist < y_dist else y_dist

        if last_dist < 10:
            last_dist = 10.0
        elif last_dist > 100:
            last_dist = 100.0

        # Make array of observations
        obs_arr = [0.0] * 9
        index = int(last_dist / 10) - 1
        obs_arr[index] = 1.0
        error = np.array([1.0, 2.0, 4.0, 7.0, 13.0, 7.0, 4.0, 2.0, 1.0])
        error = error / sum(error)
        res.append(np.convolve(error, obs_arr, mode="same"))

        # Next step
        lp = i

    return np.array(res).T

""" Main """

# Take arguments
if len(sys.argv) != 2:
    print "Usage: path_maker input_file"
    exit()

in_file = open(sys.argv[1], "r")

# Main loop for parser
status = True
for i in in_file:
    yacc.parse(i)

print "Parsed Information"
print res_path
print res_rect

# Make matrices
print "Markov Chain"
print createMarkovChain(res_path["path"], 0.9)

print "Observations"
print createObsMatrix(res_path["path"], res_rect, 1)

# Close the file
in_file.close()

