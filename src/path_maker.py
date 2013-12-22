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

""" Parsed Information Will Go Here """

res_path = {}
res_rect = {}

""" Tokens """
tokens = (
    'TAG_OPEN', 'TAG_CLOSE',
    'PATH', 'RECT',
    'D', 'M', 'C', 'L', 'Z',
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

def t_M(t):
    r'm'
    return t

def t_C(t):
    r'c'
    return t

def t_L(t):
    r'l'
    return t

def t_Z(t):
    r'z'
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
    r'[a-z\-]+=".*"'
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
        t.value = int(t.value)
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

def p_path_def_m(t):
    '''path_def : M NUMBER COMMA NUMBER
                | M NUMBER COMMA NUMBER path_def'''
    pass

def p_path_def_c(t):
    '''path_def : C NUMBER COMMA NUMBER NUMBER COMMA NUMBER NUMBER COMMA NUMBER path_def
                | C NUMBER COMMA NUMBER NUMBER COMMA NUMBER NUMBER COMMA NUMBER'''
    pass

def p_path_def_l(t):
    '''path_def : L NUMBER COMMA NUMBER path_def
                | L NUMBER COMMA NUMBER'''
    pass

def p_path_def_z(t):
    'path_def : Z'
    pass

# Rect tag content
def p_rect_tag_content_x(t):
    '''rect_tag_content : X QUOTES NUMBER QUOTES
                        | X QUOTES NUMBER QUOTES rect_tag_content'''
    pass

def p_rect_tag_content_y(t):
    '''rect_tag_content : Y QUOTES NUMBER QUOTES
                        | Y QUOTES NUMBER QUOTES rect_tag_content'''
    pass

def p_rect_tag_content_width(t):
    '''rect_tag_content : WIDTH QUOTES NUMBER QUOTES
                        | WIDTH QUOTES NUMBER QUOTES rect_tag_content'''
    pass

def p_rect_tag_content_height(t):
    '''rect_tag_content : HEIGHT QUOTES NUMBER QUOTES
                        | HEIGHT QUOTES NUMBER QUOTES rect_tag_content'''
    pass

def p_rect_tag_content_other(t):
    '''rect_tag_content : OTHERARG
                        | OTHERARG rect_tag_content'''
    pass

def p_error(t):
    print "Parssing error:", t

yacc.yacc()

""" Main """

# Take arguments
if len(sys.argv) != 3:
    print "Usage: path_maker input_file output_file"
    exit()

in_file = open(sys.argv[1], "r")
out_file = open(sys.argv[2], "w")

# Main loop for parser
status = True
for i in in_file:
    yacc.parse(i)

# Close the files
in_file.close()
out_file.close()

