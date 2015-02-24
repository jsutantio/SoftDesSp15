# Computational Art
# Jessica Sutantio
# SoftDes Spring 2015

import random
from PIL import Image
from math import *
from random import *

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """

        # single input functions
    t = [['cos_pi'],['sin_pi'],['exp']]

    # dual input functions
    s = [['X'],['Y'],['prod'],['avg'],['max']]

    if max_depth == 0:
        return choice([['a'],['b']])
    if min_depth <= 0:
        # randomly decide whether or not to continue with recursion
        contine_recurse = choice(['YES','NO'])
        if contine_recurse == 'NO':
            return choice([['a'],['b']])
        else:
            return build_random_function(min_depth-1,max_depth-1)

    else:
        function_type = choice(['one input','two input','two input'])
        if function_type == 'one input':
            function = choice(t)
            function.append(build_random_function(min_depth-1,max_depth-1))
            return function
        else:
            function = choice(s)
            function.append(build_random_function(min_depth-1,max_depth-1))
            function.append(build_random_function(min_depth-1,max_depth-1))
            return function

    #A less convoluted way to do it that I thought of but didn't have the time to tell you: Have one list of functions formatted like [ [cos_pi,place_holder], [X,place_holder_one,place_holder_two] ...]. Then choose any function from the list, and write a loop: for i in range(1,len(func)): func[i] = build_random_function(...). This will allow you to create functions that take any number of inputs with almost no code rewriting.

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(['a'],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(['b'],0.1,0.02)
        0.02
        >>> evaluate_random_function(['cos_pi',['b']],0.45,0.8)
        -0.8090169943749473
        >>> evaluate_random_function(['prod',['sin_pi',['b']],['avg',['a'],['b']]],-.01,.9)
        0.13751256249685165
        >>> evaluate_random_function(['max',['cos_pi',['b']],['avg',['a'],['a']]],-0.3,0)
        1.0
    """

    elem = f[0]
    # base case
    if elem == 'a': #You don't need to separate this base case from the other if statements. You could delete line 81 and just have a huge chunk of if statments.
        return x
    if elem == 'b': #A style thing: use elif when the cases are mutually excusive, instead of if. This makes it clear to a reader that you only expect one of these if statements to be true
        return y
    
    # evaluate the nested functions based on type
    else:
        # shorthand for recursion
        # clever!
        g = lambda funct: evaluate_random_function(funct,x,y) 
        if elem == 'X':
            return g(f[1])
        if elem == 'Y':
            return g(f[2])
        if elem == 'prod':
            return g(f[1])*g(f[2])
        if elem == 'avg':
            return 0.5*(g(f[1])+g(f[2]))
        if elem == 'cos_pi':
            return cos(pi*g(f[1]))
        if elem == 'sin_pi':
            return sin(pi*g(f[1]))
        if elem == 'exp':
            return 1.0/(1+exp(-g(f[1])))
        if elem == 'max':
            return max(g(f[1]),g(f[2]))

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """

    # check to see if val is in the interval
    # print 'val given to remap_interval: ' + str(val)
    if (val > input_interval_start) and (val < input_interval_end):
        input_offset = 0 - input_interval_start
        scale = float(val+input_offset)/(input_interval_end+input_offset)
        output_offset = 0 - output_interval_start
        val = scale*(output_interval_end+output_offset)
        return val - output_offset
    # did you add these statements checking val because this function won't work with certain inputs? It seemed to run fine without these if statements. If there is a case where these statements are nessecary, you should add a doctest that shows that case!
    if val == input_interval_start:
        return output_interval_start
    if val == input_interval_end:
        return output_interval_end


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    # print 'val given to color_map:' + str(val)
    color_code = remap_interval(val, -1, 1, 0, 255)
    # print 'color_code:' + str(color_code)
    return int(color_code)


def test_image(filename, x_size=600, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=500, y_size=500):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(8,15)
    # print red_function
    green_function = build_random_function(10,15)
    blue_function = build_random_function(14,16)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            # print 'x: ' +str(x)
            y = remap_interval(j, 0, y_size, -1, 1)
            # print 'y: ' +str(y)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    #generate_art("example5.png")
    
    # h = build_random_function(4,6)
    # print h
    # p = evaluate_random_function(h,0,0)
    # print p
    # print color_map(p)
